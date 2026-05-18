from typing import ClassVar
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.selectable import FromClause
from typing import Literal
from typing import overload
from .generics import MaybeNone

class Many2One:
    @overload
    def __getitem__(self, name: Literal[0]) -> MaybeNone[int]: ...
    @overload
    def __getitem__(self, name: Literal[1]) -> MaybeNone[str]: ...

class Many2ManyRelation:
    __table__: ClassVar[FromClause]
    __tablename__: ClassVar[str]
    x: Mapped[int]
    y: Mapped[int]
