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
"""
### Valor de registro
Este tipo de dato representa los tipos de dato válidos para diversos
argumentos de entrada en métodos del módulo así como en funcionamientos
internos, retornos en JSON y validaciones.
"""

# Tipo de transacción de creación o modificación de datos
ModificationTransaction = Literal['create', 'update']
"""
### Transacción de modificación
>>> Literal['create', 'update']
"""

# Tipo de transacción de eliminación de datos
_DeleteTransaction = Literal['delete']
"""
### Transacción de eliminación
>>> Literal['delete']
"""

# Tipo de transacción de datos
Transaction = Union[ModificationTransaction, _DeleteTransaction]
"""
### Transación de base de datos
Se omite el método `'select'` ya que no se utiliza para este tipado.
>>> Literal['create', 'update', 'delete']
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
"""
