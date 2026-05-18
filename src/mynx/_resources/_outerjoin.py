from dataclasses import dataclass
from sqlalchemy.sql.elements import BinaryExpression
from .._typing.aliases import ModelClass

@dataclass(slots= True, frozen= True)
class OuterJoin:
    model: ModelClass
    on: BinaryExpression
