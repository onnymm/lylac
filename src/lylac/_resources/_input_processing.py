from typing import Generic
from .._constants import FIELD_NAME
from .._typing.generics import _Record
from .._typing.generics import ItemOrList
from .._typing.type_parameters import _A
from .._typing.type_parameters import _M
from .._typing.type_parameters import _T
from .._typing.callables import ProcessingCallback

class InputProcessing(Generic[_M]):
    _FIRST_FIELDS = [
        FIELD_NAME.ID,
        FIELD_NAME.NAME,
    ]
    _LAST_FIELDS = [
        FIELD_NAME.DISPLAY_NAME,
        FIELD_NAME.CREATE_DATE,
        FIELD_NAME.UPDATE_DATE,
        FIELD_NAME.CREATE_UID,
        FIELD_NAME.UPDATE_UID,
    ]
    _on_creation_processing_callbacks: list[ProcessingCallback[_A]]
    _on_update_processing_callbacks: list[ProcessingCallback[_A]]

    def __init__(
        self,
    ) -> None:

        # Inicialización de lista de funciones de procesamiento personalizadas
        self._on_creation_processing_callbacks = []
        self._on_update_processing_callbacks = []

    def register_on_creation_processing(
        self,
        processing_callbacks: list[ProcessingCallback[_A]],
    ) -> None:

        # Asignación de lista de funciones
        self._on_creation_processing_callbacks = processing_callbacks

    def register_on_update_processing(
        self,
        processing_callbacks: list[ProcessingCallback[_A]],
    ) -> None:

        # Asignación de lista de funciones
        self._on_update_processing_callbacks = processing_callbacks

    def process_on_creation(
        self,
        data: ItemOrList[_Record[_A]],
    ) -> list[_Record[_A]]:

        # Se asegura una lista de datos
        data = self.to_list(data)
        # Preprocesamiento a través de las funciones personalizadas
        data = self.on_creation_custom_preprocessing(data)

        return data

    def process_on_update(
        self,
        record: _Record[_A],
    ) -> _Record[_A]:

        # Preprocesamiento a través de las funciones personalizadas
        record = self.on_update_custom_preprocessing(record)

        return record

    def to_list(
        self,
        content: ItemOrList[_T],
    ) -> list[_T]:

        # Si el contenido ya es una lista...
        if isinstance(content, list):
            # Se retorna igual
            return content
        # Se retorna el contenido dentro de una lista
        return [content]

    def on_creation_custom_preprocessing(
        self,
        data: list[_Record[_A]],
    ) -> list[_Record[_A]]:

        # Iteración por las funciones de procesamiento de entrada
        for processing_callback in self._on_creation_processing_callbacks:
            # Iteración por cada registro junto con índice para reasignación
            for ( i, record ) in enumerate(data):
                # Preprocesamiento del registro y captura del resultado por si ha sido copiado internamente
                processed_record = processing_callback(record)
                # Reasignación del registro
                data[i] = processed_record

        return data

    def on_update_custom_preprocessing(
        self,
        record: _Record[_A],
    ) -> _Record[_A]:

        # Obtención de la lista de funciones de preprocesamientoa a usar
        for processing_callback in self._on_update_processing_callbacks:
            # Preprocesamiento del registro y captura del resultado por si ha sido copiado internamente
            record = processing_callback(record)

        return record

    def reorder_fields(
        self,
        fields: list[_T],
    ) -> list[_T]:

        # Obtención de todos los campos iniciales que fueron encontrados en la lista provista
        default_first = [f for f in self._FIRST_FIELDS if f in fields]
        # Obtención de todos los campos finales que fueron encontrados en la lista provista
        default_last = [f for f in self._LAST_FIELDS if f in fields]

        # Obtención de todos los campos que no son iniciales ni finales
        filtered_fields = [f for f in fields if not (f in default_first or f in default_last)]
        # Ordenamiento alfabético de los campos
        filtered_fields.sort()

        # Construcción de lista de campos normalizada
        processed_fields = default_first + filtered_fields + default_last

        return processed_fields

    def id_first_on_fields(
        self,
        fields: list[_T],
    ) -> list[_T]:

        # Se filtran todos los campos que no sean el de ID
        clean_fields = [f for f in fields if f != FIELD_NAME.ID]
        # Concatenación de campos
        fields = [FIELD_NAME.ID] + clean_fields

        return fields
