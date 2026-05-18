import re
from typing import Any
from typing import TypeGuard
from sqlalchemy import select
from sqlalchemy.engine import Connection
from .._core import Metadata
from .._core import Transaction

class ModelDataIndex:
    _start = '__#@#'
    _end = '#@#__'
    _pattern = f'{_start}.*{_end}'

    def __init__(
        self,
        conn: Connection,
    ) -> None:

        # Obtención de la instancia de conexión
        self._conn = conn
        # Obtención de la instancia de manejo de transacciones
        self._transaction = Transaction()

    def encode(
        self,
        ref: str,
    ) -> str:

        # Construcción de la referencia codificada
        encoded_ref = f'{self._start}{ref}{self._end}'

        return encoded_ref

    def process(
        self,
        data: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        for record in data:
            for ( key, value ) in record.items():

                if self._is_encoded_ref(value):
                    record[key] = self._get_encoded_id(value)

        return data

    def _decode(
        self,
        encoded_ref: str,
    ) -> str:

        # Decoficación de la referencia
        decoded_ref = (
            encoded_ref
            .replace(self._start, '')
            .replace(self._end, '')
        )

        return decoded_ref

    def _get_encoded_id(
        self,
        encoded_ref: str,
    ) -> int | None:

        # Decoficación de la referencia
        decoded_ref = self._decode(encoded_ref)
        # Búsqueda de la ID
        record_id = self.get_resource_id(decoded_ref)

        return record_id

    def _is_encoded_ref(
        self,
        value: Any,
    ) -> TypeGuard[str]:
        if isinstance(value, str):
            if re.match(self._pattern, value):
                return True
        return False

    def get_resource_id(
        self,
        decoded_ref: str,
    ) -> int:

        # Query de búsqueda y lectura
        stmt = (
            # Selección de ID de recurso
            select(Metadata.BaseModelData.res_id)
            # Donde el nombre sea igual a la refererncia decodificada
            .where(Metadata.BaseModelData.name == decoded_ref)
        )

        # Obtención del resultado de la búsqueda
        result = self._transaction.search_read(stmt, self._conn)

        # Si el resultado tiene contenido...
        if len(result):
            # Destructuración del resultado
            [ ( record_id, ) ] = result

            return record_id
