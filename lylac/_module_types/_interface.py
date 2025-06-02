from typing import (
    Callable,
    Literal,
    Union,
)
import pandas as pd
from ._base import (
    RecordValue,
    Transaction,
    TType,
)
from ._base import (
    ModificationTransaction,
    Transaction,
)

# Tipo de dato de valor para queries SQL
_RecordValue = Union[
    int,
    float,
    str,
    bool,
    list[int],
    list[float],
    list[str],
    list[bool],
]

# Opciones de salida de datos
OutputOptions = Literal['dataframe', 'dict']

# Tipo de dato retornado por métodos de lectura en el módulo principal
DataOutput = Union[pd.DataFrame | dict[str, _RecordValue]]

# Función de automatización
AutomationCallback = Callable[[list[int]], None]
"""
### Función de automatización
Función utilizada para ejecutar una automación.
>>> def automation_do_something(record_ids: list[int]) -> None:
>>>     # do something
"""
