from ..._constants import MESSAGES
from ..._module_types import Transaction

class Access_Interface():

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
