from typing import (
    Any,
    Callable,
    Generic,
    Literal,
    TypedDict,
)
from pydantic import BaseModel
from ..._module_types import (
    _T,
    RecordData,
)

# Método de validación
ValidationMethod = Literal['record', 'list']

# Tipos de validación
_IndividualData = RecordData
_GroupData = list[RecordData]

# Argumentos de entrada de función de validación
class _ValidationOnCreateArgs(BaseModel, Generic[_T]):

    model_name: str
    """Nombre del modelo."""
    model_id: int
    """ID del modelo."""
    data: _T
    """Datos del o los registros."""

class _ValidationOnCreateParams(TypedDict, Generic[_T]):

    callback: _T
    """Función de validación en la creación de registros."""
    method: ValidationMethod
    """
    Método de ejecución de validación.
    >>> Literal['record', 'list']
    """
    message: str
    """Mensaje de error arrojado si los datos evaluados no son válidos."""

# Tipado de funciones
_IndividualValidationOnCreateCallback = Callable[[ _ValidationOnCreateArgs[_IndividualData] ], Any]
_GroupValidationOnCreateCallback = Callable[[ _ValidationOnCreateArgs[_GroupData] ], Any]

class Validation():

    class Create():

        class Mixed():

            Callback = _IndividualValidationOnCreateCallback | _GroupValidationOnCreateCallback
            """
            ### Función de validación
            Función de validación en creación de nuevos registros.
            >>> def some_validation(
            >>>     params: Validation.Create.Mixed.Args,
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnCreateArgs[_IndividualData | _GroupData]
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación en creación de nuevos registros.
            >>> class _ValidationOnCreateArgs(BaseModel):
            >>>     model_name: str
            >>>     model_id: int
            >>>     data: _IndividualData | _GroupData
            """
            Params = _ValidationOnCreateParams[Callback]
            """
            ### Parámetros de validación de creación
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnCreateParams(TypedDict):
            >>>     # Función de validación en la creación de registros.
            >>>     callback: Validation.Create.Mixed.Callback
            >>>     # Método de ejecución de validación.
            >>>     method: _ValidationMethod
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

        class Individual():

            Callback = _IndividualValidationOnCreateCallback
            """
            ### Función de validación
            Función de validación en creación de un nuevo registro.
            >>> def some_validation(
            >>>     params: Validation.Create.Individual.Args,
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnCreateArgs[_IndividualData]
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación individual en creación de un
            nuevo registro.
            >>> class _ValidationOnCreateArgs(BaseModel):
            >>>     model_name: str
            >>>     model_id: int
            >>>     data: _IndividualData
            """
            Params = _ValidationOnCreateParams[Callback]
            """
            ### Parámetros de validación de creación individual
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnCreateParams(TypedDict):
            >>>     # Función de validación en la creación de registros.
            >>>     callback: Validation.Create.Individual.Callback
            >>>     # Método de ejecución de validación.
            >>>     method = 'record'
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

        class Group():

            Callback = _GroupValidationOnCreateCallback
            """
            ### Función de validación
            Función de validación en creación de nuevos registros.
            >>> def some_validation(
            >>>     params: Validation.Create.Group.Args,
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnCreateArgs[_GroupData]
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación grupal en creación de nuevos registros.
            >>> class _ValidationOnCreateArgs(BaseModel):
            >>>     model_name: str
            >>>     model_id: int
            >>>     data: _GroupData
            """
            Params = _ValidationOnCreateParams[Callback]
            """
            ### Parámetros de validación de creación individual
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnCreateParams(TypedDict):
            >>>     # Función de validación en la creación de registros.
            >>>     callback: Validation.Create.Group.Callback
            >>>     # Método de ejecución de validación.
            >>>     method: 'list'
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

class _ValidationsPerTransaction(TypedDict):
    create: list[Validation.Create.Mixed.Params]

# Núcleo de validaciones
ValidationsHub = dict[str, _ValidationsPerTransaction]

# Mensajes a mostrar
class ErrorToShow(TypedDict):
    """
    ### Error a mostrar en validación fallida
    Error a mostrar una cuando una validación arroja datos que no cumplen con ésta.
    >>> {
    >>>     'value': ...,
    >>>     'message': '...',
    >>>     'data': {...}
    >>> }
    """
    value: Any
    """Datos que no cumplen con la validación."""
    message: str
    """Mensage que indica la razón de la validación fallida."""
    data: RecordData | list[RecordData]
    """Datos del o los objetos que no cumplieron con la validación."""
