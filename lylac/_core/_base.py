from ._submodules import (
    BaseAuth,
    BaseAutomations,
    BaseCompiler,
    BaseIndex,
    BaseStructure,
    BaseValidations,
)
from ._submodules import BaseBaseLylac

class _Lylac(BaseBaseLylac):

    _auth: BaseAuth
    _automations: BaseAutomations
    _compiler: BaseCompiler
    _index: BaseIndex
    _strc: BaseStructure
    _validations: BaseValidations
