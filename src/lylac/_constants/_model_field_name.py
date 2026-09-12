class _FIELD_NAME:
    ID = 'id'
    NAME = 'name'
    CREATE_DATE = 'create_date'
    UPDATE_DATE = 'update_date'
    CREATE_UID = 'create_uid'
    UPDATE_UID = 'update_uid'
    DISPLAY_NAME = 'display_name'

class MODEL_FIELD_NAME:

    class BASE_USERS(_FIELD_NAME):
        ACTIVE = 'active'
        LOGIN = 'login'
        PASSWORD = 'password'
        PROFILE_PICTURE = 'profile_picture'
        ROLE_IDS = 'role_ids'

    class BASE_MODEL(_FIELD_NAME):
        STATE = 'state'
        LABEL = 'label'
        MODEL = 'model'
        HAS_SEQUENCE = 'has_sequence'
        IS_ARCHIVABLE = 'is_archivable'
        HAS_LABEL = 'has_label'
        DESCRIPTION = 'description'
        FIELD_IDS = 'field_ids'
        RELATED_FIELD_IDS = 'related_field_ids'
        TRANSIENT = 'transient'

    class BASE_MODEL_FIELD(_FIELD_NAME):
        LABEL = 'label'
        STATE = 'state'
        MODEL_ID = 'model_id'
        TTYPE = 'ttype'
        NULLABLE = 'nullable'
        ON_DELETE = 'on_delete'
        IS_REQUIRED = 'is_required'
        READONLY = 'readonly'
        DEFAULT_VALUE = 'default_value'
        UNIQUE = 'unique'
        HELP_INFO = 'help_info'
        RELATED_MODEL_ID = 'related_model_id'
        RELATED_FIELD = 'related_field'
        IS_COMPUTED = 'is_computed'
        SELECTION_IDS = 'selection_ids'

    class BASE_MODEL_FIELD_SELECTION(_FIELD_NAME):
        LABEL = 'label'
        FIELD_ID = 'field_id'

    class BASE_MODEL_DATA(_FIELD_NAME):
        MODEL_NAME = 'model_name'
        RES_ID = 'res_id'

    class BASE_MODEL_DATA_PROCESS(_FIELD_NAME):
        STEP_IDS = 'step_ids'

    class BASE_MODEL_DATA_PROCESS_STEP(_FIELD_NAME):
        SEQUENCE = 'sequence'
        PROCESS_ID = 'process_id'
        MODEL_NAME = 'model_name'
        RECORD_DATA_IDS = 'record_data_ids'

    class BASE_MODEL_DATA_PROCESS_STEP_RECORD(_FIELD_NAME):
        STEP_ID = 'step_id'
        SEQUENCE = 'sequence'
        DATA = 'data'

    class BASE_USERS_GROUP(_FIELD_NAME):
        LABEL = 'label'
        ACCESS_IDS = 'access_ids'

    class BASE_USERS_ROLE(_FIELD_NAME):
        LABEL = 'label'
        GROUP_IDS = 'group_ids'

    class BASE_USERS_ACCESS(_FIELD_NAME):
        MODEL_ID = 'model_id'
        PERM_CREATE = 'perm_create'
        PERM_READ = 'perm_read'
        PERM_UPDATE = 'perm_update'
        PERM_DELETE = 'perm_delete'
        GROUP_ID = 'group_id'
