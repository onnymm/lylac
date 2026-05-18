from dataclasses import dataclass
from typing import Generic
from .._typing.aliases import ModelClass
from .._typing.generics import ModelName
from .._typing.type_parameters import _M

@dataclass(slots= True, frozen= True)
class ModelProperties(Generic[_M]):
    name: ModelName[_M]
    model: ModelClass
