from urllib.parse import quote
from .._core.env import env_

class CONFIG:
    ROOT_USER_NAME = env_.variable('ROOT_USER_NAME')

class CREDENTIALS:
    HOST = env_.variable('HOST')
    NAME = env_.variable('NAME')
    PORT = env_.variable('PORT', int)
    USER = env_.variable('USER')
    PASSWORD = env_.variable('PASSWORD', quote)
