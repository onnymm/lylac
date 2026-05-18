from .._constants import FIELD_NAME
from .._constants import MODEL_NAME
from .._typing.structures import ComputeContextHub
from .._typing.type_parameters import _M

DEFAULT_COMPUTATION_CALLBACKS: ComputeContextHub[_M] = {
    MODEL_NAME.BASE_USERS: {
        FIELD_NAME.DISPLAY_NAME: (
            lambda ctx: ctx[FIELD_NAME.NAME]
        )
    },
    MODEL_NAME.BASE_USER_SESSION: {
        'expires_at': (
            lambda ctx: ctx['create_date'] + ctx['validity_time']
        )
    },
    MODEL_NAME.BASE_MODEL: {
        FIELD_NAME.DISPLAY_NAME: (
            lambda ctx: ctx['model']
        )
    },
    MODEL_NAME.BASE_MODEL_FIELD: {
        FIELD_NAME.DISPLAY_NAME: (
            lambda ctx: ctx.concat(ctx['label'], ' (', ctx['model_id.model'], ')')
        )
    },
    MODEL_NAME.BASE_MODEL_FIELD_SELECTION: {
        FIELD_NAME.DISPLAY_NAME: (
            lambda ctx: ctx['label']
        )
    },
    MODEL_NAME.BASE_MODEL_DATA: {
        FIELD_NAME.DISPLAY_NAME: (
            lambda ctx: ctx[FIELD_NAME.NAME]
        )
    },
    MODEL_NAME.BASE_MODEL_DATA_PROCESS: {
        FIELD_NAME.DISPLAY_NAME: (
            lambda ctx: ctx[FIELD_NAME.NAME]
        )
    },
    MODEL_NAME.BASE_MODEL_DATA_PROCESS_STEP: {
        FIELD_NAME.DISPLAY_NAME: (
            lambda ctx: ctx.concat( ctx['process_id.name'], ' - ', ctx[FIELD_NAME.SEQUENCE] )
        )
    },
}
