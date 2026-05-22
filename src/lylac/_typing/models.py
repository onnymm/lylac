from typing import TypedDict
from .definitions import TType
from .definitions import Nullable

class _DefaultFields(TypedDict):
    name: Nullable[TType.Char]
    create_date: TType.Datetime
    update_date: TType.Datetime
    create_uid: Nullable[TType.Many2One]
    update_uid: Nullable[TType.Many2One]
    display_name: TType.Char
    sequence: TType.Integer

class _BasicRecord(TypedDict):
    id: TType.Integer

class RecordShape(TypedDict):
    ...

class UserSession(RecordShape):
    login: TType.Char
    active: TType.Boolean
    password: TType.Char

class _base_users__fields(RecordShape):
    login: TType.Char
    active: TType.Boolean
    password: TType.Char

class _found_session(RecordShape):
    is_active_session: TType.Boolean
    user_is_active: TType.Boolean
    uid: TType.Integer
