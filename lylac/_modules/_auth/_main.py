from typing import Literal
from passlib.context import CryptContext
from ..._core import _Lylac, BaseAuth
from ._submodules import (
    Token,
    UserSession,
)

class Auth(BaseAuth):

    def __init__(
        self,
        instance: _Lylac
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Inicialización de submódulos
        self._m_session = UserSession(self)
        self._m_token = Token(self)

        # Contexto para hasheo
        self._pwd_context = CryptContext(schemes= ['bcrypt'], deprecated= 'auto')

    def identify_user(
        self,
        token: str,
    ) -> int:

        # Obtención de la UUID de la sesión
        session_uuid = self._m_token.get_session_uuid_from_token(token)
        # Obtención de la ID del usuario desde la UUID de la sesión
        user_id = self._m_session.get_session_uuid_user_id(session_uuid)

        return user_id

    def hash_password(
        self,
        password: str,
    ) -> str:

        # Se genera el hasheo de la contraseña
        hashed_password = self._pwd_context.hash(password)

        return hashed_password

    def login(
        self,
        login: str,
        password: str,
    ) -> str | Literal[False]:

        # Obtención de la ID del usuario si las credenciales son correctas
        user_id = self._authenticate_user(login, password)
        # Si las credenciales son correctas...
        if user_id:

            # Generación de la UUID de sesión y su fecha de expiración
            ( session_uuid, expiration_date ) = self._m_session.generate_user_session(user_id)
            # Se crea un token de sesión
            token = self._m_token.create_session_token(session_uuid, expiration_date)

            return token

        # Si las credenciales no son correctas...
        else:
            return False

    def _authenticate_user(
        self,
        login: str,
        password: str,
    ) -> int | Literal[False]:

        # Obtención de los datos del usuario
        found_data = self._main._compiler.get_user_data_by_username(login)

        # Si no se encontraron datos...
        if found_data is None:
            # Se retorna falso
            return False

        # Destructuración de los datos
        ( user_id, hashed_password_from_db ) = found_data

        # Verificación de la contraseña
        verified = self._pwd_context.verify(password, hashed_password_from_db)

        # Si la contraseña es correcta...
        if verified:
            # Se retorna la ID del usuario
            return user_id
        # Si la contraseña es incorrecta...
        else:
            # Se retorna falso
            return False
