from typing import TypedDict
from .definitions import ttype
from .definitions import nullable

class _DefaultFields(TypedDict):
    name: nullable[ttype.char]
    create_date: ttype.datetime
    update_date: ttype.datetime
    create_uid: nullable[ttype.many2one]
    update_uid: nullable[ttype.many2one]
    display_name: ttype.char
    sequence: ttype.integer

class _BasicRecord(TypedDict):
    id: ttype.integer

class RecordShape(TypedDict):
    ...

class UserSession(RecordShape):
    login: ttype.char
    active: ttype.boolean
    password: ttype.char

class _base_users__fields(RecordShape):
    login: ttype.char
    active: ttype.boolean
    password: ttype.char

class _found_session(RecordShape):
    is_active_session: ttype.boolean
    user_is_active: ttype.boolean
    uid: ttype.integer
