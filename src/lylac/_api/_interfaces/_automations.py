from typing import Generic
from ..._constants import FIELD_NAME
from ..._engines import AutomationsEngine
from ..._typing.generics import ModelName
from ..._typing.literals import DMLTransaction
from ..._typing.structures import CriteriaStructure
from ..._typing.structures import FieldReadDeclaration
from ..._typing.type_parameters import _M

class _Interface_Automations(Generic[_M]):
    _engine: AutomationsEngine[_M]

    def __init__(
        self,
        engine: AutomationsEngine[_M],
    ) -> None:

        # Asignación de motor de automatizaciones
        self._engine = engine

    def register(
        self,
        on: DMLTransaction,
        model_name: ModelName[_M],
        fields: list[FieldReadDeclaration] = [FIELD_NAME.ID],
        execute_only_when: CriteriaStructure = [],
    ) -> None:

        # Obtención del decorador para registrar la función
        decorator = self._engine.register(
            on,
            model_name,
            fields,
            execute_only_when,
        )

        return decorator
