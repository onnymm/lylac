from typing import Generic
from typing import Optional
from .._typing.callables import PolicyCallback
from .._typing.generics import ScalarOrIterable
from .._typing.generics import ModelName
from .._typing.literals import DMLTransaction
from .._typing.type_parameters import _M

from dataclasses import dataclass

@dataclass(slots= True)
class PolicyProperties(Generic[_M]):
    transaction: ScalarOrIterable[DMLTransaction]
    callback: PolicyCallback[_M]
    message: str
    model_name: Optional[ModelName[_M]] = None
