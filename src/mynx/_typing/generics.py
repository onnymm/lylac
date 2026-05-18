from typing import Callable
from typing import Union
from typing import TYPE_CHECKING
from .aliases import ModelClass
from .literals import InitialModels
from .type_parameters import _A
from .type_parameters import _F
from .type_parameters import _M
from .type_parameters import _S
from .type_parameters import _T

if TYPE_CHECKING:
    from .definitions import RecordSchema
    from .models import _BasicRecord

ModelName = InitialModels | _M

ItemOrList = _T | list[_T]

Array = _T | list[_T] | tuple[_T]

_ModelIndex = dict[ModelName[_M], 'ModelClass']

MaybeNone = _T | None

Schema = Union[_S | 'RecordSchema']

EngineHub = dict[ModelName[_M], dict[str, _T]]

FunctionDecorator = Callable[[_F], _F]

_Record = Union['_BasicRecord', _A]

_Records = list[_Record[_A]]
