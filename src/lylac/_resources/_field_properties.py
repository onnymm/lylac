from dataclasses import dataclass
from typing import Generic
from typing import Optional
from .._typing.generics import ModelName
from .._typing.literals import TTypeName
from .._typing.type_parameters import _M

@dataclass(slots= True, frozen= True)
class FieldProperties(Generic[_M]):
    name: str
    ttype: TTypeName
    is_computed: bool
    related_model_name: Optional[ ModelName[_M] ]
    related_field: Optional[ str ]
