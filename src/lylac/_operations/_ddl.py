from typing import Any
from typing import Generic
from typing import Sequence
from sqlalchemy import types
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.orm import aliased
from sqlalchemy.orm import class_mapper
from .._constants import FACTORY_FIELDS
from .._constants import FACTORY_MODELS
from .._constants import FIELD_NAME
from .._contexts import ExecutionContext
from .._core import Feature
from .._core import Metadata
from .._core import ModelTemplate
from .._core.models import _Base
from .._resources import DatabaseMetadata
from .._resources import ModelColumnBasicAtts
from .._resources import ModelsBearer
from .._services import ConnectionService
from .._typing.aliases import ModelClass
from .._typing.callables import ColumnBuilder
from .._typing.generics import ModelName
from .._typing.interfaces import Many2ManyRelation
from .._typing.literals import OnDeleteOption
from .._typing.literals import TTypeName
from .._typing.type_parameters import _M
from .._utils import build_many2many_relation_name
from .._utils import get_table_name

class DDL(Generic[_M]):
    _build_column_callback: dict[TTypeName, ColumnBuilder]
    _ttype_to_dbtype: dict[TTypeName, str] = {
        'integer': 'INTEGER',
        'char': 'VARCHAR(255)',
        'float': 'FLOAT',
        'boolean': 'BOOLEAN',
        'date': 'DATE',
        'datetime': 'TIMESTAMP',
        'time': 'TIME',
        'duration': 'INTERVAL',
        'file': 'BYTEA',
        'text': 'TEXT',
        'selection': 'VARCHAR(255)',
        'many2one': 'INTEGER',
        'json': 'JSONB',
    }

    def __init__(
        self,
        models_bearer: ModelsBearer[_M],
        database_metadata: DatabaseMetadata,
    ) -> None:

        self._connection = ConnectionService()
        self._models_bearer = models_bearer
        self._database_metadata = database_metadata
        self._base = _Base

        # Inicialización de mapa de funciones de construcción de instancias de campo
        self._initialize_columns_builder()

    def create_field_column(
        self,
        name: str,
        ttype: TTypeName,
        model_name: ModelName[_M],
        nullable: bool,
        unique: bool,
        default_value: Any,
        related_model_table_name: str | None,
        on_delete: OnDeleteOption | None,
    ) -> None:

        # Inicialización de la instancia de definición de campo
        field_definition = ModelColumnBasicAtts(
            nullable= nullable,
            unique= unique,
            default= default_value,
        )

        # Inicialización de instancia de campo
        field_instance = self._build_column_callback[ttype](field_definition, related_model_table_name, on_delete)

        # Obtención del modelo del campo
        model_model = self._models_bearer.get_model(model_name)

        # Se añade la instancia de campo como atributo del modelo
        setattr(
            model_model,
            name,
            field_instance,
        )
        # Se registra la instancia al modelo en el esquema de SQLAlchemy
        class_mapper(model_model).add_property(name, field_instance)

    def add_column_to_table(
        self,
        model_table_name: str,
        field_name: str,
        field_ttype: TTypeName,
        default_value: Any,
        related_model_table_name: str | None,
        on_delete: OnDeleteOption | None,
        conn: Connection,
    ):

        db_type = self._ttype_to_dbtype[field_ttype]

        # default_value_query
        if default_value is None:
            default_value_query = ''
        else:
            if isinstance(default_value, str):
                value = f"'{default_value}'"
            elif isinstance(default_value, bool):
                value = str(default_value).upper()
            else:
                value = str(default_value)
            default_value_query = f'DEFAULT {value}'

        if field_ttype != 'many2one':
            constraint = ''
        else:
            constraint = (
                f"""
                ALTER TABLE {model_table_name}
                ADD CONSTRAINT {model_table_name}_{field_name}_fkey
                FOREIGN KEY ({field_name})
                REFERENCES {related_model_table_name}({FIELD_NAME.ID})
                ON DELETE {on_delete.replace('_', ' ').upper()};
                """
            )

        main_query = text(
            f"""
            ALTER TABLE {model_table_name} ADD COLUMN {field_name} {db_type}
            {default_value_query};
            {constraint}
            """
        )

        conn.execute(main_query)

    def create_model_table(
        self,
        conn: Connection,
        model_table_name: str,
        model_name: ModelName[_M],
        has_sequence: bool = False,
        is_archivable: bool = False,
        has_label: bool = False,
    ) -> None:

        # Obtención del modelo
        model_model = self.create_model_class(
            model_table_name,
            has_sequence,
            is_archivable,
            has_label,
        )
        # Creación de la tabla en la base de datos
        model_model.__table__.create(conn)
        # Se añade el modelo al portador de modelos
        self._models_bearer.add_model(model_name, model_model)

        return model_model

    def delete_model_table(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
    ) -> None:

        # Obtención de la clase del modelo
        model_model = self._models_bearer._index[model_name]
        # Remoción del modelo de los metadatos de Base
        model_model.__table__.drop(execution_ctx.conn)
        # Suscripción para eliminación del modelo en el portador de modelos
        execution_ctx.run_after_commit(
            lambda _: self._models_bearer.discard_model(model_name)
        )

    def rebuild_from_existing_database(
        self,
        conn: Connection,
    ) -> None:

        # Obtención de clases de modelos para armar queries
        base_model = Metadata.BaseModel
        base_model_field = Metadata.BaseModelField
        parent_model = aliased(base_model)
        related_model = aliased(base_model)

        # Query para búsqueda de registros de modelos
        base_model__stmt = (
            select(
                base_model.name,
                base_model.model,
                base_model.has_sequence,
                base_model.is_archivable,
                base_model.has_label,
            )
            .where(base_model.model.notin_(FACTORY_MODELS))
        )

        # Obtención de los datos de la búsqueda
        result: Sequence[tuple[str, str]] = (
            conn
            .execute(base_model__stmt)
            .fetchall()
        )

        # Iteración por las propiedades obtenidas de cada registro de modelo encontrado
        for ( model_table_name, model_name, has_sequence, is_archivable, has_label ) in result:
            # Creación de la clase del modelo
            model_model = self.create_model_class(
                model_table_name,
                has_sequence,
                is_archivable,
                has_label,
            )
            # Se añade la clase del modelo al portador de modelos
            self._models_bearer.add_model(model_name, model_model)

        # Query para búsqueda de registros de campos de modelos
        base_model_field__stmt = (
            select(
                base_model_field.name,
                base_model_field.ttype,
                parent_model.model,
                base_model_field.nullable,
                base_model_field.unique,
                base_model_field.default_value,
                related_model.name,
                base_model_field.on_delete,
            )
            .select_from(base_model_field)
            .outerjoin(
                parent_model,
                base_model_field.model_id == parent_model.id,
            )
            .outerjoin(
                related_model,
                base_model_field.related_model_id == related_model.id,
            )
            .where(
                and_(
                    base_model_field.state != 'base',
                    base_model_field.name.notin_(FACTORY_FIELDS),
                    base_model_field.is_computed == False,
                )
            )
            .order_by(base_model_field.id)
        )

        # Obtención de los datos de la búsqueda
        result: Sequence[tuple[str, TTypeName, ModelName[_M], bool, bool, str, str, str]] = (
            conn
            .execute(base_model_field__stmt)
            .fetchall()
        )

        # Iteración por las propiedades de cada registro de campo encontrado
        for ( name, ttype, model_name, nullable, unique, default_value, related_model_table_name, on_delete ) in result:

            # Si el campo es de tipo de one2many o many2many...
            if ttype == 'one2many':
                # No se hace nada
                continue

            # Si el campo es de tipo many2many...
            elif ttype == 'many2many':
                # Creación de la clase de la relación many2many
                self._create_m2m_model(
                    name,
                    model_name,
                    related_model_table_name,
                )

            else:
                # Creación del campo en su modelo correspondiente
                self.create_field_column(
                    name,
                    ttype,
                    model_name,
                    nullable,
                    unique,
                    default_value,
                    related_model_table_name,
                    on_delete,
                )

    def create_model_class(
        self,
        model_table_name: str,
        has_sequence: bool = False,
        is_archivable: bool = False,
        has_label: bool = False,
    ) -> ModelClass:

        # Inicialización de lista de clases a heredar
        classes_to_inherit = [_Base, ModelTemplate]
        # Si el modelo tiene secuencia...
        if has_sequence:
            # Se añade la clase de secuencia
            classes_to_inherit.append(Feature.HasSequence)
        # Si el modelo permite archivar...
        if is_archivable:
            # Se añade la clase de secuencia
            classes_to_inherit.append(Feature.Archivable)
        # Si el modelo tiene secuencia...
        if has_label:
            # Se añade la clase de secuencia
            classes_to_inherit.append(Feature.LabeledModel)

        # Inicialización de clase de modelo
        model_model = type(
            model_table_name,
            tuple(classes_to_inherit),
            {'__tablename__': model_table_name},
        )

        return model_model

    def create_m2m_relation_table(
        self,
        conn: Connection,
        field_name: str,
        model_name: ModelName[_M],
        related_model_table_name: str,
    ) -> None:

        # Construcción y registro del modelo
        m2m_model_model = self._create_m2m_model(field_name, model_name, related_model_table_name)

        # Creación de la tabla en la base de datos
        m2m_model_model.__table__.create(conn)

    def drop_database(
        self,
    ) -> None:

        # Eliminación de toda la base de datos
        self._base.metadata.drop_all(self._connection._engine)

    def _create_m2m_model(
        self,
        field_name: str,
        model_name: ModelName[_M],
        related_model_table_name: str,
    ) -> type[Many2ManyRelation]:

        # Obtención del nombre de la tabla del modelo
        model_table_name = get_table_name(model_name)
        # Construcción del nombre para índice
        name_for_index = f'{model_table_name}__{field_name}'

        # Creación de clase de modelo many2many
        m2m_model_model = self._create_m2m_relation_model_class(model_table_name, related_model_table_name, field_name)

        # Registro del modelo en el portador de modelos
        self._models_bearer.add_m2m_model(name_for_index, m2m_model_model)

        return m2m_model_model

    def _create_m2m_relation_model_class(
        self,
        x_model_table_name: str,
        y_model_table_name: str,
        m2m_field_name: str,
    ) -> type[Many2ManyRelation]:

        # Construcción de nombre de modelo
        m2m_model_name = build_many2many_relation_name(x_model_table_name, y_model_table_name, m2m_field_name)

        # Definición de instancia de campo X
        x_field = Column(
            types.Integer,
            ForeignKey(
                f'{x_model_table_name}.{FIELD_NAME.ID}',
                ondelete= "CASCADE",
            ),
            primary_key= True,
        )

        # Definición de instancia de campo Y
        y_field = Column(
            types.Integer,
            ForeignKey(
                f'{y_model_table_name}.{FIELD_NAME.ID}',
                ondelete= "CASCADE"
            ),
            primary_key= True,
        )

        # Creación de la clase del modelo
        m2m_model_model = type(
            m2m_model_name,
            (_Base,),
            {
                '__tablename__': m2m_model_name,
                'x': x_field,
                'y': y_field,
            },
        )

        return m2m_model_model

    def _initialize_columns_builder(
        self,
    ) -> None:

        # Construcción de mapa de funciones para creación de instancias de campo para modelos
        self._build_column_callback = {
            'integer': lambda definition, _, __: Column(types.Integer, **definition),
            'char': lambda definition, _, __: Column(types.String(255), **definition),
            'float': lambda definition, _, __: Column(types.Float, **definition),
            'boolean': lambda definition, _, __: Column(types.Boolean, **definition),
            'date': lambda definition, _, __: Column(types.Date, **definition),
            'datetime': lambda definition, _, __: Column(types.DateTime, **definition),
            'time': lambda definition, _, __: Column(types.Time, **definition),
            'duration': lambda definition, _, __: Column(types.Interval, **definition),
            'file': lambda definition, _, __: Column(types.LargeBinary, **definition),
            'text': lambda definition, _, __: Column(types.Text, **definition),
            'selection': lambda definition, _, __: Column(types.String(255), **definition),
            'json': lambda definition, _, __: Column(types.JSON, **definition),
            'many2one': lambda definition, related_model_name, on_delete: (
                Column(
                    types.Integer,
                    ForeignKey(
                        f'{related_model_name}.{FIELD_NAME.ID}',
                        ondelete= (
                            on_delete
                            .replace('_', ' ')
                            .upper()
                        )
                    ),
                    **definition,
                )
            ),
        }
