from ...._module_types import ModelName

class _BaseAutomations():

    def register_model(
        self,
        model_name: ModelName
    ) -> None:
        ...
