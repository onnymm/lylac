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

class TableBaseData(BaseModel):
    NAME: str
    MODEL: str

class DataPerRecord(BaseModel, Generic[_T]):
    id: int
    """ID del registro."""
    record_data: _T
    """Datos del registro en la base de datos."""
    transaction: Optional[Transaction] = None
    """Tipo de transacción que accionó la automatización en curso."""

class DataPerTransaction(BaseModel, Generic[_T]):
    ids: list[int]
    records_data: list[_T]
    transaction: Transaction

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

class NewField(BaseModel):
    """
    ### Nuevo campo
    Modelo base para crear objetos de campo nuevo para usarse en automatizaciones
    de creación de modelos de SQLAlchemy, tablas de base de datos y sus respectivos
    campos.
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
    default_value: Optional[RecordValue] = None
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

AutomationTemplate = Callable[[DataPerRecord | DataPerTransaction], None]

# Lista de diccionario serializable a JSON
SerializableDict = list[dict[str, RecordValue]]
"""
### Diccionario convertible en JSON
Esta estructura está habilitada para ser convertida a JSON ya que no contiene
objetos que no sean legibles por el serializador de FastAPI.
"""
