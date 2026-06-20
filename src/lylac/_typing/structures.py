from typing import Any
from typing import Literal
from typing import TypedDict
from typing import Union
from typing import TYPE_CHECKING
from .aliases import AliasedField
from .aliases import DMLCompatible
from .aliases import JSONLikeScalar
from .aliases import RecordValueDataType
from .generics import Array
from .generics import ItemOrList
from .generics import MaybeNone
from .generics import ModelName
from .literals import ComparisonOperator
from .literals import TTypeName
from .literals import LogicOperator
from .type_parameters import _M
from .type_parameters import _T

if TYPE_CHECKING:
    from .callables import ComputeFieldFn

JSONLikeObjShape = dict[str, Array[ Union['JSONLikeScalar', 'JSONLike'] ]]
"""
### Diccionario serializable
Diccionario compatible para ser serializado a tipo de dato `JSONB` por el motor
de PostgreSQL.

- El tipo de dato de la llave debe ser `str`.
- El tipo de dato del valor puede ser escalar, lista o tupla de:
    - `JSONLikeScalar`
    - `JSONLike`
"""

JSONLike = Array[ Union[JSONLikeObjShape, 'JSONLikeScalar'] ]
"""
Tipo de dato compatible para ser serializado a tipo de dato `JSONB` por el
motor de PostgreSQL.

El tipo de dato puede ser escalar, lista o tupla de:
- `JSONLikeScalar` que representa los tipos:
    - `int`
    - `float`
    - `str`
    - `bool`
    - `None`
- `JSONLikeObjShape` que representa un diccionario serializable conformado
por:
    - Llaves que deben ser de tipo `str`
    - Valores que pueden ser escalar, lista o tupla de:
        - `JSONLikeScalar`
        - `JSONLike`

Los valores son convertidos a notación *JSON* (JavaScript Object Notation):
- `int` → `number` (Sin punto decimal)
- `float` → `number` (Con punto decimal)
- `str` → `string`
- `bool` → `boolean`
- `dict` → `object`
- `list` → `array`
- `tuple` → `array`
"""

ComputeContextHub = dict[ModelName[_M], dict[str, 'ComputeFieldFn[_M]']]

FieldComputation = tuple[str, 'TTypeName', 'ComputeFieldFn']

_ExpansionSpec = list[Union[str, 'FrameReadField']] | Literal[True]
_ArrayExpansion = tuple[str, _ExpansionSpec]
_FieldName = str
_FieldAlias = str
_Aliased = tuple[_T, _FieldAlias]
_NestedExpansion = Union[_ArrayExpansion, _Aliased[_ArrayExpansion]]

FrameReadField = Union[_FieldName, _Aliased[_FieldName], FieldComputation]

FieldReadDeclaration = Union[FrameReadField, _NestedExpansion]

RecordIDs = ItemOrList[int]
"""
### IDs de registros
Escalar o una lista de `int` que representa IDs de registros en tablas de la
base de datos.
"""

class RelationCommand:
    class Create(TypedDict):
        create: ItemOrList[RecordData]
    class Add(TypedDict):
        add: RecordIDs
    class Update(TypedDict):
        update: ItemOrList[ tuple[RecordIDs, RecordData] ]
    class Replace(TypedDict):
        replace: RecordIDs
    class Unlink(TypedDict):
        unlink: RecordIDs
    class Delete(TypedDict):
        delete: RecordIDs
    class Clear(TypedDict):
        clear: Literal[True]

RelationCommands = Union[
    RelationCommand.Create,
    RelationCommand.Add,
    RelationCommand.Update,
    RelationCommand.Replace,
    RelationCommand.Unlink,
    RelationCommand.Delete,
    RelationCommand.Clear,
]
"""
### Comandos de relación
Este tipo de dato representa un diccionario que contiene comandos de
modificación de los registros referenciados en campos de tipo `one2many` y
`many2many` ya sea crear, añadir, desvincular, reemplazar o limpiar la lista
de registros relacionados o modificando registros específicos desde el registro
que los referencía.

Las llaves y valores del diccionario son:
- `'create'`: Escalar o lista de `RecordData`.
- `'add'`: Escalar o lista de `int`.
- `'update'`: Tupla de:
    - Escalar o lista de `int`.
    - `RecordData`
- `'replace'`: Escalar o lista de `int`.
- `'unlink'`: Escalar o lista de `int`.
- `'delete'`: Escalar o lista de `int`.
- `'clear'`: Literal `True`.
"""

RecordValue = Union[DMLCompatible, JSONLike, RelationCommands, 'RecordData']
"""
### Valor de registro
Tipo de dato que se puede usar como valor para un campo de modelo en la base
datos al crear o modificar registros, tipo de dato compatible para ser
serializado a tipo de dato JSONB por el motor de PostgreSQL o diccionario que
contiene comandos de modificación de los registros referenciados en campos de
tipo `one2many` y `many2many` ya sea crear, añadir, desvincular, reemplazar o
limpiar la lista de registros relacionados o modificando registros específicos
desde el registro que los referencía.

Los valores posibles pueden ser:
- `DMLCompatible`:
    - `int`
    - `float`
    - `str`
    - `bool`
    - `datetime.date`
    - `datetime.datetime`
    - `datetime.time`
    - `datetime.timedelta`
    - `None`
- `JSONLike` que puede ser un escalar o lista de:
    - `JSONLikeScalar` que representa los tipos:
        - `int`
        - `float`
        - `str`
        - `bool`
        - `None`
    - `JSONLikeObjShape` que representa un diccionario serializable conformado
    por:
        - Llaves que deben ser de tipo `str`
        - Valores que pueden ser escalar, lista o tupla de:
            - `JSONLikeScalar`
            - `JSONLike`
- `RelationCommands` que representa un diccionario con llaves y valores
mapeados como:
    - `'create'`: Escalar o lista de `RecordData`.
    - `'add'`: Escalar o lista de `int`.
    - `'update'`: Tupla de:
        - Escalar o lista de `int`.
        - `RecordData`
    - `'replace'`: Escalar o lista de `int`.
    - `'unlink'`: Escalar o lista de `int`.
    - `'delete'`: Escalar o lista de `int`.
    - `'clear'`: Literal `True`.
- `RecordData` que representa un diccionario de datos para crear un registro de
tipo Many2one que puede contener como valores cualquiera de los tipos anteriores.
"""

RecordData = dict[str, RecordValue]
"""
## Datos de registro
Diccionario que contiene los datos de un registro para ser creado o modificado.

- Las llaves deben ser de tipo `str`.
- Los valores pueden ser cualquiera de:
    - `DMLCompatible`:
        - `int`
        - `float`
        - `str`
        - `bool`
        - `datetime.date`
        - `datetime.datetime`
        - `datetime.time`
        - `datetime.timedelta`
        - `None`
    - `JSONLike` que puede ser un escalar o lista de:
        - `JSONLikeScalar` que representa los tipos:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `None`
        - `JSONLikeObjShape` que representa un diccionario serializable
        conformado por:
            - Llaves que deben ser de tipo `str`
            - Valores que pueden ser escalar, lista o tupla de:
                - `JSONLikeScalar`
                - `JSONLike`
    - `RelationCommands` que representa un diccionario con llaves y valores
    mapeados como:
        - `'create'`: Escalar o lista de `RecordData`.
        - `'add'`: Escalar o lista de `int`.
        - `'update'`: Tupla de:
            - Escalar o lista de `int`.
            - `RecordData`
        - `'replace'`: Escalar o lista de `int`.
        - `'unlink'`: Escalar o lista de `int`.
        - `'delete'`: Escalar o lista de `int`.
        - `'clear'`: Literal `True`.

----
### # `DMLCompatible`
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

----
### # `JSONLike`
Tipo de dato compatible para ser serializado a tipo de dato `JSONB` por el
motor de PostgreSQL.

El tipo de dato puede ser escalar, lista o tupla de:
- `JSONLikeScalar` que representa los tipos:
    - `int`
    - `float`
    - `str`
    - `bool`
    - `None`
- `JSONLikeObjShape` que representa un diccionario serializable conformado
por:
    - Llaves que deben ser de tipo `str`
    - Valores que pueden ser escalar, lista o tupla de:
        - `JSONLikeScalar`
        - `JSONLike`

Los valores son convertidos a notación *JSON* (JavaScript Object Notation):
- `int` → `number` (Sin punto decimal)
- `float` → `number` (Con punto decimal)
- `str` → `string`
- `bool` → `boolean`
- `dict` → `object`
- `list` → `array`
- `tuple` → `array`

----
### # `JSONLikeObjShape`
Diccionario compatible para ser serializado a tipo de dato `JSONB` por el motor
de PostgreSQL.

- El tipo de dato de la llave debe ser `str`.
- El tipo de dato del valor puede ser escalar, lista o tupla de:
    - `JSONLikeScalar`
    - `JSONLike`

----
### # `JSONLikeScalar`
Tipo de dato escalar serializable a JSON.

El tipo de dato puede ser:
- `int`
- `float`
- `str`
- `bool`
- `None`

----
### # `RelationCommands`
Este tipo de dato representa un diccionario que contiene comandos de
modificación de los registros referenciados en campos de tipo `one2many` y
`many2many` ya sea crear, añadir, desvincular, reemplazar o limpiar la lista
de registros relacionados o modificando registros específicos desde el registro
que los referencía.

Las llaves y valores del diccionario son:
- `'create'`: Escalar o lista de `RecordData`.
- `'add'`: Escalar o lista de `int`.
- `'update'`: Tupla de:
    - Escalar o lista de `int`.
    - `RecordData`
- `'replace'`: Escalar o lista de `int`.
- `'unlink'`: Escalar o lista de `int`.
- `'delete'`: Escalar o lista de `int`.
- `'clear'`: Literal `True`.
"""

CriteriaValue = ItemOrList[ MaybeNone[RecordValueDataType] ]

TripletStructure = tuple[str, ComparisonOperator, CriteriaValue]

CriteriaStructure = list[ Union[LogicOperator, TripletStructure] ]
"""
## Estructura de criterio de búsqueda
La estructura del criterio de búsqueda consiste en una lista de dos tipos de
dato:
- `TripletStructure`: Estructura de tripletas para queries SQL
- `LogicOperator`: Operador lógico

Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
primera posición:
>>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
>>> # "amount" es mayor a 500 y "name" contiene "as"
>>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
>>> # "id" es igual a 5 o "state" es igual a "posted"

----
### Operador lógico
Tipo de dato que representa un operador lógico.

Los operadores lógicos disponibles son:
- `'&'`: AND
- `'|'`: OR

----
### Estructura de tripletas para queries SQL
Este tipo de dato representa una condición sencilla para usarse en una
transacción en base de datos.

La estructura de una tripleta consiste en 3 diferentes parámetros:
1. Nombre del campo del modelo
2. Operador de comparación
3. Valor de comparación

Algunos ejemplos de tripletas son:
>>> ('name', '=', 'Onnymm')
>>> # Nombre es igual a "Onnymm"
>>> ('id', '=', 5)
>>> # ID es igual a 5
>>> ('amount', '>', 500)
>>> # "amount" es mayor a 500
>>> ('name', 'ilike', 'as')
>>> # "name" contiene "as"

----

### Operador de comparación
Tipo de dato que representa una operador de comparación.

Los operadores de comparación disponibles son:
- `'='`: Igual a
- `'!='`: Diferente de
- `'>'`: Mayor a
- `'>='`: Mayor o igual a
- `'<'`: Menor que
- `'<='`: Menor o igual que
- `'in'`: Está en
- `'not in'`: No está en
- `'ilike'`: Contiene
- `'not ilike'`: No contiene
- `'~'`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
- `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)
"""

RawFieldProperties = tuple[str, TTypeName, bool, ModelName[_M], str]
