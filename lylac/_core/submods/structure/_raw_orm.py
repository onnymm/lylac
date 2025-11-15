from typing import Tuple
from ...._module_types import TType

class _RawORM_Interface():

    def get_model_fields(
        self,
        model_name,
    ) -> list[Tuple[int, str, TType, None | str, None | str, bool]]:
        ...
