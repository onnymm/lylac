import re
from typing import Any
from ...._constants import MODEL_NAME
from .._module_types import Validation
from ._base import _BaseValidations

class _Validations():

    def __init__(
        self,
        instance: _BaseValidations,
    ) -> None:

        # Asignación de instancia propietaria
        self._validations = instance
        # Asignación de instancia principal
        self._main = instance._main

    def validate_required(
            self,
            params: Validation.Create.Individual.Args,
        ) -> Any:

            # Obtención de los campos requeridos
            required_fields: list[str] = (
                self._main.search_read(
                    MODEL_NAME.BASE_MODEL_FIELD,
                    [
                        '&',
                            ('model_id', '=', params.model_id),
                            ('is_required', '=', True)
                    ],
                    ['name'],
                    output_format= 'dataframe',
                )
                ['name']
                .to_list()
            )

            # Inicialización de lista de campos faltantes
            missing_fields: list[str] = []

            # Iteración por cada campo requerido
            for required_field in required_fields:
                # Si el campo requerido no está en los datos entrantes de creación...
                if required_field not in params.data.keys():
                    # Se añade el nombre del campo a los campos faltantes
                    missing_fields.append(required_field)

            # Si existen campos faltantes
            if missing_fields:
                # Se retorna la información
                return missing_fields

    def model_names(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Obtención del nombre del modelo a crear
        record_name: str = params.data['name']
        # Obtención del nombre de modelo del modelo a crear
        record_model: str = params.data['model']

        # Comparación
        if record_name.replace('_', '.') != record_model:
            return record_model

    def valid_model_name(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Obtención del nombre del modelo
        model_name = params.data['name']

        # Se valida que el nombre con los caracteres válidos
        coincidence = re.match(r'^\w*$', model_name)

        # Si no existe coincidencia se retorna el nombre
        if coincidence is None:
            return model_name
