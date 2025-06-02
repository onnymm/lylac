from typing import (
    Literal,
    Union,
)

# Tipo de dato de valor para queries SQL
RecordValue = Union[
    int,
    float,
    str,
    bool,
    list[int],
    list[float],
    list[str],
    list[bool],
]

# Tipo de transacción de creación o modificación de datos
ModificationTransaction = Literal['create', 'update']

# Tipo de transacción de eliminación de datos
_DeleteTransaction = Literal['delete']

# Tipo de transacción de datos
Transaction = Union[ModificationTransaction, _DeleteTransaction]
"""
### Transación de base de datos
Se omite el método `'select'` ya que no se utiliza para este tipado.
"""

# Nombre de tipo dato en columnas base de datos
TType = Literal['integer', 'char', 'float', 'boolean', 'date', 'datetime', 'time', 'file', 'text', 'selection', 'many2one']

# Datos para la creación de un objeto
RecordData = dict[str, RecordValue]
"""
### Datos de registro
Datos que contienen los valores de campo de un registro en la base de datos.
Ejemplo
>>> # Un registro
>>> {
>>>     'name': 'Onnymm',
>>>     'password': ...,
>>>     'active': True,
>>> }
>>> 
>>> # Varios registros
>>> [
>>>     {
>>>         'name': 'Onnymm',
>>>         'password': ...,
>>>         'active': True,
>>>     },
>>>     {
>>>         'name': 'Lumii',
>>>         'password': ...,
>>>         'active': True,
>>>     },
>>> ]
"""
