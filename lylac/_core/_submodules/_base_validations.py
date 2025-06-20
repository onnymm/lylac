from ._base_base_lylac import BaseBaseLylac

class BaseValidations():
    _main: BaseBaseLylac

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
