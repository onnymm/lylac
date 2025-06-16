import re
from typing import Any
from ...._constants import MODEL_NAME
from ...._module_types import ModelRecord
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

    def validate_required_fields(
        self,
        params: Validation.Create.Individual.Args[ModelRecord.BaseModelField],
    ) -> Any:
        """
        ### Validación de campos requeridos
        Esta validación revisa en la base de datos cuáles son los campos requeridos en
        el modelo de la transacción, revisa los datos entrantes y valida que el
        diccionario entrante contenga las llaves de los campos requeridos. Arroja un
        error si encuentra una llave faltante.
        """

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

    def coherent_label_and_name_in_new_model(
        self,
        params: Validation.Create.Individual.Args[ModelRecord.BaseModel],
    ) -> Any:
        """
        ### Coherencia en nombre y etiqueta de modelo
        Esta validación compara la etiqueta del nuevo modelo y se asegura que el nombre
        modelo cumpla con la estructura de reemplazo de guiones bajos por puntos.

        Ejemplo:

        `base_permissions` - `base.permissions`

        Arroja un error si el formato no coincide.
        """

        # Obtención del nombre del modelo a crear
        record_name = params.data['name']
        # Obtención del nombre de modelo del modelo a crear
        record_model = params.data['model']

        # Comparación
        if record_name.replace('_', '.') != record_model:
            return record_model

    def valid_model_label(
        self,
        params: Validation.Create.Individual.Args[ModelRecord.BaseModel],
    ) -> Any:
        """
        ### Etiqueta de modulo válida
        Esta validación se asegura que la etiqueta del nuevo modelo solo contenga
        letras minúsculas y guiones bajos en ésta.
        """

        # Obtención del nombre del modelo
        model_name = params.data['name']

        # Se valida que el nombre con los caracteres válidos
        coincidence = re.match(r'^[a-z_]*$', model_name)

        # Si no existe coincidencia se retorna el nombre
        if coincidence is None:
            return model_name

    def unmutable_field_properties(
        self,
        params: Validation.Update.Individual.Args[ModelRecord.BaseModelField],
    ) -> Any:
        """
        ### Propiedades de campo inmutables
        Esta validación se asegura de que solo la etiqueta de campo sea editable ya que
        no es posible realizar modificaciones de propiedades a columnas de tablas en la
        base de datos.
        """

        # Campos válidos
        valid_fields = ['name']

        # Revisión
        for field in params.data.keys():
            # Si se encuentra un campo que no es válido...
            if field not in valid_fields:
                # Se retorna True para disparar el error
                return True
