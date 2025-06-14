from ..._module_types import ValidationData

validations_data: list[ValidationData] = [
    # Validación de campos requeridos en creación de un registro en cualquier tabla
    {
        'module': '_validations',
        'callback': 'validate_required',
        'transaction': 'create',
        'method': 'record',
        'model': 'generic',
        'message': 'Los campos {value} son requeridos en el registro {data}.',
    },
    # Caracteres válidos en etiqueta de modelo en creación de un registro en la tabla de modelos
    {
        'module': '_validations',
        'callback': 'valid_model_name',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model',
        'message': 'El valor "{value}" en el nombre de modelo solo puede contener letras y guiones bajos.'
    },
    # Consistencia en etiqueta y modelo de nueva tabla en creación de un registro en la tabla de modelos
    {
        'module': '_validations',
        'callback': 'model_names',
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
]
