class FIELD_NAME:
    """
    ### Nombre de campo
    Constantes de nombres de campo que se encuentran en todo modelo de la base de
    datos.
    """
    ID = 'id'
    """`integer` ID del registro."""
    NAME = 'name'
    """`char` Nombre del registro."""
    CREATE_DATE = 'create_date'
    """`datetime` Fecha y hora de creación del registro."""
    UPDATE_DATE = 'update_date'
    """`datetime` Última fecha y hora de modificación del registro."""
    CREATE_UID = 'create_uid'
    """`many2one` Usuario que creó el registro."""
    UPDATE_UID = 'update_uid'
    """`many2one` Último usuario que modificó el registro."""
    DISPLAY_NAME = 'display_name'
    """`char` Nombre representativo del registro."""
    SEQUENCE = 'sequence'
    """`integer` Secuencia del registro."""
    ACTIVE = 'active'
    """`boolean` El registro está activo"""
    STATE = 'state'
    """`selection` Tipo de registro."""
    LABEL = 'label'
    """`char` Leyenda descriptiva del registro."""

    X = 'x'
    """
    `integer` Campo de ID de registro que referencía en relaciones `many2one`.
    """
    Y = 'y'
    """
    `integer` Campo de ID de registro referenciado en relaciones `many2one`.
    """

class MODEL_NAME:
    """
    ### Nombre de modelo
    Nombres de modelo base en la base de datos.
    """
    BASE_USERS = 'base.users'
    """
    Usuarios de la base de datos.
    """
    BASE_USER_SESSION = 'base.user.session'
    """
    Sesiones de usuario.
    """
    BASE_USER_ACCESS = 'base.user.access'
    """
    Permisos de acceso.
    """
    BASE_USER_GROUPS = 'base.user.groups'
    """
    Grupos de acceso.
    """
    BASE_USERS_ROLE = 'base.users.role'
    """
    Roles de usuario.
    """
    BASE_MODEL = 'base.model'
    """
    Modelos de la base de datos.
    """
    BASE_MODEL_FIELD = 'base.model.field'
    """
    Campos de modelos de la base de datos.
    """
    BASE_MODEL_FIELD_SELECTION = 'base.model.field.selection'
    """
    Valores de selección de campos de modelos de la base de datos.
    """
    BASE_MODEL_DATA = 'base.model.data'
    """
    Datos de modelos y registros de toda la base de datos.
    """
    BASE_MODEL_DATA_PROCESS = 'base.model.data.process'
    """
    Procesos de creación de datos iniciales de modelos en la base de datos.
    """
    BASE_MODEL_DATA_PROCESS_STEP = 'base.model.data.process.step'
    """
    Pasos de procesos de creación de datos de modelos.
    """
    BASE_MODEL_DATA_PROCESS_STEP_RECORD = 'base.model.data.process.step.record'
    """
    Registros de datos de modelos a crear en la base de datos.
    """
    BASE_RULES = 'base.rules'
    """
    Registros de reglas de registro.
    """

FACTORY_MODELS = [
    MODEL_NAME.BASE_USERS,
    MODEL_NAME.BASE_USER_SESSION,
    MODEL_NAME.BASE_MODEL,
    MODEL_NAME.BASE_MODEL_FIELD,
    MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
    MODEL_NAME.BASE_MODEL_DATA,
    MODEL_NAME.BASE_MODEL_DATA_PROCESS,
    MODEL_NAME.BASE_MODEL_DATA_PROCESS_STEP,
    MODEL_NAME.BASE_MODEL_DATA_PROCESS_STEP_RECORD,
]
"""
Modelos predeterminados.
"""

FACTORY_FIELDS = [
    FIELD_NAME.ID,
    FIELD_NAME.NAME,
    FIELD_NAME.CREATE_DATE,
    FIELD_NAME.UPDATE_DATE,
    FIELD_NAME.CREATE_UID,
    FIELD_NAME.UPDATE_UID,
    FIELD_NAME.DISPLAY_NAME,
    FIELD_NAME.SEQUENCE,
    FIELD_NAME.ACTIVE,
    FIELD_NAME.LABEL,
]
"""
Campos predeterminados.
"""

class RELATION_ACTION_NAME:
    """
    Nombres de comandos de acciones de relación.
    """
    CREATE = 'create'
    ADD = 'add'
    UPDATE = 'update'
    UNLINK = 'unlink'
    CLEAR = 'clear'
    REPLACE = 'replace'
    DELETE = 'delete'

RELATION_ACTIONS = [
    RELATION_ACTION_NAME.CREATE,
    RELATION_ACTION_NAME.ADD,
    RELATION_ACTION_NAME.UPDATE,
    RELATION_ACTION_NAME.UNLINK,
    RELATION_ACTION_NAME.CLEAR,
    RELATION_ACTION_NAME.REPLACE,
    RELATION_ACTION_NAME.DELETE,
]
"""
Nombres de comandos de acciones de relación.
"""

class PACKAGE:
    INITIAL_USERS = 'initial_users'
    INITIAL_STRUCTURE = 'initial_structure'

INITIAL_PACKAGES = [
    PACKAGE.INITIAL_USERS,
    PACKAGE.INITIAL_STRUCTURE,
]

class DATA_RESOURCE:
    'Referencias comunes para obtención de sus respectivas IDs.'
    ROOT_USER = 'base_users.root_user'
    'Superusuario de la base de datos.'
    ADMIN_USER = 'base_users.admin_user'
    'Administrador de la base de datos.'

    class MODEL:
        'Referencias de modelos en la base de datos.'
        BASE_USERS = 'base_model.base_users'
        BASE_USERS_ROLE = 'base_model.base_users_role'
        BASE_USER_ACCESS = 'base_model.base_user_access'
        BASE_USER_SESSION = 'base_model.base_user_session'
        BASE_USER_GROUPS = 'base_model.base_user_groups'
        BASE_RULES = 'base_model.base_rules'
        BASE_MODEL = 'base_model.base_model'
        BASE_MODEL_FIELD = 'base_model.base_model_field'
        BASE_MODEL_FIELD_SELECTION = 'base_model.base_model_field_selection'
        BASE_MODEL_DATA = 'base_model.base_model_data'
        BASE_MODEL_DATA_PROCESS = 'base_model.base_model_data_process'
        BASE_MODEL_DATA_PROCESS_STEP = 'base_model.base_model_data_process_step'
        BASE_MODEL_DATA_PROCESS_STEP_RECORD = 'base_model.base_model_data_process_step_record'

class PRESET:

    class SERVER_TASK:

        UPDATE_INSTANCE_METADATA = 'update_instance_metadata'

    class AUTOMATION:

        BASE_MODEL__CREATE_TABLE_ON_DATABASE = 'create_table_on_database'
        BASE_MODEL__CREATE_MODEL = 'create_model'
        BASE_MODEL__DROP_TABLE = 'drop_table'
        BASE_MODEL__DELETE_MODEL = 'delete_model'
        BASE_MODEL__RESTORE = 'restore'

        BASE_MODEL_FIELD__CREATE_COLUMN = 'create_column'
        BASE_MODEL_FIELD__REGISTER_ON_MODEL = 'register_on_model'
        BASE_MODEL_FIELD__DROP_COLUMN = 'drop_column'
