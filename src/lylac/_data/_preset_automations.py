from typing import TYPE_CHECKING
from .._constants import DATA_RESOURCE
from .._constants import FACTORY_FIELDS
from .._constants import PRESET
from .._resources import AutomationProperties
from .._typing.generics import EngineHub
from .._typing.generics import ModelName
from .._typing.literals import InitialModels

if TYPE_CHECKING:
    from .._contexts import AutomationContext

def _base_model__register_model_on_engines(ctx: AutomationContext) -> None:

    # Iteración por cada registro de campo creado
    for record in ctx.records:
        # Obtención del nombre del modelo
        model_name = record['model']
        # Registro de modelo en automatizaciones y campos computados
        ctx.register_model(model_name)

def _base_model__create_model_and_table_in_database(ctx: AutomationContext) -> None:

    # Evaluación del tipo de campo en base a quién lo crea
    field_state = (
        'base'
            if ctx.uid == ctx.get_resource_id(DATA_RESOURCE.ROOT_USER)
            else 'generic'
    )

    # Iteración por cada registro de modelo creado
    for record in ctx.records:
        # Obtención de la ID de modelo
        model_id = record['id']
        # Obtención de valor de si el modelo tiene secuencia
        has_sequence = record['has_sequence']
        # Obtención de valor de si el modelo permite archivar
        is_archivable = record['is_archivable']
        # Obtención de valor de si el modelo contiene leyenda
        has_label = record['has_label']

        # Creación del modelo
        ctx.action(
            'base.model',
            PRESET.AUTOMATION.BASE_MODEL__CREATE_TABLE_ON_DATABASE,
            model_id,
        )

        # Inicialización de datos de campos a crear
        fields_to_create = [
            {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_id,
                'unique': True,
                'state': field_state,
            },
            {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_id,
                'state': field_state,
            },
            {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_id,
                'state': field_state,
            },
            {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_id,
                'state': field_state,
            },
            {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_id,
                'related_model_id': ctx.get_resource_id('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': field_state,
            },
            {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_id,
                'related_model_id': ctx.get_resource_id('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': field_state,
            },
            {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_id,
                'state': field_state,
                'is_computed': True
            },
        ]

        # Si el modelo tiene secuencia...
        if has_sequence:
            # Se añade campo de secuencia
            fields_to_create.append({
                'name': 'sequence',
                'label': 'Secuencia',
                'ttype': 'integer',
                'nullable': False,
                'model_id': model_id,
                'is_required': True,
            })
        # Si el modelo tiene leyenda...
        if has_label:
            # Se añade campo de leyenda
            fields_to_create.append({
                'name': 'label',
                'label': 'Leyenda',
                'ttype': 'char',
                'nullable': False,
                'model_id': model_id,
                'state': field_state,
            })
        # Si el modelo permite archivar
        if is_archivable:
            fields_to_create.append({
                'name': 'active',
                'label': 'Activo',
                'ttype': 'boolean',
                'default_value': True,
                'model_id': model_id,
                'state': field_state,
            })

        # Creación de los campos predeterminados que todo modelo debe tener
        ctx.create(
            'base.model.field',
            fields_to_create
        )

        # Actualización de los metadatos de la instancia
        ctx._execution_ctx.database_metadata.update(ctx._execution_ctx.conn)

def _base_model__drop_table(ctx: AutomationContext) -> None:

    # Iteración por cada registro de modelo creado
    for record in ctx.records:
        # Eliminación del modelo
        ctx.action(
            'base.model',
            PRESET.AUTOMATION.BASE_MODEL__DROP_TABLE,
            record['id'],
        )

    # Actualización de los metadatos de la instancia
    ctx._execution_ctx.database_metadata.update(ctx._execution_ctx.conn)

def _base_model_field__create_m2m_relation(ctx: AutomationContext) -> None:

    # Iteración por cada registro de campo creado
    for record in ctx.records:

        # Obtención del nombre del campo
        field_name = record['name']
        # Obtención del nombre del modelo del campo
        field_model_name: ModelName = record['model_id.model']
        # Obtención del nombre de la tabla del modelo relacionado del campo
        field_related_model_table_name: str = record['related_model_id.name']

        # Creación del modelo de relación many2many
        ctx._ddl.create_m2m_relation_table(
            ctx._execution_ctx.conn,
            field_name,
            field_model_name,
            field_related_model_table_name,
        )

def _base_model_field__create_column_and_register_field(ctx: AutomationContext) -> None:

    # Iteración por cada registro de campo creado
    for record in ctx.records:

        # Creación de la columna en la tabla
        ctx.action(
            'base.model.field',
            PRESET.AUTOMATION.BASE_MODEL_FIELD__CREATE_COLUMN,
            record['id'],
        )
        # Registro de la instancia en el modelo
        ctx.action(
            'base.model.field',
            PRESET.AUTOMATION.BASE_MODEL_FIELD__REGISTER_ON_MODEL,
            record['id'],
        )

    # Actualización de los metadatos de la instancia
    ctx.task(PRESET.SERVER_TASK.UPDATE_INSTANCE_METADATA)

def _base_model_field__restore_parent_model_structure(ctx: AutomationContext) -> None:

    # Inicialización de conjunto de IDs de modelos
    model_ids = set()

    # Iteración por cada registro de campo creado
    for record in ctx.records:
        # Obtención de la ID de modelo a la que pertenecía el campo
        model_id = record['model_id.id']
        # Obtención del nombre del campo
        field_name = record['name']
        # Obtención del nombre de la tabla del modelo
        table_name = record['model_id.name']
        # Se añade la ID de modelo al conjunto
        model_ids.add(model_id)

        ctx._ddl.drop_column(ctx._execution_ctx.conn, table_name, field_name)

    # Iteración por cada ID de modelo a restaurar
    for model_id in model_ids:
        # Eliminación del modelo únicamente de los metadatos de SQLAlchemy
        ctx.action(
            'base.model',
            PRESET.AUTOMATION.BASE_MODEL__DELETE_MODEL,
            model_id,
        )
        # Restauración del modelo con los campos restantes
        ctx.action(
            'base.model',
            PRESET.AUTOMATION.BASE_MODEL__RESTORE,
            model_id,
        )

    # Actualización de los metadatos de la instancia
    ctx.task(PRESET.SERVER_TASK.UPDATE_INSTANCE_METADATA)

def _base_model__register_model_data(ctx: AutomationContext) -> None:

    # Inicialización de lista de registros a crear
    data_to_create: list[dict] = []

    # Iteración por cada registro creado
    for record in ctx.records:
        # Creación de los datos de registro de modelo
        new_record = {
            'res_id': record['res_id'],
            'name': record['name'],
            'model_name': 'base.model',
        }
        # Se añade éste a la lista de registros a crear
        data_to_create.append(new_record)

    # Creación de registros
    ctx.create('base.model.data', data_to_create)

def _base_users_role__register_model_data(ctx: AutomationContext) -> None:

    # Inicialización de lista de registros a crear
    data_to_create: list[dict] = []

    # Iteración por cada registro creado
    for record in ctx.records:
        # Obtención de ID del registro
        record_id = record['id']
        # Obtención del nombre del rol
        name = record['name']

        # Creación de los datos de registro de modelo
        new_record = {
            'res_id': record_id,
            'name': f'base_users_role.{name}',
            'model_name': 'base.users.role',
        }

        # Se añade éste a la lista de registros a crear
        data_to_create.append(new_record)

    # Creación de registros
    ctx.create('base.model.data', data_to_create)

def _base_user_groups__register_model_data(ctx: AutomationContext) -> None:

    # Inicialización de lista de registros a crear
    data_to_create: list[dict] = []

    # Iteración por cada registro creado
    for record in ctx.records:
        # Obtención de ID del registro
        record_id = record['res_id']
        # Obtención del nombre del grupo
        name = record['name']
        # Creación de los datos de registro de modelo
        new_record = {
            'res_id': record_id,
            'name': f'base_user_groups.{name}',
            'model_name': 'base.user.groups',
        }
        # Se añade éste a la lista de registros a crear
        data_to_create.append(new_record)

    # Creación de registros
    ctx.create('base.model.data', data_to_create)

def _base_rules__register_model_data(ctx: AutomationContext):

    # Inicialización de lista de registros a crear
    data_to_create: list[dict] = []

    # Iteración por cada registro creado
    for record in ctx.records:
        # Obtención de ID del registro
        record_id = record['id']
        # Obtención del nombre del grupo
        name = record['name']
        # Obtención del nombre de tabla del modelo
        model_table_name = record['model_table_name']

        # Creación de los datos de registro de modelo
        new_record = {
            'res_id': record_id,
            'name': f'base_rules.{model_table_name}__{name}',
            'model_name': 'base.rules',
        }
        # Se añade éste a la lista de registros a crear
        data_to_create.append(new_record)

    # Creación de registros
    ctx.create('base.model.data', data_to_create)

DEFAULT_ON_CREATE_AUTOMATIONS: EngineHub[InitialModels, AutomationProperties[InitialModels]] = {

    'base.model': {

        _base_model__create_model_and_table_in_database.__name__: AutomationProperties(
            callback= _base_model__create_model_and_table_in_database,
            model_name= 'base.model',
            fields= ('name', 'model', 'has_sequence', 'is_archivable', 'has_label'),
            execute_only_when= [],
        ),

        _base_model__register_model_on_engines.__name__: AutomationProperties(
            callback= _base_model__register_model_on_engines,
            model_name= 'base.model',
            fields= ('model',),
            execute_only_when= [],
        ),

        _base_model__register_model_data.__name__: AutomationProperties(
            callback= _base_model__register_model_data,
            model_name= 'base.model',
            fields= (
                ('id', 'res_id'),
                ('name', 'char', lambda ctx: ctx.concat('base_model.', ctx['name'])),
            ),
            execute_only_when= [],
        ),

    },

    'base.model.field': {

        _base_model_field__create_column_and_register_field.__name__: AutomationProperties(
            callback= _base_model_field__create_column_and_register_field,
            model_name= 'base.model.field',
            fields= (
                'name',
                'ttype',
                'nullable',
                'default_value',
                'unique',
                'model_id.model',
                'model_id.name',
                'related_model_id.name',
                'on_delete',
            ),
            execute_only_when= [
                '&',
                    '&',
                        ('name', 'not in', FACTORY_FIELDS),
                        ('ttype', 'not in', ['one2many', 'many2many']),
                    ('is_computed', '=', False),
            ],
        ),

        _base_model_field__create_m2m_relation.__name__: AutomationProperties(
            callback= _base_model_field__create_m2m_relation,
            model_name= 'base.model.field',
            fields= (
                'name',
                'model_id.model',
                'related_model_id.name',
            ),
            execute_only_when= [('ttype', '=', 'many2many')],
        ),

    },

    'base.user.groups': {

        _base_user_groups__register_model_data.__name__: AutomationProperties(
            callback= _base_user_groups__register_model_data,
            model_name= 'base.user.groups',
            fields= (
                'name',
                ('id', 'res_id'),
            ),
            execute_only_when= [],
        ),

    },

    'base.users.role': {

        _base_users_role__register_model_data.__name__: AutomationProperties(
            callback= _base_users_role__register_model_data,
            model_name= 'base.users.role',
            fields= ('name',),
            execute_only_when= [],
        ),

    },

    'base.rules': {

        _base_rules__register_model_data.__name__: AutomationProperties(
            callback= _base_rules__register_model_data,
            model_name= 'base.rules',
            fields= (
                'name',
                ('model_table_name', 'char', lambda ctx: ctx['model_id.name']),
            ),
            execute_only_when= [],
        ),

    },

}

DEFAULT_ON_UPDATE_AUTOMATIONS: EngineHub[InitialModels, AutomationProperties[InitialModels]] = {}

DEFAULT_ON_DELETE_AUTOMATIONS: EngineHub[InitialModels, AutomationProperties[InitialModels]] = {

    'base.model': {

        _base_model__drop_table.__name__: AutomationProperties(
            callback= _base_model__drop_table,
            model_name= 'base.model',
            fields= ('model',),
            execute_only_when= [],
        ),

    },

    'base.model.field': {

        _base_model_field__restore_parent_model_structure.__name__: AutomationProperties(
            callback= _base_model_field__restore_parent_model_structure,
            model_name= 'base.model.field',
            fields= ('model_id.id', 'model_id.name', 'name'),
            execute_only_when= [],
        ),

    },

}
