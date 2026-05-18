from typing import Generic
from .._constants import FIELD_NAME
from .._typing.generics import ItemOrList
from .._typing.type_parameters import _M
from .._typing.type_parameters import _T

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
