from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from typing import Generic
from typing import TypedDict
from .type_parameters import _T
from .literals import InitialModels
from .literals import OnDeleteOption
from .literals import StateOption
from .literals import TTypeName
from .structures import JSONLike
from .interfaces import Many2One

# Tipado para valores nulos
type nullable[T] = T | None

class ttype:
    integer = int
    char = str
    boolean = bool
    float = float
    date = date
    datetime = datetime
    time = time
    duration = timedelta
    many2one = Many2One
    one2many = list[int]
    many2many = list[int]
    file = str
    text = str
    selection = _T
    json = JSONLike

class RecordSchema(TypedDict):
    id: ttype.integer
    name: nullable[ttype.char]
    create_date: ttype.datetime
    update_date: ttype.datetime
    create_uid: ttype.many2one
    update_uid: ttype.many2one

class _InternalModelSchema:
    class _Common(TypedDict):
        name: ttype.char
    class _HasStep(TypedDict):
        sequence: ttype.integer
    class _FactoryState(TypedDict):
        state: ttype.selection[StateOption]
    class _LabeledModel(TypedDict):
        label: ttype.char

    class base_users(_Common):
        login: ttype.char
        password: ttype.char
        role_ids: ttype.many2many
        profile_picture: ttype.file

    class base_model(_Common, _FactoryState, _LabeledModel):
        model: ttype.selection[InitialModels]
        description: ttype.text
        has_sequence: ttype.boolean

    class base_model_field(_Common, _FactoryState, _LabeledModel):
        model_id: ttype.integer
        ttype: ttype.selection[TTypeName]
        nullable: ttype.boolean
        on_delete: ttype.selection[OnDeleteOption]
        is_required: ttype.boolean
        readonly: ttype.boolean
        default_value: ttype.char
        unique: ttype.boolean
        help_info: ttype.text
        related_model_id: ttype.many2one
        related_field: ttype.char
        is_computed: ttype.boolean

    class base_model_field_selection(_Common, _LabeledModel):
        field_id: ttype.many2one

    class base_model_data(_Common):
        model_name: ttype.char
        res_id: ttype.many2one

    class base_model_data_process(_Common):
        step_ids: ttype.one2many

    class base_model_data_step(_Common, _HasStep):
        process_id: ttype.many2one
        model_name: ttype.char
        res_name: ttype.char

    class base_model_data_step_record(_Common, _HasStep, Generic[_T]):
        step_id: ttype.many2one
        data: _T
