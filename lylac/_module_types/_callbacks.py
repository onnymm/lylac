from typing import Callable
from ._models import (
    DataPerRecord,
    DataPerTransaction,
)

AutomationTemplate = Callable[[DataPerRecord | DataPerTransaction], None]
"""
### Función de automatización
Estructura que debe tener una función para registrarse como automatización
>>> def some_automation(params: DataPerRecord[Any]) -> None:
>>>     ...
"""
