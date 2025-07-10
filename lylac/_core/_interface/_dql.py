from typing import Optional
import pandas as pd
from ..._module_types import (
    CriteriaStructure,
    ModelName,
    OutputOptions,
    RecordValue,
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

    def read(
        self,
        model_name: ModelName,
        record_ids: int | list[int],
        fields: list[str],
        sortby: str | list[str],
        ascending: bool | list[bool],
        output_format: Optional[OutputOptions],
        only_ids_in_relations: bool,
    ) -> pd.DataFrame | list[dict[str, RecordValue]]:
        ...

    def search_read(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
        fields: list[str] = [],
        offset: int | None = None,
        limit: int | None = None,
        sortby: str | list[str] | None = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | dict[str, RecordValue]:
        ...

    def search_count(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
    ) -> int:
        ...
