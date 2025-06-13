from ...._core import _Lylac
from .._module_types import ValidationsHub

class _BaseValidations():
    _main: _Lylac
    _hub: ValidationsHub = {}
    _active: bool = False

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
