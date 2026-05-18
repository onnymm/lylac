from typing import Generic
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.elements import BooleanClauseList
from ..._typing.structures import CriteriaStructure
from ..._typing.structures import TripletStructure
from ..._typing.type_parameters import _M

class Contract_WhereContext(Generic[_M]):

    def build_conditions(
        self,
        search_criteria: CriteriaStructure,
    ) -> BinaryExpression | BooleanClauseList:
        ...

    def create_binary_expression(
        self,
        triplet: TripletStructure,
    ) -> BinaryExpression:
        ...
