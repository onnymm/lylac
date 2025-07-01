from ._base_base_lylac import BaseBaseLylac
from ._base_structure import BaseStructure

class BaseValidations():
    _main: BaseBaseLylac
    _strc: BaseStructure

    def initialize_model_validations(
        self,
        model_name: str,
    ) -> None:
        ...

    def drop_model_validations(
        self,
        model_name: str,
    ) -> None:
        ...
