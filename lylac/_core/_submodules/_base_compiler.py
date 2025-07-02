from ._base_base_lylac import BaseBaseLylac
from ..._module_types import RecordData

class BaseCompiler():

    def create(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> list[int]:
        ...

    def create_many2many(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> None:
        ...

    def delete_many2many(
        self,
        model_name: str,
        field_name: str,
        record_ids: list[int],
    ) -> None:
        ...
