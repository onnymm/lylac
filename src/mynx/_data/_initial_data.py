from typing import TYPE_CHECKING
from .._constants import DATA_RESOURCE

if TYPE_CHECKING:
    from .._main import Lylac

# Grupos de permisos
def _create_permission_groups(ctx: Lylac.TransactionContext):

    ctx.create(
        'base.user.groups',
        [
            # Permisos básicos
            {
                'name': 'basic_permissions',
                'label': 'Permisos básicos',
                'access_ids': {
                    'create': [
                        {
                            'name': 'base_users__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USERS),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_model__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_model_field__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_FIELD),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_model_field_selection__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_FIELD_SELECTION),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_model_data__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_DATA),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_model_data_process__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_DATA_PROCESS),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_model_data_process_step__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_model_data_process_step_record__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_user_session__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_SESSION),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_user_access__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_ACCESS),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_user_groups__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_GROUPS),
                            'perm_read': True,
                        },
                        {
                            'name': 'base_users_role__user',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USERS_ROLE),
                            'perm_read': True,
                        },
                    ],
                },
            },
            # Administrador de la estructura de la base de datos
            {
                'name': 'database_structure_admin',
                'label': 'Administrador de la estructura de la base de datos',
                'access_ids': {
                    'create': [
                        {
                            'name': 'base_model__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_model__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_FIELD),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_model__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_FIELD_SELECTION),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_model_data__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_DATA),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_model_data_process__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_DATA_PROCESS),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_model_data_process_step__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_DATA_PROCESS_STEP),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_model_data_process_step_record__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL_DATA_PROCESS_STEP_RECORD),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                    ],
                },
            },
            # Administrador de permisos de usuarios
            {
                'name': 'access_admin',
                'label': 'Administrador de permisos de usuarios',
                'access_ids': {
                    'create': [
                        {
                            'name': 'base_user_access__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_ACCESS),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_user_groups__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_GROUPS),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_users_role__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USERS_ROLE),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_rules__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_RULES),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                    ],
                },
            },
            # Administrador de usuarios
            {
                'name': 'users_admin',
                'label': 'Administrador de usuarios',
                'access_ids': {
                    'create': [
                        {
                            'name': 'base_users__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USERS),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'base_users__admin',
                            'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_SESSION),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                    ]
                }
            },
        ],
    )

# Modelos, campos y valores de selección
def _build_models_structure(ctx: Lylac.TransactionContext):

    ctx.create(
        'base.model',
        [
            # Creación de modelo de grupos de acceso
            {
                'name': 'base_user_groups',
                'model': 'base.user.groups',
                'label': 'Grupos de acceso',
                'description': 'Registros de grupos de acceso.',
                'has_label': True,
            },
            # Creación de modelo de reglas de registro
            {
                'name': 'base_rules',
                'model': 'base.rules',
                'label': 'Reglas de registro',
                'description': 'Reglas de registro para definir dominios de transacciones.',
                'is_archivable': True,
                'has_label': True,
                'field_ids': {
                    'create': [
                        {
                            'name': 'domain',
                            'label': 'Dominio',
                            'ttype': 'text',
                            'is_required': True,
                            'nullable': False,
                        },
                        {
                            'name': 'model_id',
                            'label': 'Modelo',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL),
                            'on_delete': 'cascade',
                            'is_required': True,
                            'nullable': False,
                        },
                        {
                            'name': 'perm_create',
                            'label': 'Permiso de creación',
                            'ttype': 'boolean',
                            'default_value': False,
                        },
                        {
                            'name': 'perm_read',
                            'label': 'Permiso de lectura',
                            'ttype': 'boolean',
                            'default_value': False,
                        },
                        {
                            'name': 'perm_update',
                            'label': 'Permiso de modificación',
                            'ttype': 'boolean',
                            'default_value': False,
                        },
                        {
                            'name': 'perm_delete',
                            'label': 'Permiso de eliminación',
                            'ttype': 'boolean',
                            'default_value': False,
                        },
                        {
                            'name': 'global',
                            'label': 'Global',
                            'ttype': 'boolean',
                            'default_value': False,
                            'nullable': False,
                        },
                    ],
                }
            }
        ]
    )

    ctx.create(
        'base.model',
        [
            # Creación de modelo de permisos de acceso
            {
                'name': 'base_user_access',
                'model': 'base.user.access',
                'label': 'Permisos de acceso',
                'description': 'Registros de permisos de acceso granulares.',
                'field_ids': {
                    'create': [
                        {
                            'name': 'model_id',
                            'label': 'Modelo',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_MODEL),
                            'on_delete': 'cascade',
                            'nullable': False,
                            'is_required': True,
                            'readonly': True,
                        },
                        {
                            'name': 'perm_create',
                            'label': 'Permiso de creación',
                            'ttype': 'boolean',
                            'default_value': False,
                        },
                        {
                            'name': 'perm_read',
                            'label': 'Permiso de lectura',
                            'ttype': 'boolean',
                            'default_value': False,
                        },
                        {
                            'name': 'perm_update',
                            'label': 'Permiso de modificación',
                            'ttype': 'boolean',
                            'default_value': False,
                        },
                        {
                            'name': 'perm_delete',
                            'label': 'Permiso de eliminación',
                            'ttype': 'boolean',
                            'default_value': False,
                        },
                        {
                            'name': 'group_id',
                            'label': 'Grupo',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_GROUPS),
                            'on_delete': 'cascade',
                            'is_required': True,
                            'nullable': False,
                        },
                    ]
                }
            },
            # Creación de modelo de sesiones de usuario
            {
                'name': 'base_users_role',
                'model': 'base.users.role',
                'label': 'Roles de usuario',
                'has_label': True,
                'field_ids': {
                    'create': {
                        'name': 'group_ids',
                        'label': 'Grupos',
                        'ttype': 'many2many',
                        'related_model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_GROUPS),
                    },
                },
            },
        ],
    )

    ctx.update(
        'base.model',
        ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_GROUPS),
        {
            'field_ids': {
                'create': {
                    'name': 'access_ids',
                    'label': 'Accesos',
                    'ttype': 'one2many',
                    'related_model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_ACCESS),
                    'related_field': 'group_id',
                },
            },
        },
    )

    ctx.create(
        'base.model.field',
        [
            # Creación de campo de roles del usuario en modelo de usuarios
            {
                'name': 'role_ids',
                'label': 'Roles',
                'ttype': 'many2many',
                'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USERS),
                'related_model_id': ctx.get_resource_id('base_model.base_users_role'),
            },
            # Creación de campo de reglas de registro en modelo de grupos de acceso
            {
                'name': 'rule_ids',
                'label': 'Reglas de registro',
                'ttype': 'many2many',
                'model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_USER_GROUPS),
                'related_model_id': ctx.get_resource_id(DATA_RESOURCE.MODEL.BASE_RULES)
            },
        ],
    )

# Roles de usuario
def _create_user_roles(ctx: Lylac.TransactionContext):

    # Creación de rol de super usuario
    ctx.update(
        'base.users',
        ctx.get_resource_id(DATA_RESOURCE.ROOT_USER),
        {
            'role_ids': {
                'create': {
                    'name': 'root_user',
                    'label': 'Superusuario',
                    'group_ids': {
                        'add': [
                            ctx.get_resource_id('base_user_groups.basic_permissions'),
                            ctx.get_resource_id('base_user_groups.database_structure_admin'),
                            ctx.get_resource_id('base_user_groups.access_admin'),
                            ctx.get_resource_id('base_user_groups.users_admin'),
                        ],
                    },
                },
            },
        },
    )

    # Creación de rol de administrador de la base de datos
    ctx.update(
        'base.users',
        ctx.get_resource_id(DATA_RESOURCE.ADMIN_USER),
        {
            'role_ids': {
                'create': {
                    'name': 'database_admin',
                    'label': 'Administrador de la base de datos',
                    'group_ids': {
                        'add': [
                            ctx.get_resource_id('base_user_groups.basic_permissions'),
                            ctx.get_resource_id('base_user_groups.database_structure_admin'),
                            ctx.get_resource_id('base_user_groups.access_admin'),
                            ctx.get_resource_id('base_user_groups.users_admin'),
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
