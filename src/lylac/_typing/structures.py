from typing import Iterable
from typing import Literal
from typing import TypedDict
from typing import Union
from typing import TYPE_CHECKING
from .aliases import FieldName
from .aliases import DMLScalarCompatible
from .aliases import JSONLikeScalar
from .literals import LiteralTarget
from .generics import Array
from .generics import ScalarOrIterable
from .generics import ModelName
from .literals import ComparisonOperator
from .literals import TTypeName
from .literals import LogicOperator
from .type_parameters import _M
from .type_parameters import _T

if TYPE_CHECKING:
    from .callables import ComputeFieldFn
    from .callables import ValueResolutionFn

JSONLikeObjShape = dict[str, ScalarOrIterable[ Union['JSONLikeScalar', 'JSONLike'] ]]
"""
### Diccionario serializable
Diccionario compatible para ser serializado a tipo de dato `JSONB` por el motor
de PostgreSQL.

- El tipo de dato de la llave debe ser `str`.
- El tipo de dato del valor puede ser escalar o iterable de:
    - `JSONLikeScalar`
    - `JSONLike`
"""

JSONLike = ScalarOrIterable[ Union[JSONLikeObjShape, 'JSONLikeScalar'] ]
"""
Tipo de dato compatible para ser serializado a tipo de dato `JSONB` por el
motor de PostgreSQL.

El tipo de dato puede ser escalar o iterable de:
- `JSONLikeScalar` que representa los tipos:
    - `int`
    - `float`
    - `str`
    - `bool`
    - `None`
- `JSONLikeObjShape` que representa un diccionario serializable conformado
por:
    - Llaves que deben ser de tipo `str`
    - Valores que pueden ser escalar o iterable de:
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

ParsedFromInput = Union[DMLScalarCompatible, JSONLike]
"""
### Tipo de dato parseado desde entrada
Tipo de dato parseado desde una entrada de datos.
Este tipado garantiza el tipo de dato estándar para cada *TType*:

| TType       | Python               |
|-------------|----------------------|
| `integer`   | `int`                |
| `char`      | `str`                |
| `boolean`   | `bool`               |
| `float`     | `float`              |
| `selection` | `str`                |
| `date`      | `datetime.date`      |
| `time`      | `datetime.time`      |
| `datetime`  | `datetime.datetime`  |
| `duration`  | `datetime.timedelta` |
| `many2one`  | `int`                |
| `text`      | `str`                |
| `file`      | `BytesIO`            |
| `JSON`      | `JSONLike`           |

### # `JSONLike`
Tipo de dato compatible para ser serializado a tipo de dato `JSONB` por el
motor de PostgreSQL.

El tipo de dato puede ser escalar o iterable de:
- `JSONLikeScalar` que representa los tipos:
    - `int`
    - `float`
    - `str`
    - `bool`
    - `None`
- `JSONLikeObjShape` que representa un diccionario serializable conformado
por:
    - Llaves que deben ser de tipo `str`
    - Valores que pueden ser escalar o iterable de:
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

### # JSONLikeScalar
Tipo de dato escalar serializable a JSON.

El tipo de dato puede ser:
- `int`
- `float`
- `str`
- `bool`
- `None`

### # JSONLikeObjShape
Diccionario compatible para ser serializado a tipo de dato `JSONB` por el motor
de PostgreSQL.

- El tipo de dato de la llave debe ser `str`.
- El tipo de dato del valor puede ser escalar o iterable de:
    - `JSONLikeScalar`
    - `JSONLike`
"""

ComputeContextHub = dict[ModelName[_M], dict[str, 'ComputeFieldFn']]

FieldComputation = tuple[FieldName, 'TTypeName', 'ComputeFieldFn']

_ExpansionSpec = Iterable['FieldReadDeclaration'] | Literal[True]

_ArrayExpansion = tuple[FieldName, _ExpansionSpec]

_Aliased = tuple[_T, str]

FrameReadField = Union[FieldName, _Aliased[FieldName], FieldComputation]

Aliaseddd = _Aliased[Union[FieldName, FieldComputation, _ArrayExpansion]]

FieldReadDeclaration = Union[FieldName, FieldComputation, _ArrayExpansion, Aliaseddd]

RecordIDs = ScalarOrIterable[int]
"""
### IDs de registros
Escalar o iterable de `int` que representa IDs de registros en tablas de la
base de datos.
"""

class RelationCommand:
    class Create(TypedDict):
        create: ScalarOrIterable[InputRecordData[_M]]
    class Add(TypedDict):
        add: RecordIDs
    class Update(TypedDict):
        update: ScalarOrIterable[ tuple[RecordIDs, InputRecordData[_M]] ]
    class Replace(TypedDict):
        replace: RecordIDs
    class Unlink(TypedDict):
        unlink: RecordIDs
    class Delete(TypedDict):
        delete: RecordIDs
    class Clear(TypedDict):
        clear: Literal[True]

RelationCommands = Union[
    RelationCommand.Create[_M],
    RelationCommand.Add,
    RelationCommand.Update[_M],
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
- `'create'`: Escalar o iterable de `InputRecordData`.
- `'add'`: Escalar o iterable de `int`.
- `'update'`: Tupla de:
    - Escalar o iterable de `int`.
    - `InputRecordData`
- `'replace'`: Escalar o iterable de `int`.
- `'unlink'`: Escalar o iterable de `int`.
- `'delete'`: Escalar o iterable de `int`.
- `'clear'`: Literal `True`.
"""

type RecordValue[_M] = Union[DMLScalarCompatible, JSONLike, RelationCommands[_M], 'InputRecordData[_M]', 'ValueResolutionFn[_M]']
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
- `JSONLike` que puede ser un escalar o iterable de:
    - `JSONLikeScalar` que representa los tipos:
        - `int`
        - `float`
        - `str`
        - `bool`
        - `None`
    - `JSONLikeObjShape` que representa un diccionario serializable conformado
    por:
        - Llaves que deben ser de tipo `str`
        - Valores que pueden ser escalar o iterable de:
            - `JSONLikeScalar`
            - `JSONLike`
- `RelationCommands` que representa un diccionario con llaves y valores
mapeados como:
    - `'create'`: Escalar o iterable de `InputRecordData`.
    - `'add'`: Escalar o iterable de `int`.
    - `'update'`: Tupla de:
        - Escalar o iterable de `int`.
        - `InputRecordData`
    - `'replace'`: Escalar o iterable de `int`.
    - `'unlink'`: Escalar o iterable de `int`.
    - `'delete'`: Escalar o iterable de `int`.
    - `'clear'`: Literal `True`.
- `InputRecordData` que representa un diccionario de datos para crear un registro de
tipo Many2one que puede contener como valores cualquiera de los tipos anteriores.
"""

type InputRecordData[_M] = dict[FieldName, RecordValue[_M]]
"""
## Datos de registro
Diccionario que contiene los datos de un registro para ser creado o modificado.

- Las llaves deben ser de tipo `str`.
- Los valores pueden ser cualquiera de:
    - `DMLScalarCompatible`:
        - `int`
        - `float`
        - `str`
        - `bool`
        - `datetime.date`
        - `datetime.datetime`
        - `datetime.time`
        - `datetime.timedelta`
        - `None`
    - `JSONLike` que puede ser un escalar o iterable de:
        - `JSONLikeScalar` que representa los tipos:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `None`
        - `JSONLikeObjShape` que representa un diccionario serializable
        conformado por:
            - Llaves que deben ser de tipo `str`
            - Valores que pueden ser escalar o iterable de:
                - `JSONLikeScalar`
                - `JSONLike`
    - `RelationCommands` que representa un diccionario con llaves y valores
    mapeados como:
        - `'create'`: Escalar o iterable de `InputRecordData`.
        - `'add'`: Escalar o iterable de `int`.
        - `'update'`: Tupla de:
            - Escalar o iterable de `int`.
            - `InputRecordData`
        - `'replace'`: Escalar o iterable de `int`.
        - `'unlink'`: Escalar o iterable de `int`.
        - `'delete'`: Escalar o iterable de `int`.
        - `'clear'`: Literal `True`.

----
### # `DMLScalarCompatible`
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

El tipo de dato puede ser escalar o iterable de:
- `JSONLikeScalar` que representa los tipos:
    - `int`
    - `float`
    - `str`
    - `bool`
    - `None`
- `JSONLikeObjShape` que representa un diccionario serializable conformado
por:
    - Llaves que deben ser de tipo `str`
    - Valores que pueden ser escalar o iterable de:
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
- El tipo de dato del valor puede ser escalar o iterable de:
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
- `'create'`: Escalar o iterable de `InputRecordData`.
- `'add'`: Escalar o iterable de `int`.
- `'update'`: Tupla de:
    - Escalar o iterable de `int`.
    - `InputRecordData`
- `'replace'`: Escalar o iterable de `int`.
- `'unlink'`: Escalar o iterable de `int`.
- `'delete'`: Escalar o iterable de `int`.
- `'clear'`: Literal `True`.
"""

type CriteriaValue[_M] = Union[ ScalarOrIterable[DMLScalarCompatible], 'ValueResolutionFn[_M]' ]

FieldReference = Union[ FieldName, FieldComputation ]

TripletStructure = tuple[FieldReference, ComparisonOperator, CriteriaValue[_M]]

CriteriaStructure = list[ Union[LogicOperator, TripletStructure[_M]] ]
"""
## Estructura de criterio de búsqueda
La estructura del criterio de búsqueda expresa un conjunto de condiciones que
se pueden usar para filtrar registros en la base de datos al momento de leer o
invocar registros para un fin específico.

La estructura se conforma de un iterable con los tipos:
- `TripletStructure`: Tupla de 3 posiciones que representa una condición.
- `LogicOperator`: Operador lógico que une tripletas de condiciones.

----

### Estructura de tripletas de condición
Este tipo de dato representa una condición para usarse en una transacción en
base de datos.

La estructura de una tripleta consiste en 3 diferentes parámetros:
1. Referencia de campo. Puede ser alguno de los siguientes tipos:
    - `FieldName`: Nombre del campo del modelo o referencia *Many2One*
    - `FieldComputation`: Cómputo de campo.
Nombre del campo del modelo, referencia many2one o campo computado
2. Operador de comparación. Puede ser alguno de los siguientes literales:
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
    - `'~'`: Coincide con expresión regular (sensible a mayúsculas y
    minúsculas)
    - `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y
    minúsculas)
    - `!'~'`: No coincide con expresión regular (sensible a mayúsculas y
    minúsculas)
    - `!'~*'`: No coincide con expresión regular (no sensible a mayúsculas y
    minúsculas)
3. Valor de comparación. Puede ser alguno de los siguientes tipos:
    - `ScalarOrIterable[DMLScalarCompatible]`Escalar o iterable de Tipo de dato
    que se puede usar como valor para un campo de modelo. El tipo de dato puede
    ser:
        - `int`
        - `float`
        - `str`
        - `bool`
        - `datetime.date`
        - `datetime.datetime`
        - `datetime.time`
        - `datetime.timedelta`
        - `None`
    - `ValueResolutionFn[_M]`: Función de resolución de valor que se usa para
    resolver y retornar un valor que se usará en el campo para almacenarse en
    la base de datos

Algunos ejemplos de tripletas:
>>> ('name', 'like', 'Onnymm')
>>> # El nombre contiene 'Onnymm'
>>> ('id', '=', 5)
>>> # La ID es igual a 5
>>> ('create_uid.name', 'ends with', 'Azzur')
>>> # El nombre del usuario creador del registro termina con "Azzur"
>>> ('device_id.type_id.create_date', '=', lambda ctx: ctx.today())
>>> # La fecha de creación del tipo de dispostivo del dispositivo es igual a hoy
>>> (('subtotal', 'float', lambda ctx: ctx['qty'] * ctx['price']), '<', 500)
>>> # El cómputo del subtotal es menor a 500

Las tuplas de estructura se deben unir por medio de un operador lógico que va
al principio. Por ejemplo:
>>> ('amount', '>', 500)
>>> # El monto es mayor a 500
>>> ('name', 'ilike', 'as')
>>> # El nombre contiene "as"
>>> 
>>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
>>> # El monto es mayor a 500 y el nombre contiene "as"
----

### Operador lógico
Tipo de dato que representa un operador lógico.

Los operadores lógicos disponibles son:
- `'&'`: AND
- `'|'`: OR
"""

RawFieldProperties = tuple[str, TTypeName, bool, ModelName[_M], str]

NotificationTarget = Union[LiteralTarget, ScalarOrIterable[int]]
