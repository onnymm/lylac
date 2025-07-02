from ._base_base_lylac import BaseBaseLylac
from ._base_structure import BaseStructure
from ..._module_types import RecordData

class BaseValidations():
    _main: BaseBaseLylac
    _strc: BaseStructure

    def initialize_model_validations(
        self,
        model_name: str,
    ) -> None:
        ...

    def run_validations_on_create(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> None:
        ...

    def drop_model_validations(
        self,
        model_name: str,
    ) -> None:
        ...
