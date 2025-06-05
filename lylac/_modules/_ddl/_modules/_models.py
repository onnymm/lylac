from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.types import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    Time,
    LargeBinary,
)
from ...._constants import MODEL_NAME
from ...._data import default_field_template
from ...._module_types import (
    ModelRecord,
    FieldAttributes,
    NewRecord,
    TType,
)
from .._module_types import ColumnGenerator
from ._base import (
    _BaseDDLManager,
    _BaseModels,
)

class _Models(_BaseModels):

    build_column: dict[TType, ColumnGenerator]
    """
    ### Construcción de columna
    Este mapa de métodos construye una columna tipada para un modelo de SQLALchemy.
    Uso:
    >>> # Creación de un campo tipo 'integer'
    >>> field = NewField(...)
    >>> column = self.build_column['integer'](field)
    """

    atts: list[str] = [
        'nullable',
        'default',
        'unique',
    ]
    """
    ### Atributos de columna
    Esta lista declara los atributos que se pueden especificar dinámicamente en la
    creación de columnas dinámica.
    """

    def __init__(
        self,
        instance: _BaseDDLManager,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance
        # Asignación de la instancia principal
        self._main = instance._main
        # Asignación de modelo base
        self._base = instance._main._base

        # Inicialización de mapa de funciones
        self._initialize_column_builder()

    def create_model(
        self,
        model_name: str,
    ) -> type[DeclarativeBase]:
        """
        ### Creación de modelo
        Este método crea un nuevo modelo de SQLAlchemy con sus campos base y lo
        registra en la estructura de tablas de la instancia principal.
        """

        # Inicialización del modelo
        class model(self._base):
            __tablename__ = model_name

        # Registro del modelo en la estructura de SQLAlchemy
        self._main._strc.register_table(model)

        # Se retorna el modelo para ser usado por otros métodos
        return model

    def delete_model(
        self,
        model_name: str,
    ) -> None:
        """
        ### Eliminar modelo
        Este método elimina un modelo de SQLAlchemy del registro de Base y del mapa de tablas
        """

        # Se obtiene el esquema del registro de Base
        table_scheme = self._base.metadata.tables[model_name]

        # Se elimina el esquema de los modelos heredados de Base
        self._base.metadata.remove(table_scheme)

        # Se elimina el modelo de los registros del mapa de modelos
        self._main._strc.unregister_table(model_name)

    def add_field_to_model(
        self,
        table_model: type[DeclarativeBase],
        field: FieldAttributes,
    ) -> None:
        """
        ### Añadir campo al modelo
        Este método añade un nuevo campo al modelo de SQLAlchemy provisto.
        """

        # Creación de la instancia a ser añadida
        field_instance = self.build_column[field.ttype](field)

        # Se añade la instancia de campo como atributo del modelo
        setattr(
            table_model,
            field.field_name,
            field_instance,
        )

        # Se registra la instancia la modelo en el esquema de SQLAlchemy
        class_mapper(table_model).add_property(field.field_name, field_instance)

    def build_field_atts(
        self,
        params: ModelRecord.BaseModelField,
    ) -> FieldAttributes:
        """
        ### Construcción de atributos de campo
        Construcción de atributos para usarse en nuevos campos de modelo de SQLAlchemy.
        """

        # Obtención del nombre del modelo vinculado
        table_model: str = self._main.get_value(MODEL_NAME.BASE_MODEL, params['model_id'], 'model')

        # Creación de los parámetros para ser usados en las automatizaciones
        field_atts = FieldAttributes(
            field_name= params['name'],
            table_model= self._main._models.get_table_model(table_model),
            label= params['label'],
            ttype= params['ttype'],
            nullable= params['nullable'],
            is_required= params['is_required'],
            default= self._parse_default_value(params),
            unique= params['unique'],
            help_info= params['help_info'],
            related_model_id= params['related_model_id'],
        )

        return field_atts

    def _parse_default_value(
        self,
        params: ModelRecord.BaseModelField,
    ) -> (int | float | str | bool | None):

        # Si no existe valor por defecto se termina la ejecución
        if params['default_value'] is None:
            return None

        # Obtención del tipo de dato´y valor
        ttype = params['ttype']
        value = params['default_value']

        # Si el valor es booleano
        if ttype == 'boolean':
            if value == 'true':
                return True
            else:
                return False
        # Si el valor es entero
        elif ttype == 'integer':
            return int(value)
        # Si el valor es flotante
        elif ttype == 'float':
            return float(value)
        # El valor se retorna en formato de cadena de texto
        else:
            return value

    def _initialize_column_builder(
        self
    ) -> None:

        # Inicialización de mapa de funciones
        self.build_column = {
            'integer': lambda field: Column(Integer, **self._build_field_kwargs(field)),
            'char': lambda field: Column(String(255), **self._build_field_kwargs(field)),
            'float': lambda field: Column(Float, **self._build_field_kwargs(field)),
            'boolean': lambda field: Column(Boolean, **self._build_field_kwargs(field)),
            'date': lambda field: Column(Date, **self._build_field_kwargs(field)),
            'datetime': lambda field: Column(DateTime, **self._build_field_kwargs(field)),
            'time': lambda field: Column(Time, **self._build_field_kwargs(field)),
            'file': lambda field: Column(LargeBinary, **self._build_field_kwargs(field)),
            'text': lambda field: Column(Text, **self._build_field_kwargs(field)),
            'selection': lambda field: Column(String, **self._build_field_kwargs(field)),
            'many2one': lambda field: Column(
                Integer,
                ForeignKey(f'{self._get_table_name(field.related_model_id)}.id'),
                **self._build_field_kwargs(field)
            ),
        }

    def _build_field_kwargs(
        self,
        field: FieldAttributes
    ) -> dict:

        # Inicialización de los kwargs del campo
        field_kwargs = {}

        # Iteración por cada mapeo de atributos
        for att in self.atts:
            # Obtención del valor declarado en el objeto entrante
            field_att_value = getattr(field, att)
            # Si existe un valor declarado...
            if field_att_value is not None:
                # Se añade éste a los kwargs del campo
                field_kwargs[att] = field_att_value

        # Retorno de los kwargs del campo
        return field_kwargs

    def _get_table_name(
        self,
        model_id: int
    ) -> str:

        # Obtención del nombre de la tabla
        table_name: str = self._main.get_value(MODEL_NAME.BASE_MODEL, model_id, 'name')

        return table_name
