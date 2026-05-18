from dataclasses import dataclass
from typing import Generic
from .._constants import FIELD_NAME
from .._typing.callables import AutomationCallback
from .._typing.generics import ModelName
from .._typing.structures import CriteriaStructure
from .._typing.structures import FieldReadDeclaration
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R

@dataclass
class AutomationProperties(Generic[_M, _R]):
    execute_only_when: CriteriaStructure
    callback: AutomationCallback[_M, _R]
    model_name: ModelName[_M]
    fields: tuple[FieldReadDeclaration] = (FIELD_NAME.ID,)
