from dataclasses import dataclass
from typing import Generic
from .._typing.callables import ActionCallback
from .._typing.generics import ModelName
from .._typing.type_parameters import _M

@dataclass(slots= True)
class ActionProperties(Generic[_M]):
    model_name: ModelName[_M]
    name: str
    callback: ActionCallback[_M]
    fields: tuple[str] = tuple()
