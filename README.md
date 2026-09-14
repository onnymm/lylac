# Lylac
Un framework ORM programable para PostgreSQL, diseñado para plataformas empresariales extensibles.

## Instalación
```bash
pip install git+https://github.com/onnymm/lylac.git
```

## Índice

**MÉTODOS**

- **[login — Iniciar sesión](#login-iniciar-sesión)**
- **[create — Creación de registros](#create-creación-de-uno-o-muchos-registros)**
- **[search — Búsqueda de registros](#search-búsqueda-de-registros)**
- **[read — Lectura de registros](#read-lectura-de-registros)**
- **[search_read — Búsqueda y lectura de registros](#search_read-búsqueda-y-lectura-de-registros)**
- **[search_count — Conteo de búsqueda](#search_count-conteo-de-búsqueda)**
- **[update — Actualización de registros](#update-actualización-de-registros)**
- **[delete — Eliminación de registros](#delete-eliminación-de-registros)**
- **[authenticate_user — Autenticación de usuario](#authenticate_user-autenticación-de-usuario)**

**INICIALIZACIÓN**
- **[Variables de entorno](#variables-de-entorno)**
    - **[Credenciales](#credenciales)**
    - **[Usuarios](#usuarios)**
    - **[Parámetros opcionales](#parámetros-opcionales)**
- **[Creación de la base de datos](#creación-de-la-base-de-datos)**

**TIPADOS**
- **[_M — Nombre de modelo personalizado](#_m-nombre-de-modelo-personalizado)**
- **[_T — Parámetro de tipo _T](#_t-parámetro-de-tipo-_t)**
- **[_Aliased — Alias de tipo _T para declaración de campos](#_aliased-alias-de-tipo-_t-para-declaración-de-campos)**
- **[ComputeFieldFn — Función de cómputo de campo](#computefieldfn-función-de-cómputo-de-campo)**
- **[CriteriaStructure — Estructura de criterio de búsqueda](#criteriastructrure-estructura-de-criterio-de-búsqueda)**
- **[FieldComputation — Cómputo de campo](#fieldcomputation-cómputo-de-campo)**
- **[FieldName — Nombre de campo existente en el modelo](#fieldname-nombre-de-campo-existente-en-el-modelo)**
- **[FieldReadDeclaration — Declaración de campos a leer](#fieldreaddeclaration-declaración-de-campos-a-leer)**
- **[ItemOrList — Elemento o lista de elementos](#itemorlist-elemento-o-lista-de-elementos)**
- **[ModelName — Nombre de modelo](#modelname-nombre-de-modelo)**
- **[TTypeName — Nombre de tipo de dato de campo](#ttypename-nombre-de-tipo-de-dato-de-campo)**

----

## Métodos

### `login` Iniciar sesión
Este método permite crear una sesión de usuario y retorna una UUID de sesión para poder autenticarse cuando se use alguno de los métodos de transacción de datos.

Uso:
```py
# Obtención de UUID de sesión de autenticación
session_uuid = db.login('onnymm', 'contraseñasecreta123')
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

----

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

db.create(session_uuid, 'base.users', records)
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

**Retorno**
- `record_ids`: *list[int]* — Lista de IDs de los registros encontrados.

----

### `read` Lectura de registros
Este método retorna una lista de diccionarios con el contenido de los registros de un modelo de la base de datos a partir de una lista de IDs, en el orden en el que se especificaron los campos o todos los campos en caso de no haber sido especificados.

Uso:
```py
# Ejemplo 1
db.read(session_uuid, 'base.users', [2])
# [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]

# Ejemplo 2
db.read(session_uuid, 'base.users', [2, 3])
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
# ]

# Ejemplo 3
db.read(session_uuid, 'base.users', [2, 3], ['login', 'create_date'])
# [
#   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
#   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
# ]
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[int]* — ID o lista de IDs de los registros a leer.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer.
- `sortby` **(Opcional)**: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)]* — Nombre o nombres de campo a usar para ordenar los registros.
- `ascending` **(Opcional)**: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[bool]* — Dirección de ordenamiento, ascendente (*True*) o descendente (*False*). Este y el parámetro `sortby` deben coincidir. Si se especificó 1 campo, 1 dirección de ordenamiento debe ser especificada. Si se especificaron $n$ campos de ordenamiento, $n$ direcciones de ordenamiento deben ser especificadas.

**Retorno**
- `records`: *list[RecordData]* — Lista de diccionarios con los datos de los registros solicitados.

----

### `search_read` Búsqueda y lectura de registros
Este método retorna una lista de diccionarios con el contenido de los registros de un modelo de la base de datos, en el orden en el que se especificaron los campos o todos los campos en caso de no haber sido especificados.

Uso:
```py
# Ejemplo 1
db.search_read(session_uuid, 'base.users')
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   ...
# ]

# Ejemplo 2
db.search_read(session_uuid, 'base.users', [('user', '=', 'onnymm')])
# [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]

# Ejemplo 3
db.search_read(session_uuid, 'base.users', fields= ['user', 'create_date'])
# [
#   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
#   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
#   ...
# ]
```

#### Desfase de registros para paginación
Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que una búsqueda normal arrojaría los siguientes resultados:
```py
db.search_read(session_uuid, 'base.users')
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
#   ...
# ]
```

Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como por ejemplo lo siguiente:
```py
db.search_read(session_uuid, 'base.users', offset= 2)
# [
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
#   {'id': 7, 'name': 'Sarko Zuimx', 'login': 'sarzu', ...},
#   {'id': 8, 'name': 'Leo Minnix', 'login': 'minnleo', ...},
#   ...
# ]
```

#### Límite de registros retornados para paginación
También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
```py
db.search_read(session_uuid, 'base.users')
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
#   ...
# ]
```

Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un número provisto:
```py
db.search_read(session_uuid, 'base.users', limit= 3)
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...}
# ]
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)* — Criterio de búsqueda.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer.
- `offset` **(Opcional)**: *int* — Desfase de resultados retornados.
- `limit` **(Opcional)**: *int* — Límite de cantidad de resultados retornados.
- `sortby` **(Opcional)**: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)]* — Nombre o nombres de campo a usar para ordenar los registros.
- `ascending` **(Opcional)**: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[bool]* — Dirección de ordenamiento, ascendente (*True*) o descendente (*False*). Este y el parámetro `sortby` deben coincidir. Si se especificó 1 campo, 1 dirección de ordenamiento debe ser especificada. Si se especificaron $n$ campos de ordenamiento, $n$ direcciones de ordenamiento deben ser especificadas.

**Retorno**
- `records`: *list[RecordData]* — Lista de diccionarios con los datos de los registros solicitados.

----

### `search_count` Conteo de búsqueda
Este método retorna el conteo de de todos los registros de un modelo o los registros que cumplan con la condición de búsqueda provista, ideal para funcionalidades de paginación que muestran un total de registros.

Uso:
```py
# Ejemplo 1
db.search_count(session_uuid, 'base.users')
# 5

# Ejemplo 2
db.search_count(session_uuid, 'base.permissions', [('create_uid', '=', 5)])
# 126
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)* — Criterio de búsqueda.

**Retorno**
- `count`: *int* — Total de registros encontrados.

----

### `update` Actualización de registros
Este método realiza la actualización de uno o más registros a partir de su respectiva ID provista, actualizando uno o más campos con el valor provisto. Este método solo sobreescribe un mismo valor por cada campo a todos los registros provistos.

Uso:
```py
db.search_read(session_uuid, 'base.users', fields= ['login', 'name'])
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii'},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim'},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio'},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
#   ...
# ]

# Modificación
db.update(session_uuid, 'base.users', [3, 4, 5], {'name': 'Cambiado'})
# True

db.search_read(session_uuid, 'base.users', fields= ['login', 'name'])
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
#   {'id': 3, 'name': 'Cambiado', 'login': 'lumii'},
#   {'id': 4, 'name': 'Cambiado', 'login': 'meshkim'},
#   {'id': 5, 'name': 'Cambiado', 'login': 'luunafio'},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
#   ...
# ]
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[int]* — ID o lista de IDs de los registros a actualizar.
- `data`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[RecordData]* — Diccionario o lista de diccionarios de los datos a crear.

**Retorno**
- `response`: *Literal[True]* — Respuesta de que la operación se realizó correctamente.

----

### `delete` Eliminación de registros
Este método realiza la eliminaciónd e uno o más registros de la base de datos a partir de su respectiva ID provista.

Uso:
```py
db.search_read(session_uuid, 'base.users')
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
#   ...
# ]

# Eliminación del registro con ID 2

db.delete(session_uuid, 'base.users', 2)
# True

db.search_read(session_uuid, 'base.users')
# [
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
#   ...
# ]
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[int]* — ID o lista de IDs de los registros a eliminar.

**Retorno**
- `response`: *Literal[True]* — Respuesta de que la operación se realizó correctamente.

----

### `authenticate_user` Autenticación de usuario
Este método recibe una UUID de sesión y resuelve a qué usuario le pertenece la sesión.

Uso:
```py
session_uuid = '4d9ad73f-40cf-4b33-8feb-4c593c172cf2'

db.authenticate_user(session_uuid)
# 2
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.

**Retorno**
- `user_id`: *int* — ID del usuario propietario de la sesión.

----

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

### `_Aliased` Alias de tipo [_T](#_t-parámetro-de-tipo-_t) para declaración de campos
Representación de una tupla que toma una declaración de campo de tipo [_T](#_t-parámetro-de-tipo-_t) y le da un nombre corto de tipo `str`:

Ejemplo de representación:
```py
_Aliased[FieldName]
# tuple[FieldName, str]

_Aliased[_ArrayExpansion]
# tuple[_ArrayExpansion, str]
```

Ejemplo de uso:
```py
# _Aliased[FieldName]
('create_id.name', 'created_by')

# _Aliased[FieldName]
('record_id.employee_id.complete_name', 'responsible')

# _Aliased[_ArrayExpansion]
(('detail_ids', [...]), 'detailed_operation')
```

### `ComputeFieldFn` Función de cómputo de campo
Estructura que representa una función que recibe un contexto de cómputo y retorna una instancia de campo que se usa para computar una columna en la lectura de registros desde la base de datos.

Estructura:
```py
# Función def
def model_name__computed_field(ctx: Lylac.ComputeContext):
    ...
    return computed_field_instance

# Función lambda
fn = lambda ctx: ...
```

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

### `FieldComputation` Cómputo de campo
Representación para declarar el cómputo de un campo en tiempo real. La estructura está conformada por una tupla de 3 elementos:
1. [FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo) — Nombre de campo existente en el modelo.
2. [TTypeName](#ttypename-nombre-de-tipo-de-dato-de-campo) — Nombre de tipo de dato de campo.
3. [ComputeFieldFn](#computefieldfn-función-de-cómputo-de-campo)[_M](#_m-nombre-de-modelo-personalizado) — Función de cómputo de campo.

Estructura de ejemplo:
```py
computed_total = ('total', 'float', lambda ctx: ctx['qty'] * ctx['price'])

# Uso
db.read(session_uuid, 'sale.order', fields= ['name', computed_total])
```

### `FieldName` Nombre de campo existente en el modelo
Alias del tipo `str`. Representa el nombre de un campo existente en un modelo de la base de datos o una referencia en cadena a través de relaciones de modelos.

Los nombres más comunes son:
- `'id'`
- `'name'`
- `'create_date'`
- `'update_date'`
- `'create_uid'`
- `'update_uid'`
- `'display_name'`

Para obtener los detalles de un registro referenciado en campos de tipo `many2one` se puede usar el acceso `.` seguido del nombre del campo cuyo valor se desea obtener:

```py
'create_uid'
# [2, 'Onnymm Azzur']
# Usuario de creación

'create_uid.name'
# 'Onnymm Azzur'

'create_uid.create_date'
# '2026-09-12 12:15:36'
```

### `FieldReadDeclaration` Declaración de campos a leer
Este tipado representa una lista de cualquiera de los siguientes tipos o representaciones:
- [FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo) — Nombre de campo existente en el modelo.
- [_Aliased](#_aliased-alias-de-tipo-_t-para-declaración-de-campos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)] — Nombre de campo con alias.
- [FieldComputation](#fieldcomputation-cómputo-de-campo)[[_M](#_m-nombre-de-modelo-personalizado)] — Cómputo de campo

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

### `TTypeName` Nombre de tipo de dato de campo
Conjunto de literales que representan los nombres de los tipos de dato disponibles para ser usados desde el framework.

Los nombres disponibles son:
- `'integer'` Entero.
- `'char'` Caracter.
- `'float'` Flotante.
- `'boolean'` Booleano.
- `'date'` Fecha.
- `'datetime'` Fecha y hora.
- `'time'` Hora.
- `'duration'` Duración o intervalo.
- `'file'` Archivo o binario.
- `'text'` Texto largo.
- `'selection'` Selección.
- `'many2one'` Relación muchos a uno hacia un modelo.
- `'one2many'` Relación uno a muchos hacia un modelo.
- `'many2many'` Relación muchos a muchos hacia un modelo.
- `'json'` JSON.
