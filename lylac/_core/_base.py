from ._submodules import (
    BaseIndex,
    BaseStructure,
    BaseValidations,
)
from ._submodules import BaseBaseLylac

class _Lylac(BaseBaseLylac):

    _strc: BaseStructure
    _index: BaseIndex
    _validations: BaseValidations
