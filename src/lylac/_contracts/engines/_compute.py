from typing import Generic
from ..._resources import DatabaseMetadata
from ..._typing.structures import ComputeContextHub
from ..._typing.type_parameters import _M

class Contract_ComputationEngine(Generic[_M]):
    hub: ComputeContextHub[_M]

    def expand_to_custom_models(
        self,
        database_metadata: DatabaseMetadata[_M],
    ) -> None:
        ...
