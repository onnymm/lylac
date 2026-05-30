from dataclasses import dataclass
from .._typing.structures import _ExpansionSpec

@dataclass(slots= True)
class FieldExpansionSpecs:
    name: str
    spec: _ExpansionSpec
    alias: str
