from typing import (
    Any,
    Callable,
)
from sqlalchemy.orm.properties import MappedColumn
from ..._module_types import FieldAttributes

ColumnGenerator = Callable[[FieldAttributes], MappedColumn[Any]]
