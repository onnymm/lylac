from datetime import datetime
from datetime import timedelta
from hashlib import sha256
from passlib.context import CryptContext
from typing import TYPE_CHECKING
from typing import Callable
from uuid import uuid4
from sqlalchemy.engine import Connection
from .._constants import DATA_RESOURCE
from .._constants import DEFAULTS
from .._constants import MODEL_NAME
from .._constants import ERROR_LABEL
from .._constants import TTYPE_NAME
from .._typing.generics import _Records
from .._typing.models import RecordShape
from .._typing.definitions import TType
from .._typing.type_parameters import _M
from ..errors import IncorrectPasswordError
from ..errors import ExpiredSessionError
from ..errors import InvalidSessionUUIDError
from ..errors import UserNotActiveError
from ..errors import UserNotFoundError
from ..settings import SETTINGS

if TYPE_CHECKING:
    from .._main import Lylac

class _base_users(RecordShape):
    login: TType.Char
    active: TType.Boolean
    password: TType.Char

class _found_session(RecordShape):
    is_active_session: TType.Boolean
    user_is_active: TType.Boolean
    uid: TType.Integer

_pwd_context = CryptContext(schemes= ['bcrypt_sha256'], deprecated= 'auto')

def hash_password(raw_pwd: str) -> str:
    """
    Obtención de hash de contraseña.
    """

    # Hasheo de contraseña
    hashed_pwd = _pwd_context.hash(raw_pwd)

    return hashed_pwd

def default_password() -> str:

    # Construcción de hash de contraseña genérica
    pwd = hash_password(SETTINGS.SECURITY.DEFAULT_PASSWORD)

    return pwd

def verify_password(
    input_password: str,
    hashed_password: str,
) -> bool:

    # Verificación de la contraseña
    is_correct = _pwd_context.verify(input_password, hashed_password)

    return is_correct

def build_login_callback(
    main: 'Lylac[_M]',
    username: str,
    password: str,
) -> Callable[[Connection], int]:

    # Definición de la transacción
    def transaction(conn: Connection):
        # Inicialización de contexto de ejecución
        execution_ctx = main._create_execution_context(DATA_RESOURCE.ROOT_USER, conn)
        # Se busca el usuario
        found_users: _Records[_base_users] = main._crud.search_read(
            execution_ctx,
            MODEL_NAME.BASE_USERS,
            [('login', '=', username)],
            ['login', 'active', 'password'],
        )

        # Si no se encontró usuario...
        if not found_users:
            # Se arroja error de usuario no encontrado
            raise UserNotFoundError(ERROR_LABEL.AUTHENTICATION.USER_NOT_FOUND)

        # Obtención de los datos del usuario
        [ user_data ] = found_users

        # Si el usuario no está activo...
        if not user_data['active']:
            # Se arroja error de usuario inactivo
            raise UserNotActiveError(ERROR_LABEL.AUTHENTICATION.USER_NOT_ACTIVE)

        # Obtención de la contraseña hasheada
        hashed_password: str = user_data['password']
        # Obtención de la ID del usuario
        user_id = user_data['id']

        # Verificación de la contraseña
        is_pwd_correct = verify_password(password, hashed_password)

        # Si la contraseña no es correcta...
        if not is_pwd_correct:
            # Se arroja error de contraseña incorrecta
            raise IncorrectPasswordError(ERROR_LABEL.AUTHENTICATION.INCORRECT_PASSWORD)

        # Creación de UUID de sesión
        session_uuid = uuid4().__str__()

        # Hasheo de la UUID de sesión
        hashed_session_uuid = (
            sha256( session_uuid.encode() )
            .hexdigest()
        )

        # Creación de sesión de usuario
        main._crud.create(
            execution_ctx,
            MODEL_NAME.BASE_USER_SESSION,
            {
                'name': hashed_session_uuid,
                'user_id': user_id,
                'validity_time': timedelta(days= DEFAULTS.EXPIRATION_TOKEN_DAYS),
            },
        )

        # Se realiza commit
        conn.commit()

        return session_uuid

    return transaction

def build_authenticate_user_callback(
    main: 'Lylac[_M]',
    session_uuid: str,
):

    # Definición de la transacción
    def transaction(conn: Connection) -> int:
        # Inicialización de contexto de ejecución
        execution_ctx = main._create_execution_context(DATA_RESOURCE.ROOT_USER, conn)

        # Hasheo de la UUID de sesión
        hashed_session_uuid = (
            sha256( session_uuid.encode() )
            .hexdigest()
        )

        # Búsqueda y lectura de la sesión
        found: _Records[_found_session] = main._crud.search_read(
            execution_ctx,
            MODEL_NAME.BASE_USER_SESSION,
            [('name', '=', hashed_session_uuid)],
            [
                ('is_active_session', TTYPE_NAME.BOOLEAN, lambda ctx: ctx['expires_at'] > datetime.now()),
                ('user_id.id', 'uid'),
                ('user_id.active', 'user_is_active'),
            ],
        )

        # Si no fue encontrado ningún registro de sesión de usuario...
        if not found:
            # Se arroja error de UUID de sesión inválida
            raise InvalidSessionUUIDError(ERROR_LABEL.AUTHENTICATION.INVALID_SESSION_UUID)

        # Obtención del registro de sesión
        [ session_record ] = found

        # Obtención de datos de la sesión
        is_active_session = session_record['is_active_session']
        user_is_active = session_record['user_is_active']
        uid = session_record['uid']

        # Si la sesión ya no está activa...
        if not is_active_session:
            # Se arroja error de sesión expirada
            raise ExpiredSessionError(ERROR_LABEL.AUTHENTICATION.EXPIRED_SESSION)

        # Si el usuario no está activo...
        if not user_is_active:
            # Se arroja error de usuario desactivado
            raise UserNotActiveError(ERROR_LABEL.AUTHENTICATION.USER_NOT_ACTIVE)

        return uid

    return transaction
