from sqlalchemy.engine import Connection
from .._constants import MODEL_NAME
from .._constants import REF
from .._constants import TABLE_NAME
from .._constants import TTYPE_NAME
from .._resources import DataMap
from .._resources import ModelDataIndex
from .._typing.definitions import _InternalModelSchema
from ..settings import CONFIG

def build_initial_data(conn: Connection) -> DataMap:

    # Inicialización de instancia de índice de datos de modelo
    model_data_index = ModelDataIndex(conn)

    model_data: list[_InternalModelSchema.base_model_data] = [
        # Usuarios
        {
            'name': REF.BASE_USERS.ROOT_USER,
            'model_name': MODEL_NAME.BASE_USERS,
        },
        {
            'name': REF.BASE_USERS.ADMIN_USER,
            'model_name': MODEL_NAME.BASE_USERS,
        },
        # Modelos
        {
            'name': REF.BASE_MODEL.BASE_USERS,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_FIELD,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_DATA,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        {
            'name': REF.BASE_MODEL.BASE_USER_SESSION,
            'model_name': MODEL_NAME.BASE_MODEL,
        },
        # Campos
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__UPDATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__ACTIVE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__LOGIN,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__PASSWORD,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__PROFILE_PICTURE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__UPDATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__STATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__LABEL,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__MODEL,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__HAS_SEQUENCE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__IS_ARCHIVABLE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__HAS_LABEL,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__DESCRIPTION,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__FIELD_IDS,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__RELATED_FIELD_IDS,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__TRANSIENT,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_M,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__LABEL,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__STATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__MODEL_ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__NULLABLE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__ON_DELETE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__IS_REQUIRED,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__READONLY,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__DEFAULT_VALUE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__UNIQUE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__HELP_INFO,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__RELATED_MODEL_ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__RELATED_FIELD,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__IS_COMPUTED,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__SELECTION_IDS,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__UPDATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__LABEL,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__FIELD_ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__UPDATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__MODEL_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__RES_ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__UPDATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__STEP_IDS,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__UPDATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__SEQUENCE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__PROCESS_ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__MODEL_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__RECORD_DATA_IDS,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__UPDATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__STEP_ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__SEQUENCE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__DATA,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__CREATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__UPDATE_DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__CREATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__UPDATE_UID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__DISPLAY_NAME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__USER_ID,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__VALIDITY_TIME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__EXPIRES_AT,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__STATE__BASE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__STATE__GENERIC,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__ON_DELETE__SET_NULL,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__ON_DELETE__CASCADE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__ON_DELETE__RESTRICT,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__INTEGER,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__CHAR,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__FLOAT,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__BOOLEAN,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__DATE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__DATETIME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__TIME,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__DURATION,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__FILE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__TEXT,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__SELECTION,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__MANY2ONE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__ONE2MANY,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__MANY2MANY,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__JSON,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__STATE__BASE,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__STATE__GENERIC,
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        },
    ]

    process: list[_InternalModelSchema.base_model_data_process] = [
        # 1
        {'name': 'initial_users'},
        # 2
        {'name': 'initial_structure'},
    ]

    steps: list[_InternalModelSchema.base_model_data_step] = [
        # 1
        {
            'model_name': MODEL_NAME.BASE_USERS,
            'process_id': 1,
            'sequence': 1,
        },
        # 2
        {
            'model_name': MODEL_NAME.BASE_MODEL,
            'process_id': 2,
            'sequence': 1,
        },
        # 3
        {
            'model_name': MODEL_NAME.BASE_MODEL_FIELD,
            'process_id': 2,
            'sequence': 2,
        },
        # 4
        {
            'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
            'process_id': 2,
            'sequence': 4,
        },
    ]

    records__base_users: list[_InternalModelSchema.base_model_data_step_record[_InternalModelSchema.base_users]] = [
        {
            'name': REF.BASE_USERS.ROOT_USER,
            'step_id': 1,
            'sequence': 1,
            'data': {
                'login': CONFIG.ROOT_USER_LOGIN,
                'name': CONFIG.ROOT_USER_NAME,
            },
        },
        {
            'name': REF.BASE_USERS.ADMIN_USER,
            'step_id': 1,
            'sequence': 2,
            'data': {
                'login': CONFIG.ADMIN_USER_LOGIN,
                'name': CONFIG.ADMIN_USER_NAME,
            },
        },
    ]

    records__base_model: list[_InternalModelSchema.base_model_data_step_record[_InternalModelSchema.base_model]] = [
        {
            'name': REF.BASE_MODEL.BASE_USERS,
            'step_id': 2,
            'sequence': 1,
            'data': {
                'name': TABLE_NAME.BASE_USERS,
                'model': MODEL_NAME.BASE_USERS,
                'label': 'Usuarios',
                'description': 'Usuarios de la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL,
            'step_id': 2,
            'sequence': 2,
            'data': {
                'name': TABLE_NAME.BASE_MODEL,
                'model': MODEL_NAME.BASE_MODEL,
                'label': 'Modelos',
                'description': 'Modelos de la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_FIELD,
            'step_id': 2,
            'sequence': 3,
            'data': {
                'name': TABLE_NAME.BASE_MODEL_FIELD,
                'model': MODEL_NAME.BASE_MODEL_FIELD,
                'label': 'Campos',
                'description': 'Campos de modelos de la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION,
            'step_id': 2,
            'sequence': 4,
            'data': {
                'name': TABLE_NAME.BASE_MODEL_FIELD_SELECTION,
                'model': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
                'label': 'Valores de selección',
                'description': 'Valores de selección de campos de modelos de la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_DATA,
            'step_id': 2,
            'sequence': 5,
            'data': {
                'name': TABLE_NAME.BASE_MODEL_DATA,
                'model': MODEL_NAME.BASE_MODEL_DATA,
                'label': 'Datos de modelos',
                'description': 'Datos de modelos y registros de toda la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS,
            'step_id': 2,
            'sequence': 6,
            'data': {
                'name': TABLE_NAME.BASE_MODEL_DATA_PROCESS,
                'model': MODEL_NAME.BASE_MODEL_DATA_PROCESS,
                'label': 'Procesos de creación de datos de modelo',
                'description': 'Procesos de creación de datos iniciales de modelos en la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP,
            'step_id': 2,
            'sequence': 7,
            'data': {
                'name': TABLE_NAME.BASE_MODEL_DATA_PROCESS_STEP,
                'model': MODEL_NAME.BASE_MODEL_DATA_PROCESS_STEP,
                'label': 'Pasos de procesos',
                'description': 'Pasos de procesos de creación de datos de modelos.',
                'has_sequence': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD,
            'step_id': 2,
            'sequence': 8,
            'data': {
                'name': TABLE_NAME.BASE_MODEL_DATA_PROCESS_STEP_RECORD,
                'model': MODEL_NAME.BASE_MODEL_DATA_PROCESS_STEP_RECORD,
                'label': 'Registros de datos de modelos',
                'description': 'Registros de datos de modelos a crear en la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL.BASE_USER_SESSION,
            'step_id': 2,
            'sequence': 9,
            'data': {
                'name': TABLE_NAME.BASE_USER_SESSION,
                'model': MODEL_NAME.BASE_USER_SESSION,
                'label': 'Registros de sesiones de usuario',
                'description': 'Registros de sesiones de usuario activas y expiradas.',
                'state': 'base',
            },
        },
    ]

    records__base_model_field: list[_InternalModelSchema.base_model_data_step_record[_InternalModelSchema.base_model_field]] = [
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__ID,
            'step_id': 3,
            'sequence': 10,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'unique': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__NAME,
            'step_id': 3,
            'sequence': 20,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__CREATE_DATE,
            'step_id': 3,
            'sequence': 30,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__UPDATE_DATE,
            'step_id': 3,
            'sequence': 40,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__CREATE_UID,
            'step_id': 3,
            'sequence': 50,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__UPDATE_UID,
            'step_id': 3,
            'sequence': 60,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 70,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__ACTIVE,
            'step_id': 3,
            'sequence': 80,
            'data': {
                'name': 'active',
                'label': 'Activo',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'default_value': True,
                'nullable': False,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__LOGIN,
            'step_id': 3,
            'sequence': 90,
            'data': {
                'name': 'login',
                'label': 'Inicio de sesión',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'is_required': True,
                'unique': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__PASSWORD,
            'step_id': 3,
            'sequence': 100,
            'data': {
                'name': 'password',
                'label': 'Contraseña',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USERS__PROFILE_PICTURE,
            'step_id': 3,
            'sequence': 110,
            'data': {
                'name': 'profile_picture',
                'label': 'Foto de perfil',
                'ttype': TTYPE_NAME.FILE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__ID,
            'step_id': 3,
            'sequence': 120,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'unique': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__NAME,
            'step_id': 3,
            'sequence': 130,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__CREATE_DATE,
            'step_id': 3,
            'sequence': 140,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__UPDATE_DATE,
            'step_id': 3,
            'sequence': 150,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__CREATE_UID,
            'step_id': 3,
            'sequence': 160,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__UPDATE_UID,
            'step_id': 3,
            'sequence': 170,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 180,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__STATE,
            'step_id': 3,
            'sequence': 190,
            'data': {
                'name': 'state',
                'label': 'Tipo de campo',
                'ttype': TTYPE_NAME.SELECTION,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'default_value': 'generic',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__LABEL,
            'step_id': 3,
            'sequence': 200,
            'data': {
                'name': 'label',
                'label': 'Nombre visible',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'is_required': True,
                'nullable': False,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__MODEL,
            'step_id': 3,
            'sequence': 210,
            'data': {
                'name': 'model',
                'label': 'Referencia de modelo',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'unique': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__HAS_SEQUENCE,
            'step_id': 3,
            'sequence': 220,
            'data': {
                'name': 'has_sequence',
                'label': 'Tiene secuencia',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'readonly': True,
                'default_value': False,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__IS_ARCHIVABLE,
            'step_id': 3,
            'sequence': 221,
            'data': {
                'name': 'is_archivable',
                'label': 'Es archivable',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'readonly': True,
                'default_value': False,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__HAS_LABEL,
            'step_id': 3,
            'sequence': 222,
            'data': {
                'name': 'has_label',
                'label': 'Tiene leyenda',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'readonly': True,
                'default_value': False,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__DESCRIPTION,
            'step_id': 3,
            'sequence': 230,
            'data': {
                'name': 'description',
                'label': 'Descripción',
                'ttype': TTYPE_NAME.TEXT,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__FIELD_IDS,
            'step_id': 3,
            'sequence': 240,
            'data': {
                'name': 'field_ids',
                'label': 'Campos',
                'ttype': TTYPE_NAME.ONE2MANY,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'related_field': 'model_id',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__RELATED_FIELD_IDS,
            'step_id': 3,
            'sequence': 250,
            'data': {
                'name': 'related_field_ids',
                'label': 'Campos relacionados',
                'ttype': TTYPE_NAME.ONE2MANY,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'related_field': 'related_model_id',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL__TRANSIENT,
            'step_id': 3,
            'sequence': 251,
            'data': {
                'name': 'transient',
                'label': 'Es modelo transitorio',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__ID,
            'step_id': 3,
            'sequence': 260,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'unique': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__NAME,
            'step_id': 3,
            'sequence': 270,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__CREATE_DATE,
            'step_id': 3,
            'sequence': 280,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__UPDATE_DATE,
            'step_id': 3,
            'sequence': 290,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__CREATE_UID,
            'step_id': 3,
            'sequence': 300,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__UPDATE_UID,
            'step_id': 3,
            'sequence': 310,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 320,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__STATE,
            'step_id': 3,
            'sequence': 330,
            'data': {
                'name': 'state',
                'label': 'Tipo de campo',
                'ttype': TTYPE_NAME.SELECTION,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'default_value': 'generic',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__LABEL,
            'step_id': 3,
            'sequence': 340,
            'data': {
                'name': 'label',
                'label': 'Nombre visible',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__MODEL_ID,
            'step_id': 3,
            'sequence': 350,
            'data': {
                'name': 'model_id',
                'label': 'Modelo',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'is_required': True,
                'nullable': False,
                'on_delete': 'cascade',
                'readonly': True,
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE,
            'step_id': 3,
            'sequence': 360,
            'data': {
                'name': 'ttype',
                'label': 'Tipo de dato',
                'ttype': TTYPE_NAME.SELECTION,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__NULLABLE,
            'step_id': 3,
            'sequence': 370,
            'data': {
                'name': 'nullable',
                'label': 'Puede ser nulo',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'default_value': False,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__ON_DELETE,
            'step_id': 3,
            'sequence': 380,
            'data': {
                'name': 'on_delete',
                'label': 'Cuando se elimina el registro padre',
                'ttype': TTYPE_NAME.SELECTION,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'readonly': True,
                'default_value': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__IS_REQUIRED,
            'step_id': 3,
            'sequence': 390,
            'data': {
                'name': 'is_required',
                'label': 'Es requerido',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'default_value': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__READONLY,
            'step_id': 3,
            'sequence': 400,
            'data': {
                'name': 'readonly',
                'label': 'Solo lectura',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'default_value': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__DEFAULT_VALUE,
            'step_id': 3,
            'sequence': 410,
            'data': {
                'name': 'default_value',
                'label': 'Valor predeterminado',
                'ttype': TTYPE_NAME.JSON,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__UNIQUE,
            'step_id': 3,
            'sequence': 420,
            'data': {
                'name': 'unique',
                'label': 'Único',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'default_value': False,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__HELP_INFO,
            'step_id': 3,
            'sequence': 430,
            'data': {
                'name': 'help_info',
                'label': 'Información de ayuda',
                'ttype': TTYPE_NAME.TEXT,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__RELATED_MODEL_ID,
            'step_id': 3,
            'sequence': 440,
            'data': {
                'name': 'related_model_id',
                'label': 'Modelo relacionado',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL),
                'state': 'base',
                'on_delete': 'restrict',
                'readonly': True,
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__RELATED_FIELD,
            'step_id': 3,
            'sequence': 450,
            'data': {
                'name': 'related_field',
                'label': 'Campo relacionado',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__IS_COMPUTED,
            'step_id': 3,
            'sequence': 460,
            'data': {
                'name': 'is_computed',
                'label': 'Es computado',
                'ttype': TTYPE_NAME.BOOLEAN,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'readonly': True,
                'default_value': False,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__SELECTION_IDS,
            'step_id': 3,
            'sequence': 470,
            'data': {
                'name': 'selection_ids',
                'label': 'Valores de selección',
                'ttype': TTYPE_NAME.ONE2MANY,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'related_field': 'field_id',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__ID,
            'step_id': 3,
            'sequence': 480,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'unique': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__NAME,
            'step_id': 3,
            'sequence': 490,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__CREATE_DATE,
            'step_id': 3,
            'sequence': 500,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__UPDATE_DATE,
            'step_id': 3,
            'sequence': 510,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__CREATE_UID,
            'step_id': 3,
            'sequence': 520,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__UPDATE_UID,
            'step_id': 3,
            'sequence': 530,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 540,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__LABEL,
            'step_id': 3,
            'sequence': 550,
            'data': {
                'name': 'label',
                'label': 'Nombre visible',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'is_required': True,
                'nullable': False,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD_SELECTION__FIELD_ID,
            'step_id': 3,
            'sequence': 560,
            'data': {
                'name': 'field_id',
                'label': 'Campo',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_FIELD),
                'on_delete': 'cascade',
                'is_required': True,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__ID,
            'step_id': 3,
            'sequence': 570,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'unique': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__NAME,
            'step_id': 3,
            'sequence': 580,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__CREATE_DATE,
            'step_id': 3,
            'sequence': 590,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__UPDATE_DATE,
            'step_id': 3,
            'sequence': 600,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__CREATE_UID,
            'step_id': 3,
            'sequence': 610,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__UPDATE_UID,
            'step_id': 3,
            'sequence': 620,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 630,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__MODEL_NAME,
            'step_id': 3,
            'sequence': 640,
            'data': {
                'name': 'model_name',
                'label': 'Nombre del modelo',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'is_required': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA__RES_ID,
            'step_id': 3,
            'sequence': 650,
            'data': {
                'name': 'res_id',
                'label': 'ID de recurso',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA),
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__ID,
            'step_id': 3,
            'sequence': 660,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'unique': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__NAME,
            'step_id': 3,
            'sequence': 670,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__CREATE_DATE,
            'step_id': 3,
            'sequence': 680,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__UPDATE_DATE,
            'step_id': 3,
            'sequence': 690,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__CREATE_UID,
            'step_id': 3,
            'sequence': 700,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__UPDATE_UID,
            'step_id': 3,
            'sequence': 710,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 720,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS__STEP_IDS,
            'step_id': 3,
            'sequence': 730,
            'data': {
                'name': 'step_ids',
                'label': 'Pasos de proceso',
                'ttype': TTYPE_NAME.ONE2MANY,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'related_field': 'process_id',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__ID,
            'step_id': 3,
            'sequence': 740,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'unique': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__NAME,
            'step_id': 3,
            'sequence': 750,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__CREATE_DATE,
            'step_id': 3,
            'sequence': 760,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__UPDATE_DATE,
            'step_id': 3,
            'sequence': 770,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__CREATE_UID,
            'step_id': 3,
            'sequence': 780,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__UPDATE_UID,
            'step_id': 3,
            'sequence': 790,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 800,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__SEQUENCE,
            'step_id': 3,
            'sequence': 810,
            'data': {
                'name': 'sequence',
                'label': 'Secuencia',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__PROCESS_ID,
            'step_id': 3,
            'sequence': 820,
            'data': {
                'name': 'process_id',
                'label': 'Proceso',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                'on_delete': 'cascade',
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__MODEL_NAME,
            'step_id': 3,
            'sequence': 830,
            'data': {
                'name': 'model_name',
                'label': 'Modelo',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP__RECORD_DATA_IDS,
            'step_id': 3,
            'sequence': 840,
            'data': {
                'name': 'record_data_ids',
                'label': 'Registros',
                'ttype': TTYPE_NAME.ONE2MANY,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'related_field': 'step_id',
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__ID,
            'step_id': 3,
            'sequence': 850,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'unique': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__NAME,
            'step_id': 3,
            'sequence': 860,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__CREATE_DATE,
            'step_id': 3,
            'sequence': 870,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__UPDATE_DATE,
            'step_id': 3,
            'sequence': 880,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__CREATE_UID,
            'step_id': 3,
            'sequence': 890,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__UPDATE_UID,
            'step_id': 3,
            'sequence': 900,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 910,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__STEP_ID,
            'step_id': 3,
            'sequence': 920,
            'data': {
                'name': 'step_id',
                'label': 'Paso',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'on_delete': 'cascade',
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__SEQUENCE,
            'step_id': 3,
            'sequence': 930,
            'data': {
                'name': 'sequence',
                'label': 'Secuencia',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_MODEL_DATA_PROCESS_STEP_RECORD__DATA,
            'step_id': 3,
            'sequence': 940,
            'data': {
                'name': 'data',
                'label': 'Datos',
                'ttype': TTYPE_NAME.JSON,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__ID,
            'step_id': 3,
            'sequence': 950,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': TTYPE_NAME.INTEGER,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'unique': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__NAME,
            'step_id': 3,
            'sequence': 960,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__CREATE_DATE,
            'step_id': 3,
            'sequence': 970,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__UPDATE_DATE,
            'step_id': 3,
            'sequence': 980,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__CREATE_UID,
            'step_id': 3,
            'sequence': 990,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__UPDATE_UID,
            'step_id': 3,
            'sequence': 1000,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__DISPLAY_NAME,
            'step_id': 3,
            'sequence': 1010,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': TTYPE_NAME.CHAR,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__USER_ID,
            'step_id': 3,
            'sequence': 1020,
            'data': {
                'name': 'user_id',
                'label': 'Usuario',
                'ttype': TTYPE_NAME.MANY2ONE,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'related_model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USERS),
                'on_delete': 'cascade',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__VALIDITY_TIME,
            'step_id': 3,
            'sequence': 1030,
            'data': {
                'name': 'validity_time',
                'label': 'Tiempo de validez',
                'ttype': TTYPE_NAME.DURATION,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD.BASE_USER_SESSION__EXPIRES_AT,
            'step_id': 3,
            'sequence': 1040,
            'data': {
                'name': 'expires_at',
                'label': 'Expira el',
                'ttype': TTYPE_NAME.DATETIME,
                'model_id': model_data_index.encode(REF.BASE_MODEL.BASE_USER_SESSION),
                'is_computed': True,
                'readonly': True,
                'state': 'base',
            },
        },
    ]

    records__base_model_field_selection: list[_InternalModelSchema.base_model_data_step_record[_InternalModelSchema.base_model_field_selection]] = [
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__STATE__BASE,
            'step_id': 4,
            'sequence': 5,
            'data': {
                'name': 'base',
                'label': 'Base',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL__STATE),
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__STATE__GENERIC,
            'step_id': 4,
            'sequence': 10,
            'data': {
                'name': 'generic',
                'label': 'Personalizado',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL__STATE),
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__ON_DELETE__SET_NULL,
            'step_id': 4,
            'sequence': 15,
            'data': {
                'name': 'set_null',
                'label': 'Establecer como nulo',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__ON_DELETE),
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__ON_DELETE__CASCADE,
            'step_id': 4,
            'sequence': 20,
            'data': {
                'name': 'cascade',
                'label': 'Eliminar en cascada',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__ON_DELETE),
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL__ON_DELETE__RESTRICT,
            'step_id': 4,
            'sequence': 25,
            'data': {
                'name': 'restrict',
                'label': 'Restringir eliminación',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__ON_DELETE),
            },
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__INTEGER,
            'step_id': 4,
            'sequence': 30,
            'data': {
                'name': TTYPE_NAME.INTEGER,
                'label': 'Entero',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__CHAR,
            'step_id': 4,
            'sequence': 35,
            'data': {
                'name': TTYPE_NAME.CHAR,
                'label': 'Caracter',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__FLOAT,
            'step_id': 4,
            'sequence': 40,
            'data': {
                'name': 'float',
                'label': 'Flotante',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__BOOLEAN,
            'step_id': 4,
            'sequence': 45,
            'data': {
                'name': TTYPE_NAME.BOOLEAN,
                'label': 'Booleano',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__DATE,
            'step_id': 4,
            'sequence': 50,
            'data': {
                'name': TTYPE_NAME.DATE,
                'label': 'Fecha',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__DATETIME,
            'step_id': 4,
            'sequence': 55,
            'data': {
                'name': TTYPE_NAME.DATETIME,
                'label': 'Fecha y hora',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__TIME,
            'step_id': 4,
            'sequence': 60,
            'data': {
                'name': TTYPE_NAME.TIME,
                'label': 'Hora',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__DURATION,
            'step_id': 4,
            'sequence': 65,
            'data': {
                'name': TTYPE_NAME.DURATION,
                'label': 'Duración',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__FILE,
            'step_id': 4,
            'sequence': 70,
            'data': {
                'name': TTYPE_NAME.FILE,
                'label': 'Binario',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__TEXT,
            'step_id': 4,
            'sequence': 75,
            'data': {
                'name': TTYPE_NAME.TEXT,
                'label': 'Texto largo',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__SELECTION,
            'step_id': 4,
            'sequence': 80,
            'data': {
                'name': TTYPE_NAME.SELECTION,
                'label': 'Selección',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__MANY2ONE,
            'step_id': 4,
            'sequence': 85,
            'data': {
                'name': TTYPE_NAME.MANY2ONE,
                'label': 'Muchos a uno',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__ONE2MANY,
            'step_id': 4,
            'sequence': 90,
            'data': {
                'name': TTYPE_NAME.ONE2MANY,
                'label': 'Uno a muchos',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__MANY2MANY,
            'step_id': 4,
            'sequence': 95,
            'data': {
                'name': TTYPE_NAME.MANY2MANY,
                'label': 'Muchos a muchos',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__TTYPE__JSON,
            'step_id': 4,
            'sequence': 100,
            'data': {
                'name': TTYPE_NAME.JSON,
                'label': TTYPE_NAME.JSON,
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__TTYPE)
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__STATE__BASE,
            'step_id': 4,
            'sequence': 105,
            'data': {
                'name': 'base',
                'label': 'Base',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__STATE),
            }
        },
        {
            'name': REF.BASE_MODEL_FIELD_SELECTION.BASE_MODEL_FIELD__STATE__GENERIC,
            'step_id': 4,
            'sequence': 110,
            'data': {
                'name': 'generic',
                'label': 'Personalizado',
                'field_id': model_data_index.encode(REF.BASE_MODEL_FIELD.BASE_MODEL_FIELD__STATE),
            }
        },
    ]

    total_records = [
        *records__base_users,
        *records__base_model,
        *records__base_model_field,
        *records__base_model_field_selection,
    ]

    data_map = DataMap(
        model_data= model_data,
        process= process,
        steps= steps,
        total_records= total_records,
    )

    return data_map
