from ..._module_types import ValidationData

validations_data: list[ValidationData] = [
    # Validación de campos requeridos en creación de un registro en cualquier tabla
    {
        'module': '_validations',
        'callback': 'validate_required_fields',
        'transaction': 'create',
        'method': 'record',
        'model': 'generic',
        'message': 'Los campos {value} son requeridos en el registro {data}.',
    },
    # Caracteres válidos en etiqueta de modelo en creación de un registro en la tabla de modelos
    {
        'module': '_validations',
        'callback': 'valid_model_label',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model',
        'message': 'El valor "{value}" en el nombre de modelo solo puede contener letras y guiones bajos.'
    },
    # Consistencia en etiqueta y modelo de nueva tabla en creación de un registro en la tabla de modelos
    {
        'module': '_validations',
        'callback': 'coherent_label_and_name_in_new_model',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model',
        'message': 'El nombre y nombre de modelo de "{value}" deben ser coincidir con el patrón "model_name" - "model.name" respectivamente.',
    },
    # Restricción para no modificar propiedades de un campo ya creado en modificación de un registro en la tabla de campos
    {
        'module': '_validations',
        'callback': 'unmutable_field_properties',
        'transaction': 'update',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Las propiedades de los campos que no sea la etiqueta no pueden ser modificadas en {data}. Si realmente deseas realizar modificaciones elimina el campo y vuelve a crearlo.'
    },
    # Restricción de creación de un campo en un modelo que ya tiene un campo con el mismo nombre en creación de un registro en la tabla de modelos
    {
        'module': '_validations',
        'callback': 'forbid_duplicated_fields_in_same_model',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Ya existe un campo llamado "{value}" y no es posible registrar los datos {data}.'
    },
    # Restricción de ingreso de pares nombre/ID de modelo en creación de registros en la tabla de campos
    {
        'module': '_validations',
        'callback': 'forbid_duplicated_fields_in_same_model_in_incoming_data',
        'transaction': 'create',
        'method': 'list',
        'model': 'base.model.field',
        'message': 'Los pares de nombre de campo y modelo {value} no pueden existir más de una vez.'
    },
    # Restricción de etiqueta de campo duplicada en el mismo modelo en creación de un registro de campo
    {
        'module': '_validations',
        'callback': 'unique_field_name_in_model',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Ya existe un campo con la etiqueta "{value}" en el modelo.'
    },
    # Restricción de etiquetas de campo repetidas en el mismo modelo en datos entrantes en creación de registros de campo.
    {
        'module': '_validations',
        'callback': 'unique_field_name_in_model_in_incomig_data',
        'transaction': 'create',
        'method': 'list',
        'model': 'base.model.field',
        'message': 'No se pueden registrar campos con la misma etiqueta en el mismo modelo. Valores de error: {value}.'
    },
]
