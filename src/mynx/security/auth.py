from passlib.context import CryptContext

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
    pwd = hash_password('123456')

    return pwd

def verify_password(
    input_password: str,
    hashed_password: str,
) -> bool:

    # Verificación de la contraseña
    is_correct = _pwd_context.verify(input_password, hashed_password)

    return is_correct
