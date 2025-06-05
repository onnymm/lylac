from typing import (
    Callable,
    Literal,
    Union,
)
import pandas as pd
from ._base import RecordValue

# Opciones de salida de datos
OutputOptions = Literal['dataframe', 'dict']
"""
### Opciones de salida de datos
>>> Literal['dataframe', 'dict']
"""

# Tipo de dato retornado por métodos de lectura en el módulo principal
DataOutput = Union[pd.DataFrame | dict[str, RecordValue]]
"""
### Tipo de dato retornado
Tipo de dato retornado por métodos de lectura en el módulo principal
>>> Union[pd.DataFrame | dict[str, RecordValue]]
"""

# Función de automatización
AutomationCallback = Callable[[list[int]], None]
"""
### Función de automatización
Función utilizada para ejecutar una automación.
>>> def automation_do_something(record_ids: list[int]) -> None:
>>>     # do something
"""
