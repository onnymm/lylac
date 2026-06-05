import re
from typing import TYPE_CHECKING

from .._resources import ValidationProperties
from .._typing.definitions import _InternalModelSchema
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._contexts import ValidationContext

def _reject_static_fields(ctx: 'ValidationContext') -> None:

    # Iteración por cada registro
    for record in ctx.records:
        # Iteración por los campos estáticos
        for field_name in ['id', 'create_date', 'update_date', 'create_uid', 'update_uid']:
            # Si existe el campo en los datos...
            if field_name in record:
                # Se captura el registro con el campo estático
                ctx.catch(field_name, record)

def _confirm_required_fields(ctx: 'ValidationContext') -> None:

    # Búsqueda de los campos requeridos del modelo
    found_data = ctx.search_read(
        'base.model.field',
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

def _confirm_valid_selection_values(ctx: 'ValidationContext') -> None:

    # Busqueda de los campos de tipo selection
    found_data = ctx.search_read(
        'base.model.field',
        [
            '&',
                ('ttype', '=', 'selection'),
                ('model_id.model', '=', ctx.model_name),
        ],
        [
            'name',
            ('selection_values', 'json', lambda ctx: ctx.agg('selection_ids', 'name', 'array')),
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

def _valid_model_name(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model]') -> None:

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

def _coherent_label_and_name_in_new_model(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model]') -> None:

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

def _forbid_duplicated_fields_in_same_model(ctx: 'ValidationContext[_M, _InternalModelSchema.base_model_field]') -> None:

    # Búsqueda de registros duplicados
    duplicated_records = ctx.find_duplicated_composite_keys(ctx.records, ['model_id', 'name'])

    # Si se encontraron registros duplicados
    if duplicated_records:
        # Iteración por cada registro duplicado
        for record in duplicated_records:
            # Se captura el registro
            ctx.catch(record)

PRESET_VALIDATIONS: list[ValidationProperties[_M]] = [

        ValidationProperties(
            ['create', 'update'],
            _reject_static_fields,
            'El campo {value} no puede ser declarado ni modificado manualmente.',
        ),

        ValidationProperties(
            'create',
            _confirm_required_fields,
            'El campo {value} es requerido',
        ),

        ValidationProperties(
            ['create', 'update'],
            _confirm_valid_selection_values,
            'El valor de selección en el campo {value} es inválido.',
        ),

        ValidationProperties(
            'create',
            _valid_model_name,
            'El nombre de modelo solo puede contener minúsculas, dígitos y puntos.',
            'base.model',
        ),

        ValidationProperties(
            'create',
            _coherent_label_and_name_in_new_model,
            'El nombre de tabla de modelo debe ser igual que el nombre de modelo sustituyendo puntos por guiones bajos.',
            'base.model',
        ),

        ValidationProperties(
            'create',
            _forbid_duplicated_fields_in_same_model,
            'No puede haber nombres de campo repetidos en el mismo modelo.',
            'base.model.field',
        ),

    ]
