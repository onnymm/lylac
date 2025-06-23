# lylac
Gestor de conexión a bases de datos altamente personalizable.

## Tipados principales

### Índice
**Base**
- [`RecordValue` Valor de registro](#recordvalue-valor-de-registro)
- [`RecordData` Datos de registro](#recorddata-datos-de-registro)

**Filtros**
- [`ComparisonOperator` Operador de comparación](#comparisonoperator-operador-de-comparación)
- [ `LogicOperator` Operador lógico](#logicoperator-operador-lógico)
- [`TripletStructure` Estructura de tripletas para queries SQL](#tripletstructure-estructura-de-tripletas-para-queries-sql)

### Base

#### `RecordValue` Valor de registro
```py
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
```
Este tipo de dato representa los tipos de dato válidos para diversos
argumentos de entrada en métodos del módulo así como en funcionamientos
internos, retornos en JSON y validaciones.
```py
# Tipos de dato individuales
5
2.8
'nombre'
True
# Listas de tipos de dato
[1, 2, 3]
[1.0, 3.5, 20.56]
['name', 'char', 'active']
[False, True, True]
```

#### `RecordData` Datos de registro
Datos que contienen los valores de campo de un registro en la base de datos.
Ejemplo:
```py
{
    'name': 'Onnymm',
    'password': ...,
    'active': True,
}
```

### Filtros

#### `ComparisonOperator` Operador de comparación
```py
ComparisonOperator = Literal[
    '=',
    '!=',
    '>',
    '>=',
    '<',
    '<=',
    '><',
    'in',
    'not in',
    'ilike',
    'not ilike',
    '~',
    '~*',
]
```
Tipo de dato que representa una operador de comparación.

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

#### `LogicOperator` Operador lógico
```py
LogicOperator = Literal['&', '|']
```
Tipo de dato que representa un operador lógico.

Los operadores lógicos disponibles son:
- `'&'`: AND
- `'|'`: OR

#### `TripletStructure` Estructura de tripletas para queries SQL
```py
TripletStructure = tuple[str, ComparisonOperator, RecordValue]
```
Este tipo de dato representa una condición sencilla para usarse en una
transacción en base de datos.

La estructura de una tripleta consiste en 3 diferentes parámetros:
1. Nombre del campo del modelo
2. Operador de comparación
3. Valor de comparación

Algunos ejemplos de tripletas son:
```py
('name', '=', 'Onnymm')
# Nombre es igual a "Onnymm"
('id', '=', 5)
# ID es igual a 5
('amount', '>', 500)
# "amount" es mayor a 500
('name', 'ilike', 'as')
# "name" contiene "as"
```

> Para saber más sobre el tipo de dato `ComparisonOperator` consulta [Operador de comparación](#comparisonoperator-operador-de-comparación).
