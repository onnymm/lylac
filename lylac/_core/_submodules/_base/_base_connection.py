from typing import Literal
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.sql.selectable import (
    Select,
    TypedReturnsRows,
)
from ...._module_types import (
    _T,
    DBCredentials,
)

class BaseConnection():

    def execute(
        self,
        statement: Select[_T] | TypedReturnsRows[_T],
        commit: bool = False,
    ) -> CursorResult[_T]:
        ...

    def create_connection(
        self,
        credentials: DBCredentials | str | Literal['env'],
    ) -> Engine:
        ...
