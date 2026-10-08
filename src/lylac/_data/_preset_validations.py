import re
from typing import TYPE_CHECKING
from .._constants import CRUD_METHOD_NAME
from .._constants import MODEL_NAME
from .._constants import FIELD_NAME
from .._constants import TTYPE_NAME
from .._resources import ValidationProperties
from .._typing.definitions import _InternalModelSchema
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._contexts import ValidationContext

def _validation__reject_id_values(ctx: 'ValidationContext') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo de ID se encuentra en los datos...
        if FIELD_NAME.ID in record:
            # Se captura el registro
            ctx.catch(record)

def _validation__reject_create_and_update_date_values(ctx: 'ValidationContext') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo de ID se encuentra en los datos...
        if FIELD_NAME.CREATE_DATE in record or FIELD_NAME.UPDATE_DATE in record:
            # Se captura el registro
            ctx.catch(record)

def _validation__reject_create_and_update_user_values(ctx: 'ValidationContext') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo de ID se encuentra en los datos...
        if FIELD_NAME.CREATE_UID in record or FIELD_NAME.UPDATE_UID in record:
            # Se captura el registro
            ctx.catch(record)

def _validation__confirm_required_fields(ctx: 'ValidationContext') -> None:

    # Búsqueda de los campos requeridos del modelo
    found_data = ctx.search_read(
        MODEL_NAME.BASE_MODEL_FIELD,
        [
            '&',
                ('is_required', '=', True),
                ('model_id.model', '=', ctx.model_name),
        ],
        ['name'],
    )

    # Construcción de lista de campos requeridos
    required_fields = [record['name'] for record in found_data]

    # Iteración por cada registro
    for record in ctx.records:
        # Iteración por cada campo requerido
        for field_name in required_fields:
            # Si el campo no está en los datos...
            if field_name not in record:
                # Se captura el registro con el campo faltante
                ctx.catch(record, field_name)

def _validation__prevent_update_on_readonly_fields(ctx: 'ValidationContext') -> None:

    # Búsqueda de los campos de solo lectura del modelo
    found_data = ctx.search_read(
        MODEL_NAME.BASE_MODEL_FIELD,
        [
            '&',
                ('readonly', '=', True),
                ('model_id.model', '=', ctx.model_name),
        ],
        ['name'],
    )

    # Construcción de lista de campos de solo lectura
    readonly_fields = [record['name'] for record in found_data]

    # Iteración por cada registro
    for record in ctx.records:
        # Iteración por cada campo de solo lectura
        for field_name in readonly_fields:
            # Si el campo está en los datos...
            if field_name in record:
                # Se captura el registro con el campo de solo lectura
                ctx.catch(record, field_name)

def _validation__prevent_create_or_update_on_computed_fields(ctx: 'ValidationContext') -> None:

    # Búsqueda de los campos computados
    found_data = ctx.search_read(
        MODEL_NAME.BASE_MODEL_FIELD,
        [
            '&',
                ('is_computed', '=', True),
                ('model_id.model', '=', ctx.model_name),
        ],
        ['name'],
    )

    # Construcción de lista de campos computados
    computed_fields = [record['name'] for record in found_data]

    # Iteración por cada registro
    for record in ctx.records:
        # Iteración por cada campo computado
        for field_name in computed_fields:
            # Si el campo está en los datos...
            if field_name in record:
                # Se captura el registro con el campo computado
                ctx.catch(record, field_name)

def _validation__confirm_valid_selection_values(ctx: 'ValidationContext') -> None:

    # Busqueda de los campos de tipo selection
    found_data = ctx.search_read(
        MODEL_NAME.BASE_MODEL_FIELD,
        [
            '&',
                ('ttype', '=', TTYPE_NAME.SELECTION),
                ('model_id.model', '=', ctx.model_name),
        ],
        [
            'name',
            ('selection_values', TTYPE_NAME.JSON, lambda ctx: ctx.agg('selection_ids', 'name', 'array')),
        ],
    )

    # Construcción de lista de campos de tipo selection
    selection_fields = {record['name']: record['selection_values'] for record in found_data}

    # Iteración por cada registro
    for record in ctx.records:
        # Iteración por cada campo
        for field_name in selection_fields:
            # Si el campo está en el registro...
            if field_name in record:
                # Si el valor no está dentro de los valores permitidos
                if record[field_name] is not None and record[field_name] not in selection_fields[field_name]:
                    # Se captura el registro con el campo inválido
                    ctx.catch(record, field_name)

def _validation__base_model__valid_model_name(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model]') -> None:

    # Patrón de estructura válido
    valid_pattern = r'^[a-z\d\.]*$'

    # Iteración por cada registro
    for record in ctx.records:
        # Obtención de nombre de modelo
        model_name = record['model']
        # Evaluación de estructura
        result = re.match(valid_pattern, model_name)
        # Si la estructura es inválida...
        if result is None:
            # Se captura el registro
            ctx.catch(record)

def _validation__base_model__coherent_label_and_name_in_new_model(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Obtención de nombre de modelo
        model_name = record['model']
        # Obtención  de nombre de tabla
        model_table_name = record['name']

        # Si nombres de modelo en guiones bajos y tabla no son iguales...
        if model_name.replace('.', '_') != model_table_name:
            # Se captura el registro
            ctx.catch(record)

def _validation__base_model_field__forbid_duplicated_names_in_same_model_on_input(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Búsqueda de registros duplicados
    duplicated_records = ctx.find_duplicated_composite_keys(ctx.records, ['model_id', 'name'])

    # Si se encontraron registros duplicados
    if duplicated_records:
        # Iteración por cada registro duplicado
        for record in duplicated_records:
            # Se captura el registro
            ctx.catch(record)

def _validation__base_model_field__forbid_duplicated_names_in_same_model(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Obtención de los campos existentes en el modelo
    existing_fields = [
        record['name']
        for record
        in ctx.search_read(
            'base.model.field',
            [('model', '=', ctx.model_name)],
            fields= ['name'],
        )
    ]

    # Iteración por cada registro
    for record in ctx.records:
        # Obtención del nombre del campo
        name = record['name']
        # Si el nombre del campo ya fue registrado en los campos existentes...
        if name in existing_fields:
            # Se captura el registro
            ctx.catch(record, name)

def _validation__base_model_field__forbid_duplicated_labels_in_same_model_on_input(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Búsqueda de registros duplicados
    duplicated_records = ctx.find_duplicated_composite_keys(ctx.records, ['model_id', 'label'])

    # Si se encontraron registros duplicados
    if duplicated_records:
        # Iteración por cada registro duplicado
        for record in duplicated_records:
            # Se captura el registro
            ctx.catch(record)

def _validation__base_model_field__forbid_duplicated_labels_in_same_model(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Obtención de los campos existentes en el modelo
    existing_fields = [
        record['label']
        for record in ctx.search_read(
            'base.model.field',
            [('model', '=', ctx.model_name)],
            fields= ['label']
        )
    ]

    # Iteración por cada registro
    for record in ctx.records:
        # Obtención de la leyenda del campo
        label = record['label']
        # Si la leyenda del campo ya fue registrada en los campos existentes...
        if label in existing_fields:
            # Se captura el registro
            ctx.catch(record, label)

def _validation__base_model_field__reject_related_model_on_non_related_ttype(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo no es de relación...
        if record['ttype'] not in ['many2one', 'one2many', 'many2many']:
            # Si existe un valor en modelo relacionado...
            if 'related_model_id' in record:
                # Si el valor es diferente de None...
                if record['related_model_id'] is not None:
                    # Se captura el error
                    ctx.catch(record)

def _validation__base_model_field__reject_missing_related_model_on_related_ttype(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo es de relación...
        if record['ttype'] in ['many2one', 'one2many', 'many2many']:
            # Si no existe valor en modelo relacionado...
            if 'related_model_id' not in record:
                # Se captura el error
                ctx.catch(record)

def _validation__base_model_field__reject_missing_on_delete_on_many2one_ttype(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el valor [on_delete] es None...
        if record.get('on_delete') == None:
            # Se captura el error
            ctx.catch(record)

def _validation__base_users__restrict_manual_password(ctx: 'ValidationContext[_M, _InternalModelSchema.base_users]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo de contraseña se encuentra en los datos
        if 'password' in record:
            # Se captura el error
            ctx.catch(record)

def _validation__base_model_field__reject_related_field_on_one2many_ttype(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo es de relación...
        if record['ttype'] != 'one2many':
            # Si existe campo de campo relacionado en los datos...
            if 'related_field' in record:
                # Si el valor del campo es diferente de None...
                if record['related_field'] is not None:
                    # Se captura el error
                    ctx.catch(record)

def _validation__base_model_field__reject_missing_related_field_on_one2many_ttype(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo es de relación...
        if record['ttype'] == 'one2many':
            # Si no existe el campo de campo relacionado en los datos...
            if 'related_field' not in record:
                # Se captura el error
                ctx.catch(record)

def _validation__base_model_field__validate_related_field(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo es de tipo [one2many]...
        if record['ttype'] == 'one2many':
            # Obtención del modelo relacionado
            related_model_id = record['related_model_id']
            # Obtención del campo relacionado
            related_field_name = record['related_field']

            # Comprobación de la existencia del campo
            count = ctx.search(
                'base.model.field',
                [
                    '&',
                        '&',
                            ('model_id.id', '=', related_model_id),
                            ('name', '=', related_field_name),
                        ('ttype', '=', 'many2one'),
                ],
            )

            # Si no se encontraron resultados...
            if count < 1:
                # Se captura el error
                ctx.catch(record, related_field_name)

def _validation__base_model_field__validate_related_field_on_input(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Búsqueda de combinaciones repetidas en ID de campo y valor de selección
    duplicated_records = ctx.find_duplicated_composite_keys(ctx.records, ['field_id', 'name'])

    # Si se encontraron registros duplicados
    if duplicated_records:
        # Iteración por cada registro duplicado
        for record in duplicated_records:
            # Se captura el error
            ctx.ctx(record)

def _validation__base_model_field__unique_related_field(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo es de tipo [one2many]...
        if record['ttype'] == 'one2many':
            # Obtención del modelo relacionado
            related_model_id = record['related_model_id']
            # Obtención del campo relacionado
            related_field_name = record['related_field']

            # Conteo de resultados
            count = ctx.search_count(
                'base.model.field',
                [
                    '&',
                        ('ttype', '=', 'one2many'),
                        '&',
                            ('related_field', '=', related_field_name),
                            '&',
                                ('model', '=', ctx.model_name),
                                ('related_model_id.id', '=', related_model_id),
                ]
            )

            # Si existen resultados...
            if count:
                # Se captura el error
                ctx.catch(record, related_field_name)

def _validation__base_model_field__unique_related_field_on_input(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    duplicated_records = ctx.find_duplicated_composite_keys(
        [record for record in ctx.records if record['ttype'] == 'one2many'],
        ['related_model_id', 'related_field']
    )
    # Si se encuentran combinaciones repetidas en los datos entrantes...
    if duplicated_records:
        # Iteración por cada registro duplicado
        for record in duplicated_records:
            # Se captura el error
            ctx.catch(record)

def _validation__base_model_field_selection__unique_selection_value_per_model_field(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field_selection]') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Obtención de la ID del campo
        field_id = record['field_id']
        # Obtención de los valores de selección existentes para el campo
        existing_selection_records = [
            record['name']
            for record
            in ctx.search_read(
                'base.model.field.selection',
                [('field_id', '=', field_id)],
                ['name'],
            )
        ]
        # Si el valor de selección a agregar ya existe en los valores del campo...
        if record['name'] in existing_selection_records:
            # Se captura el error
            ctx.catch(record, record['name'])


PRESET_VALIDATIONS: list[ValidationProperties[_M]] = [

        ValidationProperties(
            [CRUD_METHOD_NAME.CREATE, CRUD_METHOD_NAME.UPDATE],
            _validation__reject_id_values,
            'Los valores de ID no se pueden asignar ni modificar manualmente.',
        ),

        ValidationProperties(
            [CRUD_METHOD_NAME.CREATE, CRUD_METHOD_NAME.UPDATE],
            _validation__reject_create_and_update_date_values,
            'Los valores de fecha de creación y fecha de modificación no se pueden asignar ni modificar manualmente.',
        ),

        ValidationProperties(
            [CRUD_METHOD_NAME.CREATE, CRUD_METHOD_NAME.UPDATE],
            _validation__reject_create_and_update_user_values,
            'Los valores de fecha de creación y fecha de modificación no se pueden asignar ni modificar manualmente.',
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__confirm_required_fields,
            'El campo [{value}] es requerido',
        ),

        ValidationProperties(
            [CRUD_METHOD_NAME.CREATE, CRUD_METHOD_NAME.UPDATE],
            _validation__confirm_valid_selection_values,
            'El valor de selección en el campo [{value}] es inválido.',
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.UPDATE,
            _validation__prevent_update_on_readonly_fields,
            'El campo [{value}] es de solo lectura y no puede ser modificado.',
        ),

        ValidationProperties(
            [CRUD_METHOD_NAME.CREATE, CRUD_METHOD_NAME.UPDATE],
            _validation__prevent_create_or_update_on_computed_fields,
            'El campo [{value}] es computado y no se le puede asignar un valor explícito diferente al calculado.',
        ),

        ValidationProperties(
            [CRUD_METHOD_NAME.CREATE, CRUD_METHOD_NAME.UPDATE],
            _validation__base_users__restrict_manual_password,
            'La contraseña no se puede establecer manualmente.',
            MODEL_NAME.BASE_USERS,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model__valid_model_name,
            'El nombre de modelo solo puede contener minúsculas, dígitos y puntos.',
            MODEL_NAME.BASE_MODEL,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model__coherent_label_and_name_in_new_model,
            'El nombre de tabla de modelo debe ser igual que el nombre de modelo sustituyendo puntos por guiones bajos.',
            MODEL_NAME.BASE_MODEL,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__forbid_duplicated_names_in_same_model_on_input,
            'No puede haber nombres de campo repetidos en el mismo modelo.',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__forbid_duplicated_names_in_same_model,
            'El campo [{value}] ya existe en el modelo.',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__forbid_duplicated_names_in_same_model_on_input,
            'No puede haber más de un campo con el mismo nombre en el mismo modelo.',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__forbid_duplicated_labels_in_same_model,
            'La leyenda de campo "{value}" ya existe en el modelo.',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__forbid_duplicated_labels_in_same_model_on_input,
            'No puede haber más de un campo con la misma leyenda en el mismo modelo.',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__reject_related_model_on_non_related_ttype,
            'Los campos que no son de tipo [many2one], [one2many] o [many2many] no pueden tener un [related_model_id].',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__reject_missing_related_model_on_related_ttype,
            'Los campos de tipo [many2one], [one2many] o [many2many] deben tener un [related_model_id].',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__reject_missing_on_delete_on_many2one_ttype,
            'Los campos de tipo [many2one] deben tener un parámetro en [on_delete].',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__reject_related_field_on_one2many_ttype,
            'Los campos que no son de tipo [one2many] no pueden tener un [related_field].',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__reject_missing_related_field_on_one2many_ttype,
            'Los campos de tipo [one2many] deben tener un [related_field].',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__validate_related_field,
            'El campo relacionado [{value}] del registro no es válido.',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__unique_related_field,
            'El campo [{value}] de tipo [many2one] ya está vinculado a otro campo de tipo one2many de este modelo.',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__unique_related_field_on_input,
            'No puede haber más de un campo [one2many] que se relaciona a un mismo campo [many2one] de un mismo modelo.',
            MODEL_NAME.BASE_MODEL_FIELD,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field_selection__unique_selection_value_per_model_field,
            'El valor de selección [{value}] ya existe para el campo.',
            MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        ),

        ValidationProperties(
            CRUD_METHOD_NAME.CREATE,
            _validation__base_model_field__validate_related_field_on_input,
            'Los valores de selección deben ser únicos por cada campo relacionado.',
            MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
        ),

    ]
