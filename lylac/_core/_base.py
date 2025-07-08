from ._submodules import (
    BaseAccess,
    BaseAuth,
    BaseAutomations,
    BaseCompiler,
    BaseIndex,
    BaseSelect,
    BaseStructure,
    BaseValidations,
)
from ._submodules import BaseBaseLylac

class _Lylac(BaseBaseLylac):
    _access = BaseAccess
    _auth: BaseAuth
    _automations: BaseAutomations
    _compiler: BaseCompiler
    _index: BaseIndex
    _select: BaseSelect
    _strc: BaseStructure
    _validations: BaseValidations
