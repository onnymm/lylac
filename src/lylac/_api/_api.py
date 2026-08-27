from typing import Generic
from typing import TYPE_CHECKING
from .._engines import ActionEngine
from .._engines import AutomationsEngine
from .._engines import ComputeEngine
from .._engines import PoliciesEngine
from .._engines import ServerTasksEngine
from .._engines import UserEnvEngine
from .._engines import ValidationEngine
from .._typing.type_parameters import _M
from ._interfaces import _Interface_Actions
from ._interfaces import _Interface_Automations
from ._interfaces import _Interface_Compute
from ._interfaces import _Interface_CRUD
from ._interfaces import _Interface_ServerTasks
from ._interfaces import _Interface_UserEnv
from ._interfaces import _Interface_Validations
from ._interfaces import _Interface_Policies

if TYPE_CHECKING:
    from .._main import Lylac
    from .._orchestrator import CRUD

class _MainAPI(Generic[_M]):
    automations: _Interface_Automations[_M]
    compute: _Interface_Compute[_M]
    actions: _Interface_Actions[_M]
    compute: _Interface_Compute[_M]
    policies: _Interface_Policies[_M]
    server_tasks: _Interface_ServerTasks[_M]
    env: _Interface_UserEnv[_M]
    crud: _Interface_CRUD[_M]

    def __init__(
        self,
        automations: AutomationsEngine[_M],
        validations: ValidationEngine[_M],
        actions: ActionEngine[_M],
        compute: ComputeEngine[_M],
        policies: PoliciesEngine[_M],
        server_tasks: ServerTasksEngine[_M],
        user_env: UserEnvEngine[_M],
        crud: 'CRUD[_M]',
        main: Lylac[_M],
    ) -> None:

        self.automations = _Interface_Automations[_M](automations)
        self.validations = _Interface_Validations[_M](validations)
        self.actions = _Interface_Actions[_M](actions)
        self.compute = _Interface_Compute[_M](compute, main)
        self.policies = _Interface_Policies[_M](policies)
        self.server_tasks = _Interface_ServerTasks[_M](server_tasks)
        self.env = _Interface_UserEnv[_M](user_env)
        self.crud = _Interface_CRUD[_M](crud)
        self._main = main
