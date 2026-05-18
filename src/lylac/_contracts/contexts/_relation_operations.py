from typing import Generic
from ..._typing.callables import CaptureCreatedRecordID
from ..._typing.structures import RecordData
from ..._typing.type_parameters import _M

class _Contract_CRUD:
    ...

class Contract_RelationOperationsContext(Generic[_M]):

    def run_relation_operations(
        self,
        crud: _Contract_CRUD,
    ) -> None:
        ...
    def capture_relation_commands(
        self,
        record_data: RecordData,
    ) -> CaptureCreatedRecordID:
        ...
