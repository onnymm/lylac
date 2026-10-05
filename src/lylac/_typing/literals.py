from typing import Literal

InitialModels = Literal[
    'base.model',
    'base.model.data',
    'base.model.data.process',
    'base.model.data.process.step',
    'base.model.data.process.step.record',
    'base.model.field',
    'base.model.field.selection',
    'base.rules',
    'base.users',
    'base.users.role',
    'base.users.update.password',
    'base.users.access',
    'base.users.group',
    'base.users.session',
]

TTypeName = Literal[
    'integer',
    'char',
    'float',
    'boolean',
    'date',
    'datetime',
    'time',
    'duration',
    'file',
    'text',
    'selection',
    'many2one',
    'one2many',
    'many2many',
    'json',
]
"""
## Tipo de dato en campo de modelo en la base de datos
Tipo de dato válido en un campo de un modelo de la base de datos.
- `'integer'`: Entero
- `'char'`: Cadena de texto
- `'float'`: Flotante
- `'boolean'`: Booleano
- `'date'`: Fecha
- `'datetime'`: Fecha y hora
- `'time'`: Hora
- `'duration'`: Duración en tiempo
- `'file'`: Archivo binario
- `'text'`: Texto largo
- `'selection'`: Selección
- `'many2one'`: Muchos a uno
- `'one2many'`: Uno a muchos
- `'many2many'`: Muchos a muchos
- `'json'`: JSON
"""

OnDeleteOption = Literal['cascade', 'restrict', 'set_null']

StateOption = Literal['base', 'generic']

AggFuncName = Literal['sum', 'max', 'min', 'mean', 'count', 'array']
"""
### Nombre de función de agregación
Nombres de funciones de agregación para utilizar en cómputos de campo de tipo
`one2many` y `many2many`.
"""

ComparisonOperator = Literal[
    '=',
    '!=',
    '=?',
    '>',
    '>=',
    '<',
    '<=',
    'in',
    'not in',
    'like',
    'ilike',
    'not like',
    'not ilike',
    'starts with',
    'ends with',
    '~',
    '~*',
    '!~',
    '!~*',
]
"""
### Operador de comparación
Tipo de dato que representa una operador de comparación.

Los operadores de comparación disponibles son:
- `'='`: Igual a
- `'!='`: Diferente de
- `'=?'`: No está establecido o es igual a
- `'>'`: Mayor a
- `'>='`: Mayor o igual a
- `'<'`: Menor que
- `'<='`: Menor o igual que
- `'in'`: Está en
- `'not in'`: No está en
- `'like'`: Contiene (sensible a mayúsculas y minúsculas)
- `'ilike'`: Contiene (no sensible a mayúsculas y minúsculas)
- `'not like'`: No contiene (sensible a mayúsculas y minúsculas)
- `'not ilike'`: No contiene (no sensible a mayúsculas y minúsculas)
- `'starts with'`: Comienza con (sensible a mayúsculas y minúsculas)
- `'ends with'`: Termina con (sensible a mayúsculas y minúsculas)
- `'~'`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
- `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)
- `!'~'`: No coincide con expresión regular (sensible a mayúsculas y minúsculas)
- `!'~*'`: No coincide con expresión regular (no sensible a mayúsculas y minúsculas)
"""

LogicOperator = Literal['&', '|']
"""
### Operador lógico
Tipo de dato que representa un operador lógico.

Los operadores lógicos disponibles son:
- `'&'`: AND
- `'|'`: OR
"""

DMLTransaction = Literal['create', 'update', 'delete']

RelationActionName = Literal[
    'create',
    'add',
    'update',
    'unlink',
    'clear',
    'replace',
    'delete',
]

CRUDPermission = Literal['read'] | DMLTransaction

CRUDPermissionColumnName = Literal['perm_create', 'perm_read', 'perm_update', 'perm_delete']

LiteralTarget = Literal['current_user']
