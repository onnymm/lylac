from typing import (
    Literal,
    Optional,
    TypedDict,
    Union,
)
from pydantic import BaseModel
from ._base import (
    RecordValue,
    Transaction,
    TType,
)

# Formato de credenciales para uso de base de datos
class DBCredentials(TypedDict):
    host: str
    port: int
    db_name: str
    user: str
    password: str

# Operadores de comparación para queries SQL
ComparisonOperator = Literal['=', '!=', '>', '>=', '<', '<=', '><', 'in', 'not in', 'ilike', 'not ilike', '~', '~*']
# Operadores lógicos para queries SQL
LogicOperator = Literal['&', '|']
# Estructura de tripletas para queries SQL
TripletStructure = tuple[str, ComparisonOperator, RecordValue]
# Estructura de criterios de búsqueda para queries SQL
CriteriaStructure = list[
    Union[
    LogicOperator,
        TripletStructure
    ]
]
"""
### Estructura de criterio de búsqueda
La estructura del criterio de búsqueda consiste en una lista de tuplas de 3 valores, mejor
conocidas como tripletas. Cada una de estas tripletas consiste en 3 diferentes parámetros:
1. Nombre del campo de la tabla
2. Operador de comparación
3. Valor de comparación

Algunos ejemplos de tripletas son:
>>> ('id', '=', 5)
>>> # ID es igual a 5
>>> ('amount', '>', 500)
>>> # "amount" es mayor a 500
>>> ('name', 'ilike', 'as')
>>> # "name" contiene "as"

Los operadores de comparación disponibles son:
- `'='`: Igual a
- `'!='`: Diferente de
- `'>'`: Mayor a
- `'>='`: Mayor o igual a
- `'<`': Menor que
- `'<='`: Menor o igual que
- `'><'`: Entre
- `'in'`: Está en
- `'not in'`: No está en
- `'ilike'`: Contiene
- `'not ilike'`: No contiene
- `'~'`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
- `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)

Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
Unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
primera posición:
>>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
>>> # "amount" es mayor a 500 y "name" contiene "as"
>>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
>>> # "id" es igual a 5 o "state" es igual a "posted"

Los operadores lógicos disponibles son:
- `'&'`: AND
- `'|'`: OR
"""

class _NewRecord(TypedDict):
    name: str
    label: str

class NewModel(_NewRecord):
    model: str
    description: str

class NewModelField(_NewRecord):
    ttype: TType
    model_id: int
    nullable: bool
    unique: bool
    default_value: Optional[str]

class NewModelFieldSelection(_NewRecord):
    field_id: int

Submodule = Literal['_ddl', '_automations']

class AutomationDataDict(TypedDict):
    submodule: Submodule
    callback: str
    model: str
    transaction: Transaction
    criteria: CriteriaStructure
    fields: list[str]
    execution: Literal['record', 'all']

class AutomationDataModel(BaseModel):
    submodule: Submodule
    callback: str
    model: str
    transaction: Transaction
    criteria: CriteriaStructure
    fields: list[str]
    execution: Literal['record', 'all']
