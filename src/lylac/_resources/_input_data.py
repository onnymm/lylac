from dataclasses import dataclass
from dataclasses import fields
from .._typing.literals import OnDeleteOption
from .._typing.literals import StateOption
from .._typing.literals import TTypeName

class InputData:
    class _Template:

        def to_dict(
            self,
        ) -> dict:

            return {
                field.name: getattr(self, field.name)
                for field in fields(self)
            }

    @dataclass(slots= True, frozen= True)
    class BaseModelField(_Template):
        name: str
        label: str
        ttype: TTypeName
        model_id: str
        state: StateOption = 'base'
        unique:bool = False
        default_value: str | None = None
        help_info: str | None = None
        is_computed: bool = False
        is_required: bool = False
        nullable: bool = False
        on_delete: OnDeleteOption | None = None
        readonly: bool = False
        related_field: str | None = None
        related_model_id: str | None = None
