from sqlalchemy.orm import class_mapper
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
from ..._core import _BaseLylac
# from ...data._base_fields import preset_fields
from ..._module_types import (
    DataPerRecord,
    ModelRecord,
    NewField,
    DataBaseDataType,
    TType,
)
from ._modules import (
    _BaseDDLManager,
)
from ._modules import (
    _Automations,
    _BaseDDLManager,
    _Database,
    _Models,
    _Reset
)

class DDLManager(_BaseDDLManager):

    _class_ttype: dict[TType, DataBaseDataType] = {
        'integer': Integer,
        'char': String(255),
        'float': Float,
        'boolean': Boolean,
        'date': Date,
        'datetime': DateTime,
        'time': Time,
        'file': LargeBinary,
        'text': Text,
        'selection': String(255),
    }
    """
    ### Mapa de tipos de dato
    Este mapa representa los tipos de dato en SQL por medio de SQLAlchemy y sus
    representaciones en cadena de texto.
    """


    def __init__(
        self,
        instance: _BaseLylac,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Creación del submódulo para operaciones en la base de datos
        self._db = _Database(self)

        # Creación del submódulo para operaciones en los modelos de SQLAlchemy
        self._model = _Models(self)

        # Creación del submódulo para operaciones de reseteo de base de datos
        self._reset = _Reset(self)

        # Creación del submódulo de automatizaciones
        self._automations = _Automations(self)

    def _create_table(
        self,
        name: str,
        sync_to_db: bool = True,
    ) -> None:
        """
        ### Creación de tabla
        Este método realiza la declaración de un nuevo modelo de SQLAlchemy y realiza
        la creación de su respectiva tabla en la base de datos.
        """

        # Inicialización del modelo
        class _GenericModel(self._main._base):
            __tablename__ = name

        if sync_to_db:
            # Se crea el modelo como tabla en la base de datos
            _GenericModel.__table__.create(self._main._engine)

        # Registro del modelo en la estructura de SQLAlchemy
        self._main._strc.register_table(_GenericModel)

    def _add_column_to_model(
        self,
        params: NewField,
    ) -> None:

        # Inicialización de la instancia de la columna
        new_column = self._model.build_column[params.ttype](params)

        # Se añade la instancia de columna como atributo de la tabla
        setattr(
            params.table_model,
            params.field_name,
            new_column,
        )

        # Se registra la columna a instancia de la tabla en el esquema de SQLAlchemy
        class_mapper(params.table_model).add_property(params.field_name, new_column)

    def _add_column_to_db(
        self,
        params: NewField,
    ) -> None:

        # Ejecución del SQL para creación de columna en la tabla
        self._db.add_column(params)

    def _parse_default_value(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField],
    ) -> (int | float | str | bool | None):
        
        if params.record_data['default_value'] is None:
            return None

        # Obtención del tipo de dato´y valor
        ttype = params.record_data['ttype']
        value = params.record_data['default_value']

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

    def _prepare_column_data(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField],
    ) -> NewField:

        # Obtención del nombre del modelo vinculado
        table_model_model: str = self._main.get_value('base.model', params.record_data['model_id'], 'model')

        # Creación de los parámetros para ser usados en las automatizaciones
        new_field = NewField(
            field_name= params.record_data['name'],
            table_model= self._main._models.get_table_model(table_model_model),
            label= params.record_data['label'],
            ttype= params.record_data['ttype'],
            nullable= params.record_data['nullable'],
            is_required= params.record_data['is_required'],
            default_value= self._parse_default_value(params),
            unique= params.record_data['unique'],
            help_info= params.record_data['help_info'],
            related_model_id= params.record_data['related_model_id'],
        )

        return new_field
