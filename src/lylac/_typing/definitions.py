from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from typing import Generic
from typing import TypedDict
from .type_parameters import _D
from .type_parameters import _L
from .literals import InitialModels
from .literals import OnDeleteOption
from .literals import StateOption
from .literals import TTypeName
from .structures import JSONLike
from .interfaces import Many2One

# Tipado para valores nulos
type Nullable[T] = T | None

class TType:
    Integer = int
    Char = str
    Boolean = bool
    Float = float
    Date = date
    Datetime = datetime
    Time = time
    Duration = timedelta
    Many2One = Many2One
    One2Many = list[int]
    Many2Many = list[int]
    File = str
    Text = str
    Selection = _L
    JSON = JSONLike

class Template:

    class Record(TypedDict):
        id: TType.Integer

    class _NonEditableFields(TypedDict, Record):
        create_date: TType.Datetime
        update_date: TType.Datetime
        create_uid: TType.Many2One
        update_uid: TType.Many2One
        display_name: TType.Char

    class _OnlyEditableFields(TypedDict):
        name: Nullable[TType.Char]

    class RecordWithBasicFields(_NonEditableFields, _OnlyEditableFields):
        ...

class Feature():
    class HasSequence(TypedDict):
        sequence: TType.Integer
    class HasLabel(TypedDict):
        label: TType.Char
    class IsArchivable(TypedDict):
        active: TType.Boolean

class Preset:

    class BaseModel(Template.RecordWithBasicFields):
        is_archivable: TType.Boolean
        has_sequence: TType.Boolean
        has_label: TType.Boolean
        transient: TType.Boolean
        model: TType.Char
        description: TType.Text
        state: TType.Selection[StateOption]
        field_ids: TType.One2Many
        related_field_ids: TType.One2Many

    class BaseModelData(Template.RecordWithBasicFields):
        model_name: TType.Char
        res_id: Nullable[TType.Char]

    class BaseModelDataProcess(Template.RecordWithBasicFields):
        step_ids: TType.One2Many

    class BaseModelDataProcessStep(Template.RecordWithBasicFields, Feature.HasSequence):
        process_id: TType.Many2One
        model_name: TType.Char
        record_data_ids: TType.One2Many

    class BaseModelDataProcessStepRecord(Template.RecordWithBasicFields, Feature.HasSequence, Generic[_D]):
        step_id: TType.Many2One
        data: _D # TType.JSON

    class BaseModelField(Template.RecordWithBasicFields, Feature.HasLabel):
        model_id: TType.Many2One
        ttype: TType.Selection[TTypeName]
        nullable: TType.Boolean
        on_delete: TType.Selection[OnDeleteOption]
        is_required: TType.Boolean
        readonly: TType.Boolean
        default_value: TType.JSON
        unique: TType.Boolean
        help_info: Nullable[TType.Text]
        related_model_id: Nullable[TType.Many2One]
        related_field: Nullable[TType.Char]
        is_computed: TType.Boolean
        state: TType.Selection[StateOption]
        selection_ids: TType.One2Many

    class BaseModelFieldSelection(Template.RecordWithBasicFields, Feature.HasLabel):
        field_id: TType.Many2One

    class BaseRules(Template.RecordWithBasicFields, Feature.HasLabel, Feature.IsArchivable):
        domain: TType.Text
        model_id: TType.Many2One
        perm_create: TType.Boolean
        perm_read: TType.Boolean
        perm_update: TType.Boolean
        perm_delete: TType.Boolean
        global_: TType.Boolean

    class BaseUserAccess(Template.RecordWithBasicFields):
        group_id: TType.Many2One
        model_id: TType.Many2One
        perm_create: TType.Boolean
        perm_read: TType.Boolean
        perm_update: TType.Boolean
        perm_delete: TType.Boolean

    class BaseUserGroups(Template.RecordWithBasicFields, Feature.HasLabel):
        access_ids: TType.One2Many
        rule_ids: TType.One2Many

    class BaseUsers(Template.RecordWithBasicFields, Feature.IsArchivable):
        login: TType.Char
        password: TType.Char
        profile_picture: TType.File
        role_ids: TType.One2Many

    class BaseUserSession(Template.RecordWithBasicFields):
        user_id: TType.Many2One
        validity_time: TType.Duration
        expires_at: TType.Datetime

    class BaseUsersRole(Template.RecordWithBasicFields, Feature.HasLabel):
        group_ids: TType.One2Many


class RecordSchema(TypedDict):
    id: TType.Integer
    name: Nullable[TType.Char]
    create_date: TType.Datetime
    update_date: TType.Datetime
    create_uid: TType.Many2One
    update_uid: TType.Many2One

class _InternalModelSchema:
    class _Common(TypedDict):
        name: TType.Char
    class _HasStep(TypedDict):
        sequence: TType.Integer
    class _FactoryState(TypedDict):
        state: TType.Selection[StateOption]
    class _LabeledModel(TypedDict):
        label: TType.Char

    class base_users(_Common):
        login: TType.Char
        password: TType.Char
        role_ids: TType.Many2Many
        profile_picture: TType.File

    class base_model(_Common, _FactoryState, _LabeledModel):
        model: TType.Selection[InitialModels]
        description: TType.Text
        has_sequence: TType.Boolean

    class base_model_field(_Common, _FactoryState, _LabeledModel):
        model_id: TType.Integer
        ttype: TType.Selection[TTypeName]
        nullable: TType.Boolean
        on_delete: TType.Selection[OnDeleteOption]
        is_required: TType.Boolean
        readonly: TType.Boolean
        default_value: TType.Char
        unique: TType.Boolean
        help_info: TType.Text
        related_model_id: TType.Many2One
        related_field: TType.Char
        is_computed: TType.Boolean

    class base_model_field_selection(_Common, _LabeledModel):
        field_id: TType.Many2One

    class base_model_data(_Common):
        model_name: TType.Char
        res_id: TType.Many2One

    class base_model_data_process(_Common):
        step_ids: TType.One2Many

    class base_model_data_step(_Common, _HasStep):
        process_id: TType.Many2One
        model_name: TType.Char
        res_name: TType.Char

    class base_model_data_step_record(_Common, _HasStep, Generic[_D]):
        step_id: TType.Many2One
        data: _D
