from typing import TYPE_CHECKING
from .._constants import MODEL_FIELD_NAME
from .._constants import MODEL_NAME
from .._constants import RELATION_ACTION_NAME
from .._constants import REF
from .._constants import TTYPE_NAME

if TYPE_CHECKING:
    from .._main import Lylac

# Grupos de permisos
def _create_permission_groups(ctx: Lylac.TransactionContext):

    ctx.create(
        MODEL_NAME.BASE_USERS_GROUP,
        [
            # Permisos básicos
            {
                MODEL_FIELD_NAME.BASE_USERS_GROUP.NAME: 'basic_permissions',
                MODEL_FIELD_NAME.BASE_USERS_GROUP.LABEL: 'Permisos básicos',
                MODEL_FIELD_NAME.BASE_USERS_GROUP.ACCESS_IDS: {
                    RELATION_ACTION_NAME.CREATE: [
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'base_users__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_field__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_FIELD),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_field_selection__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_data__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_DATA),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_data_process__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_data_process_step__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_data_process_step_record__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_user_session__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USER_SESSION),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users_access__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_ACCESS),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users_group__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_GROUP),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users_role__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_ROLE),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users_update_password__user',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_UPDATE_PASSWORD),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                    ],
                },
            },
            # Administrador de la estructura de la base de datos
            {
                MODEL_FIELD_NAME.BASE_USERS_GROUP.NAME: 'database_structure_admin',
                MODEL_FIELD_NAME.BASE_USERS_GROUP.LABEL: 'Administrador de la estructura de la base de datos',
                MODEL_FIELD_NAME.BASE_USERS_GROUP.ACCESS_IDS: {
                    RELATION_ACTION_NAME.CREATE: [
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_FIELD),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_FIELD_SELECTION),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_data__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_DATA),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_data_process__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_data_process_step__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_model_data_process_step_record__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                    ],
                },
            },
            # Administrador de permisos de usuarios
            {
                MODEL_FIELD_NAME.BASE_USERS_GROUP.NAME: 'access_admin',
                MODEL_FIELD_NAME.BASE_USERS_GROUP.LABEL: 'Administrador de permisos de usuarios',
                MODEL_FIELD_NAME.BASE_USERS_GROUP.ACCESS_IDS: {
                    RELATION_ACTION_NAME.CREATE: [
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users_access__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_ACCESS),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users_group__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_GROUP),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users_role__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_ROLE),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_rules__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_RULES),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                    ],
                },
            },
            # Administrador de usuarios
            {
                MODEL_FIELD_NAME.BASE_USERS_GROUP.NAME: 'users_admin',
                MODEL_FIELD_NAME.BASE_USERS_GROUP.LABEL: 'Administrador de usuarios',
                MODEL_FIELD_NAME.BASE_USERS_GROUP.ACCESS_IDS: {
                    RELATION_ACTION_NAME.CREATE: [
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.NAME: 'base_users__admin',
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USER_SESSION),
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_CREATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_READ: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_UPDATE: True,
                            MODEL_FIELD_NAME.BASE_USERS_ACCESS.PERM_DELETE: True,
                        },
                    ],
                }
            },
        ],
    )

# Modelos, campos y valores de selección
def _build_models_structure(ctx: Lylac.TransactionContext):

    ctx.create(
        MODEL_NAME.BASE_MODEL,
        [
            # Creación de modelo de grupos de acceso
            {
                MODEL_FIELD_NAME.BASE_MODEL.NAME: 'base_users_group',
                MODEL_FIELD_NAME.BASE_MODEL.MODEL: MODEL_NAME.BASE_USERS_GROUP,
                MODEL_FIELD_NAME.BASE_MODEL.LABEL: 'Grupos de acceso',
                MODEL_FIELD_NAME.BASE_MODEL.DESCRIPTION: 'Registros de grupos de acceso.',
                MODEL_FIELD_NAME.BASE_MODEL.HAS_LABEL: True,
            },
            # Creación de modelo de reglas de registro
            {
                MODEL_FIELD_NAME.BASE_MODEL.NAME: 'base_rules',
                MODEL_FIELD_NAME.BASE_MODEL.MODEL: MODEL_NAME.BASE_RULES,
                MODEL_FIELD_NAME.BASE_MODEL.LABEL: 'Reglas de registro',
                MODEL_FIELD_NAME.BASE_MODEL.DESCRIPTION: 'Reglas de registro para definir dominios de transacciones.',
                MODEL_FIELD_NAME.BASE_MODEL.IS_ARCHIVABLE: True,
                MODEL_FIELD_NAME.BASE_MODEL.HAS_LABEL: True,
                MODEL_FIELD_NAME.BASE_MODEL.FIELD_IDS: {
                    RELATION_ACTION_NAME.CREATE: [
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'domain',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Dominio',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.TEXT,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.IS_REQUIRED: True,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NULLABLE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'model_id',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Modelo',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.MANY2ONE,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.RELATED_MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL),
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.ON_DELETE: 'cascade',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.IS_REQUIRED: True,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NULLABLE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'perm_create',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Permiso de creación',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'perm_read',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Permiso de lectura',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'perm_update',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Permiso de modificación',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'perm_delete',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Permiso de eliminación',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'global_',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Global',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NULLABLE: False,
                        },
                    ],
                }
            },
            # Creación de modelo de cambio de contraseña
            {
                MODEL_FIELD_NAME.BASE_MODEL.NAME: 'base_users_update_password',
                MODEL_FIELD_NAME.BASE_MODEL.MODEL: MODEL_NAME.BASE_USERS_UPDATE_PASSWORD,
                MODEL_FIELD_NAME.BASE_MODEL.LABEL: 'Cambio de contraseña de usuario',
                MODEL_FIELD_NAME.BASE_MODEL.DESCRIPTION: 'Asistente de cambio de contraseña',
                MODEL_FIELD_NAME.BASE_MODEL.TRANSIENT: True,
                MODEL_FIELD_NAME.BASE_MODEL.FIELD_IDS: {
                    RELATION_ACTION_NAME.CREATE: [
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'current_password',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Contraseña actual',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.CHAR,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.IS_REQUIRED: True,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NULLABLE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'new_password',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Nueva contraseña',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.CHAR,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.IS_REQUIRED: True,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NULLABLE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'confirm_password',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Confirma nueva contraseña',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.CHAR,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.IS_REQUIRED: True,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NULLABLE: False,
                        },
                    ],
                },
            },
        ],
    )

    ctx.create(
        MODEL_NAME.BASE_MODEL,
        [
            # Creación de modelo de permisos de acceso
            {
                MODEL_FIELD_NAME.BASE_MODEL.NAME: 'base_users_access',
                MODEL_FIELD_NAME.BASE_MODEL.MODEL: MODEL_NAME.BASE_USERS_ACCESS,
                MODEL_FIELD_NAME.BASE_MODEL.LABEL: 'Permisos de acceso',
                MODEL_FIELD_NAME.BASE_MODEL.DESCRIPTION: 'Registros de permisos de acceso granulares.',
                MODEL_FIELD_NAME.BASE_MODEL.FIELD_IDS: {
                    RELATION_ACTION_NAME.CREATE: [
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'model_id',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Modelo',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.MANY2ONE,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.RELATED_MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_MODEL),
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.ON_DELETE: 'cascade',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NULLABLE: False,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.IS_REQUIRED: True,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.READONLY: True,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'perm_create',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Permiso de creación',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'perm_read',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Permiso de lectura',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'perm_update',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Permiso de modificación',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'perm_delete',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Permiso de eliminación',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.BOOLEAN,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.DEFAULT_VALUE: False,
                        },
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'group_id',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Grupo',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.MANY2ONE,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.RELATED_MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_GROUP),
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.ON_DELETE: 'cascade',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.IS_REQUIRED: True,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NULLABLE: False,
                        },
                    ]
                }
            },
            # Creación de modelo de sesiones de usuario
            {
                MODEL_FIELD_NAME.BASE_MODEL.NAME: 'base_users_role',
                MODEL_FIELD_NAME.BASE_MODEL.MODEL: MODEL_NAME.BASE_USERS_ROLE,
                MODEL_FIELD_NAME.BASE_MODEL.LABEL: 'Roles de usuario',
                MODEL_FIELD_NAME.BASE_MODEL.DESCRIPTION: 'Sesiones de usuario.',
                MODEL_FIELD_NAME.BASE_MODEL.HAS_LABEL: True,
                MODEL_FIELD_NAME.BASE_MODEL.FIELD_IDS: {
                    RELATION_ACTION_NAME.CREATE: [
                        {
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'group_ids',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Grupos',
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.MANY2MANY,
                            MODEL_FIELD_NAME.BASE_MODEL_FIELD.RELATED_MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_GROUP),
                        }
                    ],
                },
            },
        ],
    )

    ctx.update(
        MODEL_NAME.BASE_MODEL,
        ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_GROUP),
        {
            MODEL_FIELD_NAME.BASE_MODEL.FIELD_IDS: {
                RELATION_ACTION_NAME.CREATE: {
                    MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'access_ids',
                    MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Accesos',
                    MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.ONE2MANY,
                    MODEL_FIELD_NAME.BASE_MODEL_FIELD.RELATED_MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_ACCESS),
                    MODEL_FIELD_NAME.BASE_MODEL_FIELD.RELATED_FIELD: 'group_id',
                },
            },
        },
    )

    ctx.create(
        MODEL_NAME.BASE_MODEL_FIELD,
        [
            # Creación de campo de roles del usuario en modelo de usuarios
            {
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'role_ids',
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Roles',
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.MANY2MANY,
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS),
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.RELATED_MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_ROLE),
            },
            # Creación de campo de reglas de registro en modelo de grupos de acceso
            {
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.NAME: 'rule_ids',
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.LABEL: 'Reglas de registro',
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.TTYPE: TTYPE_NAME.MANY2MANY,
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_USERS_GROUP),
                MODEL_FIELD_NAME.BASE_MODEL_FIELD.RELATED_MODEL_ID: ctx.get_resource_id(REF.BASE_MODEL.BASE_RULES)
            },
        ],
    )

# Roles de usuario
def _create_user_roles(ctx: Lylac.TransactionContext):

    # Creación de rol de super usuario
    ctx.update(
        MODEL_NAME.BASE_USERS,
        ctx.get_resource_id(REF.BASE_USERS.ROOT_USER),
        {
            MODEL_FIELD_NAME.BASE_USERS.ROLE_IDS: {
                RELATION_ACTION_NAME.CREATE: {
                    MODEL_FIELD_NAME.BASE_USERS_ROLE.NAME: 'root_user',
                    MODEL_FIELD_NAME.BASE_USERS_ROLE.LABEL: 'Superusuario',
                    MODEL_FIELD_NAME.BASE_USERS_ROLE.GROUP_IDS: {
                        RELATION_ACTION_NAME.ADD: [
                            ctx.get_resource_id(REF.BASE_USERS_GROUP.BASIC_PERMISSIONS),
                            ctx.get_resource_id(REF.BASE_USERS_GROUP.DATABASE_STRUCTURE_ADMIN),
                            ctx.get_resource_id(REF.BASE_USERS_GROUP.ACCESS_ADMIN),
                            ctx.get_resource_id(REF.BASE_USERS_GROUP.USERS_ADMIN),
                        ],
                    },
                },
            },
        },
    )

    # Creación de rol de administrador de la base de datos
    ctx.update(
        MODEL_NAME.BASE_USERS,
        ctx.get_resource_id(REF.BASE_USERS.ADMIN_USER),
        {
            MODEL_FIELD_NAME.BASE_USERS.ROLE_IDS: {
                RELATION_ACTION_NAME.CREATE: {
                    MODEL_FIELD_NAME.BASE_USERS_ROLE.NAME: 'database_admin',
                    MODEL_FIELD_NAME.BASE_USERS_ROLE.LABEL: 'Administrador de la base de datos',
                    MODEL_FIELD_NAME.BASE_USERS_ROLE.GROUP_IDS: {
                        RELATION_ACTION_NAME.ADD: [
                            ctx.get_resource_id(REF.BASE_USERS_GROUP.BASIC_PERMISSIONS),
                            ctx.get_resource_id(REF.BASE_USERS_GROUP.DATABASE_STRUCTURE_ADMIN),
                            ctx.get_resource_id(REF.BASE_USERS_GROUP.ACCESS_ADMIN),
                            ctx.get_resource_id(REF.BASE_USERS_GROUP.USERS_ADMIN),
                        ],
                    },
                },
            },
        },
    )

def build_database_structure(ctx: Lylac.TransactionContext):

    _build_models_structure(ctx)
    _create_permission_groups(ctx)
    _create_user_roles(ctx)
