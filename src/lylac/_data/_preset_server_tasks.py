from typing import TYPE_CHECKING
from .._constants import PRESET
from .._resources import ServerTaskProperties

if TYPE_CHECKING:
    from .._contexts import ServerTaskContext

def _update_instance_metadata(ctx: ServerTaskContext):

    # Actualización de los metadatos de la instancia
    ctx._execution_ctx.database_metadata.update(ctx._execution_ctx.conn)

PRESET_SERVER_TASKS: dict[str, ServerTaskProperties] = {

    PRESET.SERVER_TASK.UPDATE_INSTANCE_METADATA: ServerTaskProperties(
        PRESET.SERVER_TASK.UPDATE_INSTANCE_METADATA,
        _update_instance_metadata,
    ),

}
