from typing import Any
from typing import Callable
from typing import Optional
from typing import TYPE_CHECKING
from sqlalchemy.engine import Connection
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm import MappedColumn
from .literals import OnDeleteOption
from .type_parameters import _M
from .type_parameters import _T
from .type_parameters import _R

if TYPE_CHECKING:
    from .._contexts import ActionContext
    from .._contexts import AutomationContext
    from .._contexts import ComputeContext
    from .._contexts import ExecutionContext
    from .._contexts import ValidationContext
    from .._contexts import ServerTaskContext
    from .._contexts import TransactionContext
    from .._orchestrator import CRUD
    from .._resources import ModelColumnBasicAtts

ExecutionCallback = Callable[[Connection], _T]

ComputeFieldFn = Callable[['ComputeContext[_M]'], InstrumentedAttribute]

CaptureComputeCallback = Callable[['ComputeContext[_M]'], 'ComputeContext[_M]']

AggFunc = Callable[[InstrumentedAttribute], InstrumentedAttribute]
"""
### Función de agregación
Función que permite declarar la agregación de un campo de tipo `one2many` o
`many2many`.
"""

CaptureCreatedRecordID = Callable[[int], None]

from typing import Callable

from typing import TYPE_CHECKING

AutomationCallback = Callable[['AutomationContext[_M, _R]'], None]

CRUD_Operation = Callable[['CRUD[_M]'], Any]

CaptureRecordID = Callable[[int], 'CRUD_Operation[_M]']

ColumnBuilder = Callable[['ModelColumnBasicAtts', Optional[str], Optional[OnDeleteOption]], MappedColumn]

TransactionCallback = Callable[[Connection], _T]

ValidationCallback = Callable[['ValidationContext[_M, _R]'], None]

ActionCallback = Callable[['ActionContext[_M]'], None]

CaptureIDsAfterDeletionFn = Callable[[], None]

ServerTaskCallback = Callable[['ServerTaskContext[_M]'], None]

ExecutableTransactionCallback = Callable[['TransactionContext[_M]'], None]

LazyResolver = Callable[['ExecutionContext[_M]'], Any]
