from ._submodules import (
    BaseAutomations,
    BaseIndex,
    BaseStructure,
    BaseValidations,
)
from ._submodules import BaseBaseLylac

class _Lylac(BaseBaseLylac):

    _automations: BaseAutomations
    _index: BaseIndex
    _strc: BaseStructure
    _validations: BaseValidations
