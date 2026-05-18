from dataclasses import dataclass
from typing import Any
from typing import Iterable

@dataclass(slots= True, frozen= True)
class ModelColumnBasicAtts:
    nullable: bool
    unique: bool
    default: Any = None

    def keys(self) -> Iterable[str]:
        return type(self).__slots__

    def __getitem__(self, key: str):
        return getattr(self, key)
