from sqlalchemy import create_engine
from ..settings import CREDENTIALS
from .._typing.callables import TransactionCallback
from .._typing.type_parameters import _T

class EngineService:

    def __init__(
        self,
    ) -> None:

        # Construcción de la URL
        url = self._build_url()
        # Inicialización del motor de conexión
        self._engine = create_engine(url)

    def execute_complex(
        self,
        callback: TransactionCallback[_T],
    ) -> _T:

        # Conexión con la base de datos
        with self._engine.begin() as conn:

            # Ejecución de la función provista y captura de la respuesta obtenida
            response = callback(conn)

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
