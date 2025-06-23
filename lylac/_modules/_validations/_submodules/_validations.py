import re
from typing import Any
from ...._constants import MODEL_NAME
from ...._core import BaseValidations
from ...._module_types import ModelRecord
from .._module_types import Validation

class _Validations():

    def __init__(
        self,
        instance: BaseValidations,
    ) -> None:

        # Asignación de instancia propietaria
        self._validations = instance
        # Asignación de instancia principal
        self._main = instance._main

    def reject_id_values(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de ID en creación
        if 'id' in params.data.keys():
            return True

    def reject_create_date_values(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de Fecha de creación en creación
        if 'create_date' in params.data.keys():
            return True

    def reject_write_date_values(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de Fecha de modificación en creación
        if 'write_date' in params.data.keys():
            return True

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
        params: Validation.Create.Individual.Args[ModelRecord.BaseModel_],
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
        params: Validation.Create.Individual.Args[ModelRecord.BaseModel_],
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
        valid_fields = ['label']

        # Revisión
        for field in params.data.keys():
            # Si se encuentra un campo que no es válido...
            if field not in valid_fields:
                # Se retorna True para disparar el error
                return True

    def forbid_duplicated_fields_in_same_model(
        self,
        params: Validation.Create.Individual.Args[ModelRecord.BaseModelField],
    ) -> Any:
        """
        ### Prohibir campos duplicados en modelo
        Esta validación se asegura que cada diccionario de datos entrante para la
        creación de un nuevo registro en el campo de modelos no incluya un nombre de
        campo combinado con una ID de modelo vinculada que ya exista en la base de
        datos. Arroja un error si encuentra coincidencias.
        """

        # Obtención de los valores a usar en filtro
        field_name = params.data['name']
        model_id = params.data['model_id']

        # Búsqueda de coincidencias
        records = self._main.search_read(
            'base.model.field',
            [
                '&',
                    ('name', '=', field_name),
                    ('model_id', '=', model_id)
            ],
            ['name', 'model_id'],
            output_format= 'dataframe',
            only_ids_in_relations= True,
        )

        # Si existen coincidencias se retorna el nombre del campo
        if len(records):
            return field_name

    def forbid_duplicated_fields_in_same_model_in_incoming_data(
        self,
        params: Validation.Create.Group.Args[ModelRecord.BaseModelField],
    ) -> Any:
        """
        Prohibir campos duplicados en modelo desde datos entrantes
        Esta validación se asegura que cada diccionario de datos entrante para la
        creación de un nuevo registro en el campo de modelos no incluya un nombre de
        campo combinado con una ID de modelo vinculada dos veces en los datos entrantes.
        """

        # Obtención de cantidad de registros a crear
        incoming_records_qty = len(params.data)

        # Si solo existe un registro la función se termina ya que no hay suficientes datos a comparar
        if incoming_records_qty == 1:
            return None

        # Obtención de lista de duplicados
        duplicated_pairs = self._main._algorythms.find_duplicates(
            params.data,
            lambda value: ( value['name'], value['model_id'] ),
        )

        # Si existen pares duplicados se retornan éstos
        if len(duplicated_pairs):
            return duplicated_pairs

    def unique_field_label_in_model(
        self,
        params: Validation.Create.Individual.Args[ModelRecord.BaseModelField],
    ) -> Any:
        """
        ### Etiqueta de campo única por modelo
        Esta validación se asegura que los datos entrantes no contengan una etiqueta de
        campo ya existente en el modelo en donde se intenta crear el registro. Arroja
        un error en caso de hallar un registro de campo con la misma etiqueta de los
        datos entrantes.
        """

        # Obtención de los valores a usar en el filtro
        field_label = params.data['label']
        model_id = params.data['model_id']

        # Búsqueda de coincidencias
        results = self._main.search_read(
            'base.model.field',
            [
                '&',
                    ('label', '=', field_label),
                    ('model_id', '=', model_id)
            ]
        )

        # Si existen coincidencias se retona el nombre del campo y la ID de modelo
        if len(results):
            return field_label

    def unique_field_label_in_model_in_incomig_data(
        self,
        params: Validation.Create.Group.Args[ModelRecord.BaseModelField],
    ) -> Any:
        """
        ### Etiqueta de campo única por modelo en datos entrantes
        Esta validación se asegura que los datos entrantes no contengan una etiqueta de
        campo repetida en los datos entrantes. Arroja un error en caso de hallar
        valores en etiqueta de campo repetidos en los datos entrantes.
        """

        # Búsqueda de duplicados
        duplicated = self._main._algorythms.find_duplicates(
            params.data,
            lambda record: ( record['label'], record['model_id'] ),
        )

        # Si existen nombres duplicados se retornan éstos
        if len(duplicated):
            return duplicated

    def avoid_password_creation(
        self,
        params: Validation.Create.Individual.Args[ModelRecord.BaseUser],
    ) -> Any:
        """
        ### Restricción de contraseña inicial
        Esta validación se asegura que no se ingrese una contraseña sin ser hasheada.
        """

        # Comprobación de existencia de Contraseña en datos entrantes
        if 'password' in params.data.keys():
            return params.data['name']

    def avoid_password_modification(
        self,
        params: Validation.Update.Individual.Args[ModelRecord.BaseUser],
    ) -> Any:

        # Comprobación de existencia de Contraseña en datos entrantes
        if 'password' in params.data.keys():
            return params.data['name']
