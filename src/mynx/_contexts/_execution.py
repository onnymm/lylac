from typing import Any
from typing import Generic
from typing import TYPE_CHECKING
from sqlalchemy.engine import Connection
from .._resources import DatabaseMetadata
from .._resources import ModelDataIndex
from .._resources import ModelsBearer
from .._resources import UserEnv
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._engines import ActionEngine
    from .._engines import AutomationsEngine
    from .._engines import ComputeEngine
    from .._engines import ValidationEngine
    from .._orchestrator import CRUD
from .._contexts.engines import BaseContext

class ExecutionContext(Generic[_M], BaseContext[_M]):

    def __init__(
        self,
        session_uuid: str,
        crud: CRUD,
        uid: int | str,
        conn: Connection,
        models_bearer: ModelsBearer[_M],
        database_metadata: DatabaseMetadata[_M],
        compute: 'ComputeEngine[_M]',
        automations: 'AutomationsEngine[_M]',
        validations: 'ValidationEngine[_M]',
        actions: 'ActionEngine[_M]',
        user_env_engine: UserEnv[_M],
    ) -> None:

        # Inicialización de entorno de usuario
        user_env = UserEnv(self, user_env_engine._resolvers)

        self.session_uuid = session_uuid
        self._crud = crud
        self._model_data_index = ModelDataIndex(conn)
        self._uid = self.resolve_uid(uid)
        self.conn = conn
        self.models_bearer = models_bearer
        self.database_metadata = database_metadata
        self.compute = compute
        self.automations = automations
        self.validations = validations
        self.actions = actions
        self._execution_ctx = self
        self._env = user_env

    @property
    def uid(
        self,
    ) -> int:
        """
        ID del usuario que ejecuta la transacción.
        """

        # Obtención de la ID del usuario en la ejecución
        uid = self._uid

        return uid

    def get_resource_id(
        self,
        name: str,
    ) -> int:

        # Obtención de la ID de la referencia de recurso
        resource_id = self._model_data_index.get_resource_id(name)

        return resource_id

    def resolve_uid(
        self,
        uid: int | str
    ) -> int | None:

        # Si la ID de usuario provista es una referencia de recurso...
        if isinstance(uid, str):
            # Obtención de la ID de usuario desde la referencia de recurso
            uid = self._model_data_index.get_resource_id(uid)

            return uid
        # Si la ID de usuario provista es un entero...
        else:
            # Se usa ésta como valor de ID de usuario
            return uid
