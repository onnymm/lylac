from typing import Optional
from ..._module_types import (
    CriteriaStructure,
    ModelName,
)

class DQL_Interface():

    def search(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        offset: Optional[int],
        limit: Optional[int],
    ) -> list[int]:
        ...
