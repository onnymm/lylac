from typing import Any
from typing import Callable
from typing import TypeVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import _DefaultFields
    from .models import RecordShape
    from .generics import _Record
    from .definitions import RecordSchema

_T = TypeVar('_T')
_M = TypeVar('_M', bound= str)
_F = TypeVar('_F', bound= Callable)
_V = TypeVar('_V', bound= tuple[Any, ...])
_R = TypeVar('_R', default= '_Record')
_S = TypeVar('_S', bound= 'RecordSchema')
_A = TypeVar('_A', bound= 'RecordShape', default= '_DefaultFields')
