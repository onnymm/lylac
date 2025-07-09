from typing import Any
import pandas as pd
from sqlalchemy.engine.cursor import CursorResult
from ..._module_types import OutputOptions, TType

class Output_Interface():

    def get_found_ids(
        self,
        response: CursorResult[int],
    ) -> list[int]:
        ...

    def build_output(
        self,
        response: pd.DataFrame,
        ttypes: list[tuple[str, TType]],
        specified_output: OutputOptions,
        default_output: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | list[dict[str, Any]]:
        ...
