from urllib.parse import quote
from .._core.env import env_
from .._constants import DEFAULTS

class CONFIG:
    ROOT_USER_NAME = env_.variable('ROOT_USER_NAME')
    ROOT_USER_LOGIN = env_.variable('ROOT_USER_LOGIN')
    ADMIN_USER_NAME = env_.variable('ADMIN_USER_NAME')
    ADMIN_USER_LOGIN = env_.variable('ADMIN_USER_LOGIN')

class CREDENTIALS:
    HOST = env_.variable('HOST')
    NAME = env_.variable('NAME')
    PORT = env_.variable('PORT', int)
    USER = env_.variable('USER')
    PASSWORD = env_.variable('PASSWORD', quote)

class DIRECTORY:
    MODULES = 'modules'

class SETTINGS:
    class DATABASE:
        CHAR_FIELD_LENGHT = env_.variable('CHAR_FIELD_LENGHT', int, DEFAULTS.CHAR_FIELD_LENGHT)
        SELECTION_FIELD_LENGHT = env_.variable('SELECTION_FIELD_LENGHT', int, DEFAULTS.SELECTION_FIELD_LENGHT)

    class SECURITY:
        DEFAULT_PASSWORD = env_.variable('DEFAULT_PASSWORD', str)
        EXPIRATION_TOKEN_DAYS = env_.variable('EXPIRATION_TOKEN_DAYS', int, DEFAULTS.EXPIRATION_TOKEN_DAYS)
