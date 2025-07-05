from ..._module_types import Transaction

class BaseAccess():
    _active: bool

    def initialize(
        self,
    ) -> None:
        ...

    def check_permission(
        self,
        user_id: int,
        transaction: Transaction,
    ) -> None:
        ...
