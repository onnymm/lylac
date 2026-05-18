from sqlalchemy import create_engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.selectable import Select
from ..settings import CREDENTIALS
from .._typing.callables import TransactionCallback
from .._typing.type_parameters import _T

class ConnectionService:

    def __init__(
        self,
    ) -> None:

        # Construcción de la URL
        url = self._build_url()
        # Inicialización del motor de conexión
        self._engine = create_engine(url)

    def execute_dql(
        self,
        statement: Select[_T],
    ) -> CursorResult[_T]:

        # Conexión con la base de datos
        with self._engine.connect() as conn:
            # Ejecución en la base de datos
            response = conn.execute(statement)

        # Retorno de respuesta tipada
        return response

    def execute_dml(
        self,
        statement: Insert[_T],
    ) -> CursorResult[int]:

        # Conexión con la base de datos
        with self._engine.connect() as conn:
            # Ejecución en la base de datos
            response = conn.execute(statement)

            conn.commit()

        # Retorno de respuesta tipada
        return response

    def execute_complex(
        self,
        callback: TransactionCallback[_T],
    ) -> _T:

        # Conexión con la base de datos
        with self._engine.begin() as conn:

            # Ejecución encapsulada para hacer rollback
            try:
                # Ejecución de la función provista y captura de la respuesta obtenida
                response = callback(conn)
            # Si ocurre algún error...
            except Exception as e:
                # Se realiza rollback
                conn.rollback()

                raise

            return response

    def _build_url(
        self,
    ) -> str:

        # Obtención de los parámetros
        db_name = CREDENTIALS.NAME
        host = CREDENTIALS.HOST
        user = CREDENTIALS.USER
        port = CREDENTIALS.PORT
        password = CREDENTIALS.PASSWORD

        # Construcción de la URL
        url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'

        return url
