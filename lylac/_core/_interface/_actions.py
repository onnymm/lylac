from ..._contexts._actions import ActionCallback
from ..._module_types import ModelName

class Actions_Interface():

    def register_action(
        self,
        model_name: ModelName,
        action_name: str,
        action_callback: ActionCallback,
    ) -> None:
        ...

    def run_action(
        self,
        token: str,
        model_name: ModelName,
        action_name: str,
        record_id: int,
    ) -> None:
        ...
