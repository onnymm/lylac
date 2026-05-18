from typing import Generic
from typing import TYPE_CHECKING
from sqlalchemy.engine import Connection
from ..._resources import DatabaseMetadata
from ..._resources import ModelsBearer
from ..._typing.type_parameters import _M

if TYPE_CHECKING:
    from ..._engines import AutomationsEngine
    from ..._engines import ValidationEngine
    from ..._engines import ActionEngine
    from ..._main import ComputeEngine

class Contract_ExecutionContext(Generic[_M]):
    conn: Connection
    database_metadata: DatabaseMetadata
    models_bearer: ModelsBearer
    compute: ComputeEngine[_M]
    uid: int
    automations: AutomationsEngine[_M]
    validations: ValidationEngine[_M]
    actions: ActionEngine[_M]

    def __init__(
        self,
        uid: int,
        conn: Connection,
        models_bearer: ModelsBearer[_M],
        database_metadata: DatabaseMetadata[_M],
        automations: AutomationsEngine[_M],
        compute: ComputeEngine[_M]
    ) -> None:
        ...

    def resolve_uid(
        self,
        uid: int | str
    ) -> int | None:
        ...
