import pandas as pd
from typing import Callable
from ...._module_types import TType

class _DataTypes_Interface():
    recover_ttype: dict[TType, Callable[[pd.DataFrame, str], pd.DataFrame]]
