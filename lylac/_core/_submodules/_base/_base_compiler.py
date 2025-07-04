from ...._module_types import (
    RecordData,
    Transaction,
)

class BaseCompiler():

    def get_user_data_by_username(
        self,
        username: str,
    ) -> tuple[int, str] | None:
        ...

    def is_active_user_from_session_uuid(
        self,
        session_uuid: str,
    ) -> bool:
        ...

    def check_permission(
        self,
        user_id: int,
        transaction: Transaction,
    ) -> bool:
        ...

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
