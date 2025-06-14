from typing import (
    Literal,
    TypedDict,
    Optional,
)
from ...._data import initial_data
from ...._module_types import Transaction
from .._module_types import ValidationMethod
from ._base import _BaseValidations

class ValidationData(TypedDict):
    module: Literal['_validations']
    callback: str
    transaction: Transaction
    method: ValidationMethod
    model: Optional[str]
    message: str

validations_data: list[ValidationData] = [
    {
        'module': '_validations',
        'callback': 'validate_required',
        'transaction': 'create',
        'method': 'record',
        'model': 'generic',
        'message': 'Los campos {value} son requeridos en el registro {data}.',
    },
    {
        'module': '_validations',
        'callback': 'valid_model_name',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model',
        'message': 'El valor "{value}" en el nombre de modelo solo puede contener letras y guiones bajos.'
    },
    {
        'module': '_validations',
        'callback': 'model_names',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model',
        'message': 'El nombre y nombre de modelo de "{value}" deben ser coincidir con el patrón "model_name" - "model.name" respectivamente.',
    },
]

class _Initialize():

    def __init__(
        self,
        instance: _BaseValidations,
    ) -> None:

        # Asignación de instancia propietaria
        self._validations = instance
        # Asignación de instancia principal
        self._main = instance._main
        # Generación de nombres de modelos iniciales
        self._initial_models = list(initial_data.keys()) + ['base.users']

    def initialize_data(
        self,
    ) -> None:

        # Genéricos
        self._validations.initialize_model_validations('generic')

        # Modelos iniciales
        for model_name in self._initial_models:
            self._validations.initialize_model_validations(model_name)

        for validation_data in validations_data:
            # Si no fue definido un modelo específico para la validación
            if validation_data['model'] is None:
                # Se define la validación para todos los modelos
                model = 'generic'
            else:
                # Se define la validación para el modelo especificado
                model = validation_data['model']

            # Obtención del nombre de la transacción para la que aplica la validación
            transaction = validation_data['transaction']

            # Obtención de la función de validación
            validation_callback = self._get_validation_callback(validation_data['module'], validation_data['callback'])

            # Se guarda la validación y sus parámetros en el núcleo de validaciones
            self._validations._hub[model][transaction].append(
                {
                    'callback': validation_callback,
                    'message': validation_data['message'],
                    'method': validation_data['method'],
                }
            )

    def _get_validation_callback(
        self,
        module_name: str,
        callback_name: str,
    ):

        # Obtención del módulo de la instancia principal
        module_extension = getattr(self._main, module_name)
        # Obtención del submódulo de validaciones del módulo de la instancia
        validations_submodule = getattr(module_extension, '_m_validations')
        # Obtención de la referencia de la función de validación
        validation_callback = getattr(validations_submodule, callback_name)

        return validation_callback