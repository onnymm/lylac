from typing import Literal
from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.sql.selectable import Select, TypedReturnsRows
from sqlalchemy.engine.base import Engine
from ..._module_types import DBCredentials
from ..._core import (
    _Lylac,
    Env,
)
from ..._module_types import _T

class Connection():

    def __init__(
        self,
        instance: _Lylac,
        credentials: DBCredentials | str | Literal['env'],
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Creación del motor de conexión a base de datos
        self._create_connection(credentials)

    def execute(
        self,
        statement: Select[_T] | TypedReturnsRows[_T],
        commit: bool = False
    ) -> CursorResult[_T]:

        # Conexión con la base de datos
        with self._main._engine.connect() as conn:
            # Ejecución en la base de datos
            response = conn.execute(statement)
            # Commit de los cambios
            if commit:
                conn.commit()

        # Retorno de respuesta tipada
        return response

    def _create_connection(
        self,
        credentials: Literal['env'] | DBCredentials | str,
    ) -> None:

        # Obtención de las variables de entorno en caso de requerirse
        if credentials == 'env':
            credentials = Env()._credentials

        # Inicialización del motor de conexión
        self._main._engine = self._create_engine(credentials)

    def _create_engine(
        self,
        params: DBCredentials | str,
    ) -> Engine:

        # Si una URL fue provista
        if isinstance(params, str):
            url = params

        # Obtención de los parámetros a utilizar
        else:
            host = params['host']
            port = params['port']
            name = params['db_name']
            user = params['user']
            password = quote(params['password'])

            url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

        # Creación del motor de conexión con la base de datos
        engine = create_engine(url)

        # Retorno del motor de conexión
        return engine
