from typing import Any
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.engine import Connection
from .._typing.type_parameters import _V

class Transaction:

    def create(
        self,
        stmt: Insert[Any],
        conn: Connection,
    ) -> list[int]:

        # Ejecución de la creación
        response = (
            conn
            .execute(stmt)
            .fetchall()
        )
        # Obtención de lista de IDs de registros creados
        record_ids: list[int] = [ record_id for ( record_id, ) in response ]

        return record_ids

    def search(
        self,
        stmt: Select[int],
        conn: Connection,
    ) -> list[int]:

        # Ejecución de la búsqueda
        [ found_data ] = (
            conn
            .execute(stmt)
            .fetchall()
        )
        # Conversión a lista de enteros
        record_ids: list[int] = list(found_data)

        return record_ids

    def search_read(
        self,
        stmt: Select[_V],
        conn: Connection,
    ) -> list[tuple[_V]]:

        # Ejecución de la búsqueda
        found_data: list[tuple[_V]] = (
            conn
            .execute(stmt)
            .fetchall()
        )

        return found_data

    def read(
        self,
        stmt: Select[_V],
        conn: Connection,
    ) -> list[tuple[_V]]:

        # Ejecución de la lectura
        data = list[tuple[_V]] = (
            conn
            .execute(stmt)
            .fetchall()
        )

        return data

    def update(
        self,
        stmt: Update,
        conn: Connection,
    ) -> None:

        # Ejecución de la actualización de datos
        conn.execute(stmt)
