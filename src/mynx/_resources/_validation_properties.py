from dataclasses import dataclass
from typing import Generic
from typing import Optional
from .._typing.callables import ValidationCallback
from .._typing.generics import ItemOrList
from .._typing.generics import ModelName
from .._typing.literals import DMLTransaction
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R

@dataclass(slots= True)
class ValidationProperties(Generic[_M, _R]):
    transaction: ItemOrList[DMLTransaction]
    callback: ValidationCallback[_M, _R]
    message: str
    model_name: Optional[ ModelName[_M] ] = None
