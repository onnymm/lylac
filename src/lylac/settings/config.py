from urllib.parse import quote
from .._core._env import env
from .._constants import DEFAULTS

class CONFIG:
    ROOT_USER_NAME = env.variable('ROOT_USER_NAME')
    ROOT_USER_LOGIN = env.variable('ROOT_USER_LOGIN')
    ADMIN_USER_NAME = env.variable('ADMIN_USER_NAME')
    ADMIN_USER_LOGIN = env.variable('ADMIN_USER_LOGIN')

class CREDENTIALS:
    HOST = env.variable('HOST')
    NAME = env.variable('NAME')
    PORT = env.variable('PORT', int)
    USER = env.variable('USER')
    PASSWORD = env.variable('PASSWORD', quote)

class DIRECTORY:
    MODULES = 'modules'

class SETTINGS:
    class DATABASE:
        CHAR_FIELD_LENGHT = env.variable('CHAR_FIELD_LENGHT', int, DEFAULTS.CHAR_FIELD_LENGHT)
        SELECTION_FIELD_LENGHT = env.variable('SELECTION_FIELD_LENGHT', int, DEFAULTS.SELECTION_FIELD_LENGHT)

    class SECURITY:
        DEFAULT_PASSWORD = env.variable('DEFAULT_PASSWORD', str)
        TOKEN_EXPIRATION_DAYS = env.variable('TOKEN_EXPIRATION_DAYS', int, DEFAULTS.TOKEN_EXPIRATION_DAYS)
