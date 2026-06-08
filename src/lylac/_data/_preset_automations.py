from typing import TYPE_CHECKING
from .._constants import DATA_RESOURCE
from .._constants import FACTORY_FIELDS
from .._resources import AutomationProperties
from .._typing.generics import ModelName
from .._typing.literals import OnDeleteOption
from .._typing.literals import InitialModels
from .._typing.literals import TTypeName
from .._typing.generics import EngineHub
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._contexts import AutomationContext

def _base_model__register_model_on_automations(ctx: AutomationContext) -> None:

    # Iteración por cada registro de campo creado
    for record in ctx.records:

        # Obtención del nombre del modelo
        model_name = record['model']

        # Registro de modelo en automatizaciones y campos computados
        ctx.register_model(model_name)

def _base_model__create_model_table_in_database(ctx: AutomationContext) -> None:

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
        # Obtención del nombre de modelo
        model_name = record['name']
        # Obtención del modelo del modelo
        model_model_name = record['model']
        # Obtención de valor de si el modelo tiene secuencia
        has_sequence = record['has_sequence']
        # Obtención de valor de si el modelo permite archivar
        is_archivable = record['is_archivable']
        # Obtención de valor de si el modelo contiene leyenda
        has_label = record['has_label']
        # Creación de la clase del modelo
        ctx._ddl.create_model_table(ctx._execution_ctx.conn, model_name, model_model_name, has_sequence, is_archivable, has_label)

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

def _base_model__delete_model_table_in_database(ctx: AutomationContext) -> None:

    # Iteración por cada registro de modelo creado
    for record in ctx.records:
        # Obtención del nombre del modelo
        model_name = record['model']
        # Se elimina el modelo de los metadatos de Base
        ctx._ddl.delete_model_table(
            ctx._execution_ctx,
            model_name,
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

def _base_model_field__create_field_column(ctx: AutomationContext) -> None:

    # Iteración por cada registro de campo creado
    for record in ctx.records:

        # Obtención del nombre del campo
        field_name = record['name']
        # Obtención del tipo de dato del campo
        field_ttype: TTypeName = record['ttype']
        # Obtención del nombre del modelo
        model_name: ModelName = record['model_id.model']
        # Obtención del nombre de la tabla del modelo
        model_table_name: str = record['model_id.name']
        # Obtención de valor de nuleable
        nullable: bool = record['nullable']
        # Obtención de valor de único
        unique: bool = record['unique']
        # Obtención de valor predeterminado
        default_value: str = record['default_value']
        # Obtención del nombre de la tabla del modelo relacionado
        related_model_table_name: str = record['related_model_id.name']
        # Obtención de valor de en eliminación
        on_delete: OnDeleteOption = record['on_delete']

        # Se crea la instancia de campo en el modelo
        ctx._ddl.create_field_column(
            field_name,
            field_ttype,
            model_name,
            nullable,
            unique,
            default_value,
            related_model_table_name,
            on_delete,
        )

        # Se crea la columna en la tabla de la base de datos
        ctx._ddl.add_column_to_table(
            model_table_name,
            field_name,
            field_ttype,
            default_value,
            related_model_table_name,
            on_delete,
            ctx._execution_ctx.conn,
        )

def _base_model_field__update_instance_metadata(ctx: AutomationContext) -> None:

    # Actualización de los metadatos de la instancia
    ctx._execution_ctx.database_metadata.update(ctx._execution_ctx.conn)

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

        '_base_model__create_model_table_in_database': AutomationProperties(
            callback= _base_model__create_model_table_in_database,
            model_name= 'base.model',
            fields= ('name', 'model', 'has_sequence', 'is_archivable', 'has_label'),
            execute_only_when= [],
        ),

        '_base_model__register_model_on_automations': AutomationProperties(
            callback= _base_model__register_model_on_automations,
            model_name= 'base.model',
            fields= ('model',),
            execute_only_when= [],
        ),

        '_base_model__register_model_data': AutomationProperties(
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

        '_base_model_field__create_field_column': AutomationProperties(
            callback= _base_model_field__create_field_column,
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

        '_base_model_field__update_instance_metadata': AutomationProperties(
            callback= _base_model_field__update_instance_metadata,
            model_name= 'base.model.field',
            execute_only_when= [],
        ),

        '_base_model_field__create_m2m_relation': AutomationProperties(
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

        '_base_user_groups__register_model_data': AutomationProperties(
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
        '_base_users_role__register_model_data': AutomationProperties(
            callback= _base_users_role__register_model_data,
            model_name= 'base.users.role',
            fields= ('name',),
            execute_only_when= [],
        ),
    },

    'base.rules': {
        '_base_rules__register_model_data': AutomationProperties(
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

        '_base_model__delete_model_table_in_database': AutomationProperties(
            callback= _base_model__delete_model_table_in_database,
            model_name= 'base.model',
            fields= ('model',),
            execute_only_when= [],
        ),

    },

}
