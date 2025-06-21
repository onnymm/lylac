import os
from ...._module_types import CredentialsFromEnv
from ...._settings import ENV_VARIABLES

class _Env():

    def __init__(
        self,
    ) -> None:

        # Obtención de los nombres de variables de entorno
        host= ENV_VARIABLES.DATABASE.HOST
        port= ENV_VARIABLES.DATABASE.PORT
        db_name= ENV_VARIABLES.DATABASE.DB_NAME
        user= ENV_VARIABLES.DATABASE.USER
        password= ENV_VARIABLES.DATABASE.PASSWORD

        # Se inicializa el objeto de credenciales obteniendo los valores de variables de entorno
        self.credentials = CredentialsFromEnv(
            host= os.environ.get(host),
            port= os.environ.get(port),
            db_name= os.environ.get(db_name),
            user= os.environ.get(user),
            password= os.environ.get(password),
        )
