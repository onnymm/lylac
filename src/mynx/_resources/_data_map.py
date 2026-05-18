from dataclasses import dataclass
from .._typing.definitions import _InternalModelSchema

@dataclass(slots= True, frozen= True)
class DataMap:
    model_data: list[_InternalModelSchema.base_model_data]
    process: list[_InternalModelSchema.base_model_data_process]
    steps: list[_InternalModelSchema.base_model_data_step]
    total_records: list[_InternalModelSchema.base_model_data_step_record]
