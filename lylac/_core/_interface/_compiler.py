from ..._module_types import (
    RecordData,
    ModelName,
    Transaction,
)

class Compiler_Interface():

    def get_user_data_by_username(
        self,
        login: str,
    ) -> tuple[int, str] | None:
        ...

    def is_active_user_from_session_uuid(
        self,
        session_uuid: str,
    ) -> bool:
        ...

    def create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> list[int]:
        ...

    def create_many2many(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> None:
        ...

    def delete_many2many(
        self,
        model_name: ModelName,
        field_name: str,
        record_ids: list[int],
    ) -> None:
        ...

    def check_permission(
        self,
        user_id: int,
        transaction: Transaction,
    ) -> bool:
        ...
