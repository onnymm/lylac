## *Índice*

**MÉTODOS**

- **[login — Iniciar sesión](#login-iniciar-sesión)**
- **[create — Creación de registros](#create-creación-de-uno-o-muchos-registros)**
- **[search — Búsqueda de registros](#search-búsqueda-de-registros)**

**INICIALIZACIÓN**
- **[Variables de entorno](#variables-de-entorno)**
    - **[Credenciales](#credenciales)**
    - **[Usuarios](#usuarios)**
    - **[Parámetros opcionales](#parámetros-opcionales)**
- **[Creación de la base de datos](#creación-de-la-base-de-datos)**

**TIPADOS**
- **[_M — Nombre de modelo personalizado](#_m-nombre-de-modelo-personalizado)**
- **[_T — Parámetro de tipo _T](#_t-parámetro-de-tipo-_t)**
- **[CriteriaStructure — Estructura de criterio de búsqueda](#criteriastructrure-estructura-de-criterio-de-búsqueda)**
- **[ItemOrList — Elemento o lista de elementos](#itemorlist-elemento-o-lista-de-elementos)**
- **[ModelName — Nombre de modelo](#modelname-nombre-de-modelo)**

----

## Métodos

### `login` Iniciar sesión
Este método permite crear una sesión de usuario y retorna un token para poder autenticarse cuando se use alguno de los métodos de transacción de datos.

Uso:
```py
# Obtención de token de autenticación
token = db.login('onnymm', 'contraseñasecreta123')
```

**Parámetros**
- `username`: *str* — Nombre de usuario.
- `password`: *str* — Contraseña del usuario.

**Retorno**
- `session_uuid`: *str* — UUID de sesión para autenticación del usuario.

> **Errores comunes**
> - `UserNotFoundError`: El usuario no fue encontrado.
> - `UserNotActiveError`: El usuario fue encontrado pero éste no está activo.
> - `IncorrectPasswordError`: El usuario fue encontrado y está activo pero la contraseña no coincide con la almacenada en la base de datos.

> ℹ️ Es decisión del desarrollador proveer o no la información sobre la falla encontrada en el inicio de sesión, por ejemplo, si desea decirle al usuario que su cuenta no existe o solo hacerle saber que "El usuario o la contraseña no son correctos".

### `create` Creación de uno o muchos registros
Este método realiza la creación de uno o muchos registros.

Uso:
```py
# Para un solo registro
record = {
    'login': 'onnymm',
    'name': 'Onnymm Azzur',
}

db.create(session_uuid, 'base.users', record)

# Para muchos registros
records = [
    {
        'login': 'onnymm',
        'name': 'Onnymm Azzur',
    },
    {
        'login': 'lumii',
        'name': 'Lumii Mynx',
    },
]

db.create(token, 'base.users', records)
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `data`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[RecordData]* — Diccionario o lista de diccionarios de los datos a crear.

**Retorno**
- `record_ids`: *list[int]* — Lista de IDs del registro o de los registros creados.

----

### `search` Búsqueda de registros
Este método retorna todas las IDs de los registros de un modelo o los registros que cumplan con la condición de búsqueda provista.

Uso:
```py
# Registros existentes en el modelo base.users
db.search(session_uuid, 'base.users')
# [1, 2, 3, 4, 5, 6, 7]

# Registros en el modelo base.users que hayan sido creados
#   por el usuario con la ID 2
db.search(session_uuid, 'base.users', [('create_uid', '=', 2)])
# [3, 5, 6]
```

#### Desfase de registros para paginación
Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que una búsqueda normal arrojaría los siguientes resultados:
```py
db.search(session_uuid, 'base.users')
# [1, 2, 3, 4, 5, 6, 7]
```

Se puede especificar que el retorno de los registros considerará solo a partir desde cierto desfase numérico, como por ejemplo lo siguiente:
```py
db.search(session_uuid, 'base.users', offset= 2)
# [3, 4, 5, 6, 7]
```

#### Límite de registros retornados para paginación
También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
```py
db.search(session_uuid, 'base.users')
# [1, 2, 3, 4, 5, 6, 7]
```

Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un número provisto:
```py
db.search(session_uuid, 'base.users', limit= 3)
# [1, 2, 3]
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)* — Criterio de búsqueda.
- `offset` **(Opcional)**: *int* — Desfase de resultados retornados.
- `limit` **(Opcional)**: *int* — Límite de cantidad de resultados retornados.

## Inicialización

### Variables de entorno
Para inicializar la estructura inicial de una base de datos se requieren configurar las siguientes variables de entorno:

#### Credenciales
Las siguientes variables pertenecen a las credenciales necesarias para conectarse a la base de datos.

| Variable         | Descripción                          |
|------------------|--------------------------------------|
| `LYLAC_HOST`     | URL donde se aloja la base de datos. |
| `LYLAC_PORT`     | Puerto.                              |
| `LYLAC_NAME`     | Nombre de la base de datos.          |
| `LYLAC_USER`     | Nombre de usuario administrador.     |
| `LYLAC_PASSWORD` | Contraseña de acceso.                |

Ejemplo:
```
LYLAC_HOST = https://wwww.mydatabasehost.com
LYLAC_PORT = 5432
LYLAC_NAME = production
LYLAC_USER = admin
LYLAC_PASSWORD = mypassword123
```

#### Usuarios
Se requiere configurar dos usuarios iniciales a la base de datos. Un usuario raíz que se usará como autor de la creación de los registros de la estructura base de la base de datos y un usuario administrador. Puede ser tu usuario.

| Variable                 | Descripción                                    |
|--------------------------|------------------------------------------------|
| `LYLAC_ROOT_USER_NAME`   | Nombre del usuario raíz.                       |
| `LYLAC_ROOT_USER_LOGIN`  | Nombre de usuario de acceso del usuario raíz.  |
| `LYLAC_ADMIN_USER_NAME`  | Nombre del usuario administrador.              |
| `LYLAC_ADMIN_USER_LOGIN` | Nombre de usuario de acceso del administrador. |

Ejemplo:
```
LYLAC_ROOT_USER_NAME = Root
LYLAC_ROOT_USER_LOGIN = lylac_root
LYLAC_ADMIN_USER_NAME = "Onnymm Azzur"
LYLAC_ADMIN_USER_LOGIN = onnymm
```

> ℹ️ El usuario raíz aparecerá archivado una vez que se inicialice la base de datos.

#### Parámetros opcionales
También se pueden configurar algunos parámetros opcionales para personalizar más el flujo de trabajo del framework.

| Variable                 | Descripción                                                                  |
|--------------------------|------------------------------------------------------------------------------|
| `LYLAC_DEFAULT_PASSWORD` | Contraseña predeterminada que se le asigna a un usuario cuando se crea éste. |

### Creación de la base de datos
Se puede comenzar con un archivo muy pequeño como el siguiente.

```py
from lylac import Lylac

db = Lylac()
```

Al ejecutar el archivo por primera vez, se imprimirá la siguiente leyenda en consola:

```cmd
La base de datos de inicializó correctamente.
```

## Tipados

### `_M` Nombre de modelo personalizado
Genérico usado para extender los nombres de modelo a nombres de modelo personalizados originalmente representados por el tipo [ModelName](#modelname_m-nombre-de-modelo).

Para poder hacer uso de esta extensión se requiere el uso del tipo `Literal` proveniente de la biblioteca nativa `typing`.

Ejemplo:
```py
from lylac import Lylac
from typing import Literal

# Nombres de modelo personalizados
Models = Literal[
    'post.post',
    'post.comment',
    'post.reaction',
]

# Creación de una clase personalizada
CustomLylac = Lylac[Models]

db = CustomLylac()
```

### `_T` Parámetro de tipo _T
Parámetro usado para tipados.

### `CriteriaStructrure` Estructura de criterio de búsqueda
La estructura del criterio de búsqueda consiste en una lista de dos tipos de dato:
- `TripletStructure`: Estructura de tripletas para queries SQL
- `LogicOperator`: Operador lógico

Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben unir por operadores lógicos `AND` u `OR`. Siendo el operador lógico el que toma la primera posición:
```py
['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
# "amount" es mayor a 500 y "name" contiene "as"
['|', ('id', '=', 5), ('state', '=', 'posted')]
# "id" es igual a 5 o "state" es igual a "posted"
```

> **Estructura de tripletas para queries SQL**
> 
> Este tipo de dato representa una condición sencilla para usarse en una
> transacción en base de datos. La estructura de una tripleta consiste en 3 diferentes parámetros:
> 1. Nombre del campo del modelo
> 2. Operador de comparación
> 3. Valor de comparación
> 
> Algunos ejemplos de tripletas son:
> ```py
> ('name', '=', 'Onnymm')
> # Nombre es igual a "Onnymm"
> ('id', '=', 5)
> # ID es igual a 5
> ('amount', '>', 500)
> # "amount" es mayor a 500
> ('name', 'ilike', 'as')
> # "name" contiene "as"
> ```
> 
> **Operador lógico**
> 
> Tipo de dato que representa un operador lógico.
> 
> Los operadores lógicos disponibles son:
> - `'&'`: AND
> - `'|'`: OR
> 
> **Operador de comparación**
> 
> Tipo de dato que representa una operador de comparación.
> 
> Los operadores de comparación disponibles son:
> - `'='`: Igual a
> - `'!='`: Diferente de
> - `'>'`: Mayor a
> - `'>='`: Mayor o igual a
> - `'<'`: Menor que
> - `'<='`: Menor o igual que
> - `'in'`: Está en
> - `'not in'`: No está en
> - `'ilike'`: Contiene
> - `'not ilike'`: No contiene
> - `'~'`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
> - `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)



### `ItemOrList` Elemento o lista de elementos
Genérico que representa la unión de un escalar y una lista de tipos [_T](#_t-parámetro-de-tipo-_t).

Ejemplo:
```py
# Una función f que recibe un entero o una lista de enteros
def f(x: int | list[int]):
    ...

# ItemOrList usado como abstracción del mismo tipo
def f(x: ItemOrList[int]):
    ...
```

### `ModelName` Nombre de modelo
Nombre de modelo de la base de datos. Un modelo representa una tabla en la base de datos. Este tipo se une con un genérico [_M](#_m-nombre-de-modelo-personalizado).

Los modelos iniciales son:
- `'base.model'`
- `'base.model.data'`
- `'base.model.data.process'`
- `'base.model.data.process.step'`
- `'base.model.data.process.step.record'`
- `'base.model.field'`
- `'base.model.field.selection'`
- `'base.rules'`
- `'base.users'`
- `'base.users.role'`
- `'base.users.update.password'`
- `'base.users.access'`
- `'base.users.group'`
- `'base.users.session'`
