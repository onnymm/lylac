from dataclasses import dataclass
from typing import Any
from .._typing.literals import LiteralTarget

@dataclass
class Notification:
    event: str
    target: LiteralTarget | list[int]
    payload: dict[str, Any]
