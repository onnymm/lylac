import os
from .._settings import ENV_VARIABLE_NAME

class ENV_VARIABLES:
    class INTERNAL_USER:
        LOGIN = os.environ.get(ENV_VARIABLE_NAME.INTERNAL_USER.LOGIN)
        NAME = os.environ.get(ENV_VARIABLE_NAME.INTERNAL_USER.NAME)
