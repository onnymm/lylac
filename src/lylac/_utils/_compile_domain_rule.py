from typing import TYPE_CHECKING
from .._typing.structures import CriteriaStructure
from .._typing.definitions import JSONLike
from datetime import datetime
from datetime import date

if TYPE_CHECKING:
    from .._contexts import ExecutionContext

_ACCESS = ''

def parse_record_rule(
    execution_ctx: 'ExecutionContext',
    json_record_rule: JSONLike,
) -> CriteriaStructure:

    # Inicialización de diccionario de acceso
    _closure = {}

    # Ejecución de código para compilar la regla de registro
    exec(
        f"_closure['{_ACCESS}'] = {json_record_rule}",
        globals= {'__builtins__': {}},
        locals= {
            '_closure': _closure,
            'uid': execution_ctx.uid,
            'now': datetime.now(),
            'today': date.today(),
            'user': execution_ctx._env,
        },
    )

    # Obtención de la registro compilada
    criteria_structure_rule = _closure[_ACCESS]

    return criteria_structure_rule
