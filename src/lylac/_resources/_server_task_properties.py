from typing import Generic
from .._typing.callables import ServerTaskCallback
from .._typing.type_parameters import _M

from dataclasses import dataclass

@dataclass(slots= True)
class ServerTaskProperties(Generic[_M]):
    name: str
    callback: ServerTaskCallback[_M]
