from sqlalchemy.engine import Connection
from .._resources import DataMap
from .._resources import ModelDataIndex
from .._typing.definitions import _InternalModelSchema

def build_initial_data(conn: Connection) -> DataMap:

    # Inicialización de instancia de índice de datos de modelo
    model_data_index = ModelDataIndex(conn)

    model_data: list[_InternalModelSchema.base_model_data] = [
        # Usuarios
        {
            'name': 'base_users.root_user',
            'model_name': 'base.users',
        },
        {
            'name': 'base_users.admin_user',
            'model_name': 'base.users',
        },
        # Modelos
        {
            'name': 'base_model.base_users',
            'model_name': 'base.model',
        },
        {
            'name': 'base_model.base_model',
            'model_name': 'base.model',
        },
        {
            'name': 'base_model.base_model_field',
            'model_name': 'base.model',
        },
        {
            'name': 'base_model.base_model_field_selection',
            'model_name': 'base.model',
        },
        {
            'name': 'base_model.base_model_data',
            'model_name': 'base.model',
        },
        {
            'name': 'base_model.base_model_data_process',
            'model_name': 'base.model',
        },
        {
            'name': 'base_model.base_model_data_process_step',
            'model_name': 'base.model',
        },
        {
            'name': 'base_model.base_model_data_process_step_record',
            'model_name': 'base.model',
        },
        {
            'name': 'base_model.base_user_session',
            'model_name': 'base.model',
        },
        # Campos
        {
            'name': 'base_model_field.base_users__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__active',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__login',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__password',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_users__profile_picture',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__state',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__label',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__model',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__has_sequence',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__is_archivable',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__has_label',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__description',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__field_ids',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__related_field_ids',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model__transient',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__label',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__state',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__model_id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__ttype',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__nullable',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__on_delete',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__is_required',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__readonly',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__default_value',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__unique',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__help_info',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__related_model_id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__related_field',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__is_computed',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field__selection_ids',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__label',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_field_selection__field_id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__model_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data__res_id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process__step_ids',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__sequence',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__process_id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__model_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step__record_data_ids',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__step_id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__data',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__create_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__update_date',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__create_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__update_uid',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__display_name',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__user_id',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__validity_time',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field.base_user_session__expires_at',
            'model_name': 'base.model.field',
        },
        {
            'name': 'base_model_field_selection.base_model__state__base',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field_selection.base_model__state__generic',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field_selection.base_model__on_delete__set_null',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field_selection.base_model__on_delete__cascade',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field_selection.base_model__on_delete__restrict',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__integer',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__char',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__float',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__boolean',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__date',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__datetime',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__time',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__duration',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__file',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__text',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__selection',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__many2one',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__one2many',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__many2many',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field.base_model_field__ttype__json',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field_selection.base_model_field__state__base',
            'model_name': 'base.model.field.selection',
        },
        {
            'name': 'base_model_field_selection.base_model_field__state__generic',
            'model_name': 'base.model.field.selection',
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
            'model_name': 'base.users',
            'process_id': 1,
            'sequence': 1,
        },
        # 2
        {
            'model_name': 'base.model',
            'process_id': 2,
            'sequence': 1,
        },
        # 3
        {
            'model_name': 'base.model.field',
            'process_id': 2,
            'sequence': 2,
        },
        # 4
        {
            'model_name': 'base.model.field.selection',
            'process_id': 2,
            'sequence': 4,
        },
    ]

    records__base_users: list[_InternalModelSchema.base_model_data_step_record[_InternalModelSchema.base_users]] = [
        {
            'name': 'base_users.root_user',
            'step_id': 1,
            'sequence': 1,
            'data': {
                'login': 'iacele',
                'name': 'iaCele',
            },
        },
        {
            'name': 'base_users.admin_user',
            'step_id': 1,
            'sequence': 2,
            'data': {
                'login': 'onnymm',
                'name': 'Onnymm',
            },
        },
    ]

    records__base_model: list[_InternalModelSchema.base_model_data_step_record[_InternalModelSchema.base_model]] = [
        {
            'name': 'base_model.base_users',
            'step_id': 2,
            'sequence': 1,
            'data': {
                'name': 'base_users',
                'model': 'base.users',
                'label': 'Usuarios',
                'description': 'Usuarios de la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': 'base_model.base_model',
            'step_id': 2,
            'sequence': 2,
            'data': {
                'name': 'base_model',
                'model': 'base.model',
                'label': 'Modelos',
                'description': 'Modelos de la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': 'base_model.base_model_field',
            'step_id': 2,
            'sequence': 3,
            'data': {
                'name': 'base_model_field',
                'model': 'base.model.field',
                'label': 'Campos',
                'description': 'Campos de modelos de la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': 'base_model.base_model_field_selection',
            'step_id': 2,
            'sequence': 4,
            'data': {
                'name': 'base_model_field_selection',
                'model': 'base.model.field.selection',
                'label': 'Valores de selección',
                'description': 'Valores de selección de campos de modelos de la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': 'base_model.base_model_data',
            'step_id': 2,
            'sequence': 5,
            'data': {
                'name': 'base_model_data',
                'model': 'base.model.data',
                'label': 'Datos de modelos',
                'description': 'Datos de modelos y registros de toda la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': 'base_model.base_model_data_process',
            'step_id': 2,
            'sequence': 6,
            'data': {
                'name': 'base_model_data_process',
                'model': 'base.model.data.process',
                'label': 'Procesos de creación de datos de modelo',
                'description': 'Procesos de creación de datos iniciales de modelos en la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': 'base_model.base_model_data_process_step',
            'step_id': 2,
            'sequence': 7,
            'data': {
                'name': 'base_model_data_process_step',
                'model': 'base.model.data.process.step',
                'label': 'Pasos de procesos',
                'description': 'Pasos de procesos de creación de datos de modelos.',
                'has_sequence': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model.base_model_data_process_step_record',
            'step_id': 2,
            'sequence': 8,
            'data': {
                'name': 'base_model_data_process_step_record',
                'model': 'base.model.data.process.step.record',
                'label': 'Registros de datos de modelos',
                'description': 'Registros de datos de modelos a crear en la base de datos.',
                'state': 'base',
            },
        },
        {
            'name': 'base_model.base_user_session',
            'step_id': 2,
            'sequence': 9,
            'data': {
                'name': 'base_user_session',
                'model': 'base.user.session',
                'label': 'Registros de sesiones de usuario',
                'description': 'Registros de sesiones de usuario activas y expiradas.',
                'state': 'base',
            },
        },
    ]

    records__base_model_field: list[_InternalModelSchema.base_model_data_step_record[_InternalModelSchema.base_model_field]] = [
        {
            'name': 'base_model_field.base_users__id',
            'step_id': 3,
            'sequence': 10,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_users'),
                'unique': True,
                'state': 'base',
                },
        },
        {
            'name': 'base_model_field.base_users__name',
            'step_id': 3,
            'sequence': 20,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_users'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__create_date',
            'step_id': 3,
            'sequence': 30,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_users'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__update_date',
            'step_id': 3,
            'sequence': 40,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_users'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__create_uid',
            'step_id': 3,
            'sequence': 50,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_users'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__update_uid',
            'step_id': 3,
            'sequence': 60,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_users'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__display_name',
            'step_id': 3,
            'sequence': 70,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_users'),
                'is_computed': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__active',
            'step_id': 3,
            'sequence': 80,
            'data': {
                'name': 'active',
                'label': 'Activo',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_users'),
                'default_value': True,
                'nullable': False,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__login',
            'step_id': 3,
            'sequence': 90,
            'data': {
                'name': 'login',
                'label': 'Inicio de sesión',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_users'),
                'unique': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__password',
            'step_id': 3,
            'sequence': 100,
            'data': {
                'name': 'password',
                'label': 'Contraseña',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_users'),
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_users__profile_picture',
            'step_id': 3,
            'sequence': 110,
            'data': {
                'name': 'profile_picture',
                'label': 'Foto de perfil',
                'ttype': 'file',
                'model_id': model_data_index.encode('base_model.base_users'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__id',
            'step_id': 3,
            'sequence': 120,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model'),
                'unique': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__name',
            'step_id': 3,
            'sequence': 130,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__create_date',
            'step_id': 3,
            'sequence': 140,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__update_date',
            'step_id': 3,
            'sequence': 150,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__create_uid',
            'step_id': 3,
            'sequence': 160,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__update_uid',
            'step_id': 3,
            'sequence': 170,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__display_name',
            'step_id': 3,
            'sequence': 180,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model'),
                'is_computed': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__state',
            'step_id': 3,
            'sequence': 190,
            'data': {
                'name': 'state',
                'label': 'Tipo de campo',
                'ttype': 'selection',
                'model_id': model_data_index.encode('base_model.base_model'),
                'default_value': 'generic',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__label',
            'step_id': 3,
            'sequence': 200,
            'data': {
                'name': 'label',
                'label': 'Nombre visible',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model'),
                'is_required': True,
                'nullable': False,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__model',
            'step_id': 3,
            'sequence': 210,
            'data': {
                'name': 'model',
                'label': 'Referencia de modelo',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model'),
                'unique': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__has_sequence',
            'step_id': 3,
            'sequence': 220,
            'data': {
                'name': 'has_sequence',
                'label': 'Tiene secuencia',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model'),
                'readonly': True,
                'state': 'base',
                'default_value': False,
            },
        },
        {
            'name': 'base_model_field.base_model__is_archivable',
            'step_id': 3,
            'sequence': 221,
            'data': {
                'name': 'is_archivable',
                'label': 'Es archivable',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model'),
                'readonly': True,
                'state': 'base',
                'default_value': False,
            },
        },
        {
            'name': 'base_model_field.base_model__has_label',
            'step_id': 3,
            'sequence': 222,
            'data': {
                'name': 'has_label',
                'label': 'Tiene leyenda',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model'),
                'readonly': True,
                'state': 'base',
                'default_value': False,
            },
        },
        {
            'name': 'base_model_field.base_model__description',
            'step_id': 3,
            'sequence': 230,
            'data': {
                'name': 'description',
                'label': 'Descripción',
                'ttype': 'text',
                'model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model__field_ids',
            'step_id': 3,
            'sequence': 240,
            'data': {
                'name': 'field_ids',
                'label': 'Campos',
                'ttype': 'one2many',
                'model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
                'related_model_id': model_data_index.encode('base_model.base_model_field'),
                'related_field': 'model_id',
            },
        },
        {
            'name': 'base_model_field.base_model__related_field_ids',
            'step_id': 3,
            'sequence': 250,
            'data': {
                'name': 'related_field_ids',
                'label': 'Campos relacionados',
                'ttype': 'one2many',
                'model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
                'related_model_id': model_data_index.encode('base_model.base_model_field'),
                'related_field': 'related_model_id',
            },
        },
        {
            'name': 'base_model_field.base_model__transient',
            'step_id': 3,
            'sequence': 251,
            'data': {
                'name': 'transient',
                'label': 'Es modelo transitorio',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__id',
            'step_id': 3,
            'sequence': 260,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'unique': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__name',
            'step_id': 3,
            'sequence': 270,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__create_date',
            'step_id': 3,
            'sequence': 280,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__update_date',
            'step_id': 3,
            'sequence': 290,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__create_uid',
            'step_id': 3,
            'sequence': 300,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__update_uid',
            'step_id': 3,
            'sequence': 310,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__display_name',
            'step_id': 3,
            'sequence': 320,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'is_computed': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__state',
            'step_id': 3,
            'sequence': 330,
            'data': {
                'name': 'state',
                'label': 'Tipo de campo',
                'ttype': 'selection',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'default_value': 'generic',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__label',
            'step_id': 3,
            'sequence': 340,
            'data': {
                'name': 'label',
                'label': 'Nombre visible',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'is_required': True,
                'nullable': False,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field__model_id',
            'step_id': 3,
            'sequence': 350,
            'data': {
                'name': 'model_id',
                'label': 'Modelo',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'is_required': True,
                'nullable': False,
                'on_delete': 'cascade',
                'readonly': True,
                'related_model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype',
            'step_id': 3,
            'sequence': 360,
            'data': {
                'name': 'ttype',
                'label': 'Tipo de dato',
                'ttype': 'selection',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__nullable',
            'step_id': 3,
            'sequence': 370,
            'data': {
                'name': 'nullable',
                'label': 'Puede ser nulo',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'default_value': False,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__on_delete',
            'step_id': 3,
            'sequence': 380,
            'data': {
                'name': 'on_delete',
                'label': 'Cuando se elimina el registro padre',
                'ttype': 'selection',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'readonly': True,
                'default_value': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__is_required',
            'step_id': 3,
            'sequence': 390,
            'data': {
                'name': 'is_required',
                'label': 'Es requerido',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'default_value': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__readonly',
            'step_id': 3,
            'sequence': 400,
            'data': {
                'name': 'readonly',
                'label': 'Solo lectura',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'default_value': False,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__default_value',
            'step_id': 3,
            'sequence': 410,
            'data': {
                'name': 'default_value',
                'label': 'Valor predeterminado',
                'ttype': 'json',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__unique',
            'step_id': 3,
            'sequence': 420,
            'data': {
                'name': 'unique',
                'label': 'Único',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'default_value': False,
                'nullable': False,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__help_info',
            'step_id': 3,
            'sequence': 430,
            'data': {
                'name': 'help_info',
                'label': 'Información de ayuda',
                'ttype': 'text',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field__related_model_id',
            'step_id': 3,
            'sequence': 440,
            'data': {
                'name': 'related_model_id',
                'label': 'Modelo relacionado',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'related_model_id': model_data_index.encode('base_model.base_model'),
                'state': 'base',
                'on_delete': 'restrict',
                'readonly': True,
            }
        },
        {
            'name': 'base_model_field.base_model_field__related_field',
            'step_id': 3,
            'sequence': 450,
            'data': {
                'name': 'related_field',
                'label': 'Campo relacionado',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'state': 'base',
                'readonly': True,
            }
        },
        {
            'name': 'base_model_field.base_model_field__is_computed',
            'step_id': 3,
            'sequence': 460,
            'data': {
                'name': 'is_computed',
                'label': 'Es computado',
                'ttype': 'boolean',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'state': 'base',
                'readonly': True,
                'default_value': False,
            }
        },
        {
            'name': 'base_model_field.base_model_field__selection_ids',
            'step_id': 3,
            'sequence': 470,
            'data': {
                'name': 'selection_ids',
                'label': 'Valores de selección',
                'ttype': 'one2many',
                'model_id': model_data_index.encode('base_model.base_model_field'),
                'related_model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'related_field': 'field_id',
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field_selection__id',
            'step_id': 3,
            'sequence': 480,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'unique': True,
                'state': 'base',
                },
        },
        {
            'name': 'base_model_field.base_model_field_selection__name',
            'step_id': 3,
            'sequence': 490,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field_selection__create_date',
            'step_id': 3,
            'sequence': 500,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field_selection__update_date',
            'step_id': 3,
            'sequence': 510,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field_selection__create_uid',
            'step_id': 3,
            'sequence': 520,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field_selection__update_uid',
            'step_id': 3,
            'sequence': 530,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field_selection__display_name',
            'step_id': 3,
            'sequence': 540,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'is_computed': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_field_selection__label',
            'step_id': 3,
            'sequence': 550,
            'data': {
                'name': 'label',
                'label': 'Nombre visible',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'is_required': True,
                'nullable': False,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_field_selection__field_id',
            'step_id': 3,
            'sequence': 560,
            'data': {
                'name': 'field_id',
                'label': 'Campo',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_field_selection'),
                'related_model_id': model_data_index.encode('base_model.base_model_field'),
                'on_delete': 'cascade',
                'is_required': True,
                'readonly': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_data__id',
            'step_id': 3,
            'sequence': 570,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'unique': True,
                'state': 'base',
                },
        },
        {
            'name': 'base_model_field.base_model_data__name',
            'step_id': 3,
            'sequence': 580,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data__create_date',
            'step_id': 3,
            'sequence': 590,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data__update_date',
            'step_id': 3,
            'sequence': 600,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data__create_uid',
            'step_id': 3,
            'sequence': 610,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data__update_uid',
            'step_id': 3,
            'sequence': 620,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data__display_name',
            'step_id': 3,
            'sequence': 630,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'is_computed': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_data__model_name',
            'step_id': 3,
            'sequence': 640,
            'data': {
                'name': 'model_name',
                'label': 'Nombre del modelo',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'is_required': True,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data__res_id',
            'step_id': 3,
            'sequence': 650,
            'data': {
                'name': 'res_id',
                'label': 'ID de recurso',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model_data'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process__id',
            'step_id': 3,
            'sequence': 660,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model_data_process'),
                'unique': True,
                'state': 'base',
                },
        },
        {
            'name': 'base_model_field.base_model_data_process__name',
            'step_id': 3,
            'sequence': 670,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data_process'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process__create_date',
            'step_id': 3,
            'sequence': 680,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_data_process'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process__update_date',
            'step_id': 3,
            'sequence': 690,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_data_process'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process__create_uid',
            'step_id': 3,
            'sequence': 700,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data_process'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process__update_uid',
            'step_id': 3,
            'sequence': 710,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data_process'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process__display_name',
            'step_id': 3,
            'sequence': 720,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data_process'),
                'is_computed': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_data_process__step_ids',
            'step_id': 3,
            'sequence': 730,
            'data': {
                'name': 'step_ids',
                'label': 'Pasos de proceso',
                'ttype': 'one2many',
                'model_id': model_data_index.encode('base_model.base_model_data_process'),
                'related_model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'related_field': 'process_id',
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__id',
            'step_id': 3,
            'sequence': 740,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'unique': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__name',
            'step_id': 3,
            'sequence': 750,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__create_date',
            'step_id': 3,
            'sequence': 760,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__update_date',
            'step_id': 3,
            'sequence': 770,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__create_uid',
            'step_id': 3,
            'sequence': 780,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__update_uid',
            'step_id': 3,
            'sequence': 790,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__display_name',
            'step_id': 3,
            'sequence': 800,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'is_computed': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_data_process_step__sequence',
            'step_id': 3,
            'sequence': 810,
            'data': {
                'name': 'sequence',
                'label': 'Secuencia',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__process_id',
            'step_id': 3,
            'sequence': 820,
            'data': {
                'name': 'process_id',
                'label': 'Proceso',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'related_model_id': model_data_index.encode('base_model.base_model_data_process'),
                'on_delete': 'cascade',
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__model_name',
            'step_id': 3,
            'sequence': 830,
            'data': {
                'name': 'model_name',
                'label': 'Modelo',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step__record_data_ids',
            'step_id': 3,
            'sequence': 840,
            'data': {
                'name': 'record_data_ids',
                'label': 'Registros',
                'ttype': 'one2many',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step'),
                'related_model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'related_field': 'step_id',
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__id',
            'step_id': 3,
            'sequence': 850,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'unique': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__name',
            'step_id': 3,
            'sequence': 860,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__create_date',
            'step_id': 3,
            'sequence': 870,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__update_date',
            'step_id': 3,
            'sequence': 880,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__create_uid',
            'step_id': 3,
            'sequence': 890,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__update_uid',
            'step_id': 3,
            'sequence': 900,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__display_name',
            'step_id': 3,
            'sequence': 910,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'is_computed': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__step_id',
            'step_id': 3,
            'sequence': 920,
            'data': {
                'name': 'step_id',
                'label': 'Paso',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'on_delete': 'cascade',
                'state': 'base',
                'related_model_id': model_data_index.encode('base_model.base_model_data_process_step')
            },
        },
        {
            'name': 'base_model_field.base_model_data_process_step_record__data',
            'step_id': 3,
            'sequence': 930,
            'data': {
                'name': 'data',
                'label': 'Datos',
                'ttype': 'json',
                'model_id': model_data_index.encode('base_model.base_model_data_process_step_record'),
                'is_required': True,
                'nullable': False,
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__id',
            'step_id': 3,
            'sequence': 940,
            'data': {
                'name': 'id',
                'label': 'ID',
                'ttype': 'integer',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'unique': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__name',
            'step_id': 3,
            'sequence': 950,
            'data': {
                'name': 'name',
                'label': 'Nombre',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__create_date',
            'step_id': 3,
            'sequence': 960,
            'data': {
                'name': 'create_date',
                'label': 'Fecha de creación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__update_date',
            'step_id': 3,
            'sequence': 970,
            'data': {
                'name': 'update_date',
                'label': 'Fecha de modificación',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__create_uid',
            'step_id': 3,
            'sequence': 980,
            'data': {
                'name': 'create_uid',
                'label': 'Usuario de creación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__update_uid',
            'step_id': 3,
            'sequence': 990,
            'data': {
                'name': 'update_uid',
                'label': 'Usuario de modificación',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'restrict',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__display_name',
            'step_id': 3,
            'sequence': 1000,
            'data': {
                'name': 'display_name',
                'label': 'Nombre a mostrar',
                'ttype': 'char',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'is_computed': True,
                'state': 'base',
            }
        },
        {
            'name': 'base_model_field.base_user_session__user_id',
            'step_id': 3,
            'sequence': 1010,
            'data': {
                'name': 'user_id',
                'label': 'Usuario',
                'ttype': 'many2one',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'related_model_id': model_data_index.encode('base_model.base_users'),
                'on_delete': 'cascade',
                'readonly': True,
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__validity_time',
            'step_id': 3,
            'sequence': 1020,
            'data': {
                'name': 'validity_time',
                'label': 'Tiempo de validez',
                'ttype': 'duration',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'state': 'base',
            },
        },
        {
            'name': 'base_model_field.base_user_session__expires_at',
            'step_id': 3,
            'sequence': 1030,
            'data': {
                'name': 'expires_at',
                'label': 'Expira el',
                'ttype': 'datetime',
                'model_id': model_data_index.encode('base_model.base_user_session'),
                'is_computed': True,
                'state': 'base',
            },
        },
    ]

    records__base_model_field_selection: list[_InternalModelSchema.base_model_data_step_record[_InternalModelSchema.base_model_field_selection]] = [
        {
            'name': 'base_model_field_selection.base_model__state__base',
            'step_id': 4,
            'sequence': 5,
            'data': {
                'name': 'base',
                'label': 'Base',
                'field_id': model_data_index.encode('base_model_field.base_model__state'),
            },
        },
        {
            'name': 'base_model_field_selection.base_model__state__generic',
            'step_id': 4,
            'sequence': 10,
            'data': {
                'name': 'generic',
                'label': 'Personalizado',
                'field_id': model_data_index.encode('base_model_field.base_model__state'),
            },
        },
        {
            'name': 'base_model_field_selection.base_model__on_delete__set_null',
            'step_id': 4,
            'sequence': 15,
            'data': {
                'name': 'set_null',
                'label': 'Establecer como nulo',
                'field_id': model_data_index.encode('base_model_field.base_model_field__on_delete'),
            },
        },
        {
            'name': 'base_model_field_selection.base_model__on_delete__cascade',
            'step_id': 4,
            'sequence': 20,
            'data': {
                'name': 'cascade',
                'label': 'Eliminar en cascada',
                'field_id': model_data_index.encode('base_model_field.base_model_field__on_delete'),
            },
        },
        {
            'name': 'base_model_field_selection.base_model__on_delete__restrict',
            'step_id': 4,
            'sequence': 25,
            'data': {
                'name': 'restrict',
                'label': 'Restringir eliminación',
                'field_id': model_data_index.encode('base_model_field.base_model_field__on_delete'),
            },
        },
        {
            'name': 'base_model_field.base_model_field__ttype__integer',
            'step_id': 4,
            'sequence': 30,
            'data': {
                'name': 'integer',
                'label': 'Entero',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__char',
            'step_id': 4,
            'sequence': 35,
            'data': {
                'name': 'char',
                'label': 'Caracter',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__float',
            'step_id': 4,
            'sequence': 40,
            'data': {
                'name': 'float',
                'label': 'Flotante',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__boolean',
            'step_id': 4,
            'sequence': 45,
            'data': {
                'name': 'boolean',
                'label': 'Booleano',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__date',
            'step_id': 4,
            'sequence': 50,
            'data': {
                'name': 'date',
                'label': 'Fecha',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__datetime',
            'step_id': 4,
            'sequence': 55,
            'data': {
                'name': 'datetime',
                'label': 'Fecha y hora',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__time',
            'step_id': 4,
            'sequence': 60,
            'data': {
                'name': 'time',
                'label': 'Hora',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__duration',
            'step_id': 4,
            'sequence': 65,
            'data': {
                'name': 'duration',
                'label': 'Duración',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__file',
            'step_id': 4,
            'sequence': 70,
            'data': {
                'name': 'file',
                'label': 'Binario',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__text',
            'step_id': 4,
            'sequence': 75,
            'data': {
                'name': 'text',
                'label': 'Texto largo',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__selection',
            'step_id': 4,
            'sequence': 80,
            'data': {
                'name': 'selection',
                'label': 'Selección',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__many2one',
            'step_id': 4,
            'sequence': 85,
            'data': {
                'name': 'many2one',
                'label': 'Muchos a uno',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__one2many',
            'step_id': 4,
            'sequence': 90,
            'data': {
                'name': 'one2many',
                'label': 'Uno a muchos',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__many2many',
            'step_id': 4,
            'sequence': 95,
            'data': {
                'name': 'many2many',
                'label': 'Muchos a muchos',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field.base_model_field__ttype__json',
            'step_id': 4,
            'sequence': 100,
            'data': {
                'name': 'json',
                'label': 'JSON',
                'field_id': model_data_index.encode('base_model_field.base_model_field__ttype')
            }
        },
        {
            'name': 'base_model_field_selection.base_model_field__state__base',
            'step_id': 4,
            'sequence': 105,
            'data': {
                'name': 'base',
                'label': 'Base',
                'field_id': model_data_index.encode('base_model_field.base_model_field__state'),
            }
        },
        {
            'name': 'base_model_field_selection.base_model_field__state__generic',
            'step_id': 4,
            'sequence': 110,
            'data': {
                'name': 'generic',
                'label': 'Personalizado',
                'field_id': model_data_index.encode('base_model_field.base_model_field__state'),
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
