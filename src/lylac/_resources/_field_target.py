from dataclasses import dataclass
from .._typing.callables import ComputeFieldFn
from .._typing.literals import TTypeName

@dataclass(slots= True, frozen= True)
class FieldTarget():
    complete_name: str
    label: str | None
    ttype: TTypeName
    computation_callback: ComputeFieldFn | None = None
