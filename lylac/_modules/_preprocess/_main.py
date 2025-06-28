from typing import Callable
from ..._core import _Lylac
from ..._module_types import RecordData
from sqlalchemy import delete
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm import Session

RecordIds = list[int]
PosCreationCallback = Callable[[RecordIds], None]
PosUpdateCallback = Callable[[], None]
FieldName = str
RecordMany2ManyData = dict[FieldName, RecordIds]

class Preprocess():

    def __init__(
        self,
        instance: _Lylac
    ):

        # Asignación de la instancia principal
        self._main = instance
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc

    def process_data_on_create(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> PosCreationCallback:

        # Escritura de usuario de creación y modificación en los datos entrantes
        self._sign_create_and_update_user_id(model_name, data)
        # Creación de función para ejecutar tras la creación de registros
        pos_creation_callback = self._build_pos_creation_callback(model_name, data)

        return pos_creation_callback

    def process_data_on_update(
        self,
        model_name: str,
        record_ids: RecordIds,
        data: RecordData,
    ):

        # Escritura de usuario de modificación
        self._sign_update_user_id(model_name, data)
        # Creación de función para ejecutar tras la actualización de registros
        after_update_callback = self._build_pos_update_callback(model_name, record_ids, data)

        return after_update_callback

    def _sign_create_and_update_user_id(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> None:

        # Obtención de los nombres de campos del modelo
        model_field_names = self._strc.get_model_field_names(model_name)

        # Si ya existen los campos de creación y modificación se actualizan éstos
        if 'create_uid' in model_field_names and 'write_uid' in model_field_names:
            for record in data:
                # Escritura de usuario de creación y modificación
                record['create_uid'] = 1
                record['write_uid'] = 1

    def _sign_update_user_id(
        self,
        model_name: str,
        data: RecordData,
    ) -> None:

        # Obtención de los nombres de campos del modelo
        model_field_names = self._strc.get_model_field_names(model_name)

        # Si ya existen los campos de creación y modificación se actualizan éstos
        if 'write_uid' in model_field_names:
            # Escritura de usuario de modificación
            data['write_uid'] = 1

    def _build_pos_creation_callback(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> PosCreationCallback:

        # Creación de función de actualizción de valores many2many
        execute_automatic_many2many_updates = self._build_many2many_updates_after_creation(model_name, data)

        def pos_create_callback(
            record_ids: RecordIds,
        ) -> None:
            # Ejecución de actualizaciones de valores many2many
            execute_automatic_many2many_updates(record_ids)

        return pos_create_callback

    def _build_pos_update_callback(
        self,
        model_name: str,
        record_ids: RecordIds,
        data: RecordData,
    ):

        # Creación de función de actualizción de valores many2many
        execute_automatic_many2many_updates = self._build_many2many_updates_after_update(model_name, record_ids, data)

        # Creación de función principal de ejecución después de actualización principal
        def pos_update_callback():
            execute_automatic_many2many_updates()

        return pos_update_callback

    def _build_many2many_updates_after_creation(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> PosCreationCallback:

        # Inicialización de lista de valores
        pending_many2many_updates: list[RecordMany2ManyData] = []
        # Obtención de los nombres de campos many2many
        many2many_fields = self._strc.get_model_many2many_field_names(model_name)

        # Iteración por la lista de registros
        for record in data:
            # Inicialización de diccionario de actualizaciones
            record_many2many_data: RecordMany2ManyData = {}
            # Iteración por cada campo many2many
            for many2many_field in many2many_fields:
                # Si el campo existe en las llaves de los datos del registro
                if many2many_field in record.keys():
                    # Se guardan los datos en el diccionario de actualizaciones
                    record_many2many_data[many2many_field] = record[many2many_field].copy()
                    # Se eliminan los datos del diccionario
                    del record[many2many_field]
            # Se añade el diccionario de actualizaciones a la lista
            pending_many2many_updates.append(record_many2many_data)

        # Creación de la funcióna a ejecutarse tras la creación de los registros
        def execute_automatic_many2many_updates(
            record_ids: RecordIds,
        ):

            # Iteración por cada ID creada
            for ( i, record_id ) in enumerate(record_ids):
                # Iteración por cada campo en los datos
                for field in pending_many2many_updates[i].keys():
                    # Obtención del nombre del modelo de relación
                    relation_model = self._strc.get_relation_model_name(model_name, field)
                    # Obtención de la lista de IDs a vincular
                    related_ids = pending_many2many_updates[i][field]
                    # Inicialización de los datos  escribir
                    many2many_data = [ {'x': record_id, 'y': related_id} for related_id in related_ids ]
                    # Creación de los datos
                    self._main._compiler.create_many2many(
                        relation_model,
                        many2many_data
                    )

        return execute_automatic_many2many_updates

    def _build_many2many_updates_after_update(
        self,
        model_name: str,
        record_ids: RecordIds,
        data: RecordData,
    ) -> PosUpdateCallback:

        # Obtención de los nombres de campos many2many del modelo
        many2many_fields = self._strc.get_model_many2many_field_names(model_name)
        # Inicialización de lista de actualizaciones a realizar
        individual_many2many_creations: list[Callable[[], None]] = []

        # Iteración por cada uno de los campos many2many contenido en el modelo
        for many2many_field in many2many_fields:
            # Si el campo existe en los datos
            if many2many_field in data.keys():
                # Obtención de la lista de IDs a actualizar
                values: RecordIds = data[many2many_field].copy()
                # Se eliminan los datos originales del diccionario
                del data[many2many_field]

                # Creación de función de creación de valores many2many
                creation_callback = self._build_many2many_update_after_update(
                    model_name,
                    many2many_field,
                    record_ids,
                    values,
                )

            # Se añade la función de creción de valores many2many
            individual_many2many_creations.append(creation_callback)

        def execute_automatic_many2many_updates():
            for callback in individual_many2many_creations:
                callback()

        return execute_automatic_many2many_updates

    def _build_many2many_update_after_update(
        self,
        model_name: str,
        field_name: str,
        record_ids: RecordIds,
        values: RecordIds,
    ):

        # Obtención del nombre del modelo de relación
        relation_model = self._strc.get_relation_model_name(model_name, field_name)
        # Inicialización de los datos a escribir
        many2many_data = [ {'x': record_id, 'y': value} for record_id in record_ids for value in values ]

        # Creación de función de actualización de valores many2many para ejecución después de actualización principal
        def update_many2many_values():
            # Eliminació de los datos anteriores
            self._main._compiler.delete_many2many(model_name, field_name, record_ids)
            # Creación de los datos
            self._main._compiler.create_many2many(relation_model, many2many_data)

        return update_many2many_values
