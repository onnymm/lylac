from typing import (
    Callable,
    Generic,
    Optional,
    TypedDict,
    TypeVar,
    Union,
)
from pydantic import BaseModel
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
from ._base import (
    RecordValue,
    Transaction,
    TType,
)
from sqlalchemy.orm.decl_api import DeclarativeBase

# Dato genérico
_T = TypeVar("_T")
"""
### Tipo de dato genérico
Tipo de dato genérico usado para declarar entradas y salidas dinámicas en
funciones:
>>> def do_something(param: _T) -> _T:
>>>     ...
>>> a = do_something(5) # `a` se tipa como entero
>>> b = do_something('Onnymm') # `b` se tipa como cadena de texto
>>> c = do_something(True) # `c` se tipa como booleano

Este tipo de dato también se puede usar para transformación de tipos de dato de
entradas y salidas:
>>> def get_first_item(iterable_object: list[_T]) -> _T:
>>>     return iterable_object[0]
>>> a = get_first_item([1, 2, 3]) # `a` se tipa como entero
>>> b = get_first_item(['uno', 'dos', 'tres']) # `b` se tipa como cadena de texto
>>> c = get_first_item([True, False]) # `c` se tipa como booleano
"""

class FieldProperties(TypedDict):
    """
    ### Propiedades de campo
    Diccionario que almacena el tipo de dato y la relación de un campo.
    >>> {
    >>>     'many2one',
    >>>     'base.users',
    >>> }
    """
    ttype: TType
    relation: str

class ModelMap(TypedDict):
    """
    ### Mapa de atributos de modelo
    Este tipo de dato almacena la información básica que define la estructura de un
    modelo almacenado en una instancia Lylac.
    >>> {
    >>>     'model': <ModelInstance>,
    >>>     'fields': {
    >>>         'id': {
    >>>             'ttype': 'integer',
    >>>             'relation': None,
    >>>         },
    >>>         ...
    >>>         'write_uid': {
    >>>             'ttype': 'many2one',
    >>>             'relation': 'base.users',
    >>>         },
    >>>     },
    >>> }
    """
    model: type[DeclarativeBase]
    """Modelo SQLAlchemy de la tabla"""
    fields: dict[str, FieldProperties]
    """
    Diccionario que almacena el tipo de dato y la relación de un campo.
    >>> {
    >>>     'many2one',
    >>>     'base.users',
    >>> }
    """

class DataPerRecord(BaseModel, Generic[_T]):
    id: int
    """ID del registro."""
    record_data: _T
    """Datos del registro en la base de datos."""
    transaction: Optional[Transaction] = None
    """Tipo de transacción que accionó la automatización en curso."""

class DataPerTransaction(BaseModel, Generic[_T]):
    ids: list[int]
    """ID de los registros."""
    records_data: list[_T]
    """Datos de los registros en la base de datos."""
    transaction: Transaction
    """Tipo de transacción que accionó la automatización en curso."""

class BaseRecord(TypedDict):
    id: int
    name: str
    create_date: str
    write_date: str

class ModelRecord():

    class BaseModel(BaseRecord):
        model: int
        label: str
        description: str

    class BaseModelField(BaseRecord):
        model_id: int
        label: str
        ttype: TType
        nullable: bool
        is_required: bool
        default_value: str | None
        unique: bool
        help_info: str | None
        related_model_id: int | None

    class BaseModelFieldSelection(BaseRecord):
        field_id: int
        label: str

class FieldAttributes(BaseModel):
    """
    ### Nuevo campo
    Modelo base para crear objetos de campo nuevo para usarse en automatizaciones
    de creación de modelos de SQLAlchemy, tablas de base de datos y sus respectivos
    campos.

    ----
    #### Atributos disponibles
    - `field_name`: Nombre del campo.
    - `table_model`: Modelo de la tabla.
    - `label`: Etiqueta de la tabla.
    - `ttype`: Tipo de dato del campo.
    - `nullable`: Puede ser nulo.
    - `is_required`: Es requerido.
    - `default`: Valor predeterminado.
    - `unique`: Único.
    - `help_info`: Información de ayuda del campo.
    - `related_model_id`: ID de modelo relacionado.
    """
    field_name: str
    """Nombre del campo."""
    table_model: type[DeclarativeBase]
    """Modelo de la tabla."""
    label: str
    """Etiqueta de la tabla."""
    ttype: TType
    """Tipo de dato del campo."""
    nullable: bool =  False
    """Puede ser nulo."""
    is_required: bool = False
    """Es requerido."""
    default: Optional[RecordValue] = None
    """Valor predeterminado."""
    unique: bool = False
    """Único."""
    help_info: Optional[str] = None
    """Información de ayuda del campo."""
    related_model_id: int | None = None
    """ID de modelo relacionado."""

DataBaseDataType = Union[
    type[Integer],
    type[String],
    type[Float],
    type[Boolean],
    type[Date],
    type[DateTime],
    type[Time],
    type[Text],
    type[LargeBinary],
]
"""
Tipo de dato de atributos de modelos de SQLAlchemy.
"""

AutomationTemplate = Callable[[DataPerRecord | DataPerTransaction], None]
"""
### Función de automatización
Estructura que debe tener una función para registrarse como automatización
>>> def some_automation(params: DataPerRecord[Any]) -> None:
>>>     ...
"""

# Lista de diccionario serializable a JSON
SerializableDict = list[dict[str, RecordValue]]
"""
### Diccionario convertible en JSON
Esta estructura está habilitada para ser convertida a JSON ya que no contiene
objetos que no sean legibles por el serializador de FastAPI.
"""
