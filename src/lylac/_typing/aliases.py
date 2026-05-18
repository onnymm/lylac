from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from typing import Union
from sqlalchemy.orm import DeclarativeBase

ModelClass = type[DeclarativeBase]
"""
### Clase de modelo
Representación de una clase de modelo de SQLAlchemy.
"""

AliasedField = tuple[str, str]
"""
### Campo con alias
Representación de la invocación de un campo renombrado en lectura de un método
de lectura desde la base de datos.
"""

JSONLikeScalar = Union[int, float, str, bool, None]
"""
### Escalar serializable
Tipo de dato escalar serializable a JSON.

El tipo de dato puede ser:
- `int`
- `float`
- `str`
- `bool`
- `None`
"""

DMLCompatible = Union[int, float, str, bool, date, datetime, time, timedelta, None]
"""
### Compatible para PostgreSQL
Tipo de dato que se puede usar como valor para un campo de modelo en la base
datos al crear o modificar registros.

El tipo de dato puede ser:
- `int`
- `float`
- `str`
- `bool`
- `datetime.date`
- `datetime.datetime`
- `datetime.time`
- `datetime.timedelta`
- `None`
"""

RecordValueDataType = Union[bool, int, float, str, date, datetime, time, timedelta]
