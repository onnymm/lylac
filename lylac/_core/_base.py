from ._submodules import (
    BaseAutomations,
    BaseCompiler,
    BaseIndex,
    BaseStructure,
    BaseValidations,
)
from ._submodules import BaseBaseLylac

class _Lylac(BaseBaseLylac):

    _automations: BaseAutomations
    _compiler: BaseCompiler
    _index: BaseIndex
    _strc: BaseStructure
    _validations: BaseValidations
