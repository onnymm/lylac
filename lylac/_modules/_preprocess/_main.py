from typing import Callable, Literal, Any, overload, TypedDict
from ..._core.modules import Preprocess_Core
from ..._core.main import _Lylac_Core
from ..._module_types import (
    _T,
    RecordData,
    ModelName,
)

RecordIds = list[int]
PosCreationCallback = Callable[[RecordIds], None]
PosUpdateCallback = Callable[[], None]
FieldName = str
RecordMany2ManyData = dict[FieldName, RecordIds]

class Preprocess(Preprocess_Core):

    def __init__(
        self,
        instance: _Lylac_Core
    ):

        # Asignación de la instancia principal
        self._main = instance
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc

    def convert_to_list(
        self,
        data: _T | list[_T],
    ) -> list[_T]:

        # Si el elemento entrante no es una lista de datos...
        if not isinstance(data, list):
            # Se convierte en lista
            return [data,]
        # Si el elemento ya es una lista de datos...
        else:
            # Se retorna éste sin cambios
            return data

    def process_data_on_create(
        self,
        user_id: int,
        model_name: ModelName,
        data: RecordData | list[RecordData],
    ) -> tuple[list[RecordData], PosCreationCallback]:
        """
        ### Preprocesamiento de datos en creación
        Este método procesa los datos entrantes, acondiciona los tipos de datos y crea
        funciones que se ejecutan tras la creación de registros.
        """

        # Conversión de datos entrantes si es necesaria
        data = self.convert_to_list(data)
        # Escritura de usuario de creación y modificación en los datos entrantes
        self._sign_create_and_update_user_id(user_id, model_name, data)
        # Creación de función para ejecutar tras la creación de registros
        ( data, pos_creation_callback ) = self._build_pos_creation_callback(model_name, data)

        return ( data, pos_creation_callback )

    def process_data_on_update(
        self,
        user_id: int,
        model_name: ModelName,
        record_ids: RecordIds,
        data: RecordData,
    ) -> PosUpdateCallback:
        """
        ### Preprocesamiento de datos en actualización
        Este método procesa los datos entrantes, acondiciona los tipos de datos y crea
        funciones que se ejecutan tras la creación de registros.
        """

        # Escritura de usuario de modificación
        self._sign_update_user_id(user_id, model_name, data)
        # Creación de función para ejecutar tras la actualización de registros
        after_update_callback = self._build_pos_update_callback(model_name, record_ids, data)

        return after_update_callback

    def _sign_create_and_update_user_id(
        self,
        user_id: int,
        model_name: ModelName,
        data: list[RecordData],
    ) -> None:

        # Obtención de los nombres de campos del modelo
        model_field_names = self._strc.get_model_field_names(model_name)

        # Si ya existen los campos de creación y modificación se actualizan éstos
        if 'create_uid' in model_field_names and 'write_uid' in model_field_names:
            for record in data:
                # Escritura de usuario de creación y modificación
                record['create_uid'] = user_id
                record['write_uid'] = user_id

    def _sign_update_user_id(
        self,
        user_id: int,
        model_name: ModelName,
        data: RecordData,
    ) -> None:

        # Obtención de los nombres de campos del modelo
        model_field_names = self._strc.get_model_field_names(model_name)

        # Si ya existen los campos de creación y modificación se actualizan éstos
        if 'write_uid' in model_field_names:
            # Escritura de usuario de modificación
            data['write_uid'] = user_id

    def _build_pos_creation_callback(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> tuple[list[RecordData], PosCreationCallback]:
        """
        ### Creación de función postransacción
        Este método construye una función que realiza más cambios y se ejecuta tras la
        creación de los registros, usando las IDs creadas como parámetro de entrada.
        """

        # Creación de función de actualizción de valores many2many
        execute_many2many_updates_after_create = self._main._subtransaction.build_many2many_updates_after_create(model_name, data)

        def pos_create_callback(
            record_ids: RecordIds,
        ) -> None:
            # Ejecución de actualizaciones de valores many2many
            execute_many2many_updates_after_create(record_ids)

        return ( data, pos_create_callback )

    def _build_pos_update_callback(
        self,
        model_name: ModelName,
        record_ids: RecordIds,
        data: RecordData,
    ) -> PosUpdateCallback:
        """
        ### Creación de función postransacción
        Este método construye una función que realiza más cambios y se ejecuta tras la
        modificación de los registros.
        """

        # Creación de función de actualizción de valores many2many
        execute_automatic_many2many_updates = self._main._subtransaction.build_many2many_updates_after_update(model_name, record_ids, data)

        # Creación de función principal de ejecución después de actualización principal
        def pos_update_callback():
            execute_automatic_many2many_updates()

        return pos_update_callback
