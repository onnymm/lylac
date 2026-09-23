# Lylac
Un framework ORM programable para PostgreSQL, diseñado para plataformas empresariales extensibles.

## Instalación
```bash
pip install git+https://github.com/onnymm/lylac.git
```

## Índice

**[MÉTODOS](#métodos)**

- **[`login` — Iniciar sesión](#login-iniciar-sesión)**
- **[`create` — Creación de registros](#create-creación-de-uno-o-muchos-registros)**
- **[`search` — Búsqueda de registros](#search-búsqueda-de-registros)**
- **[`read` — Lectura de registros](#read-lectura-de-registros)**
- **[`search_read` — Búsqueda y lectura de registros](#search_read-búsqueda-y-lectura-de-registros)**
- **[`search_count` — Conteo de búsqueda](#search_count-conteo-de-búsqueda)**
- **[`update` — Actualización de registros](#update-actualización-de-registros)**
- **[`delete` — Eliminación de registros](#delete-eliminación-de-registros)**
- **[`action` — Ejecución de una acción](#action-ejecución-de-una-acción)**
- **[`task` — Ejecución de una tarea de servidor](#task-ejecución-de-tarea-de-servidor)**
- **[`execute_transaction` — Ejecutar transacción](#execute_transaction-ejecutar-transacción)**
- **[`authenticate_user` — Autenticación de usuario](#authenticate_user-autenticación-de-usuario)**

**[INICIALIZACIÓN](#inicialización)**

- **[Variables de entorno](#variables-de-entorno)**
    - **[Credenciales](#credenciales)**
    - **[Usuarios](#usuarios)**
    - **[Parámetros opcionales](#parámetros-opcionales)**
- **[Creación de la base de datos](#creación-de-la-base-de-datos)**

**[CONTEXTOS](#contextos)**

- **[`BaseContext` — Contexto base](#basecontext-contexto-base)**
    - **[`uid` — ID del usuario que ejecuta la transacción](#uid-id-del-usuario-que-ejecuta-la-transacción)**
    - **[`create` — Creación de registros](#create-creación-de-uno-o-muchos-registros-1)**
    - **[`search` — Búsqueda de registros](#search-búsqueda-de-registros-1)**
    - **[`read` — Lectura de registros](#read-lectura-de-registros-1)**
    - **[`search_read` — Búsqueda y lectura de registros](#search_read-búsqueda-y-lectura-de-registros-1)**
    - **[`search_count` — Conteo de búsqueda](#search_count-conteo-de-búsqueda-1)**
    - **[`update` — Actualización de registros](#update-actualización-de-registros-1)**
    - **[`delete` — Eliminación de registros](#delete-eliminación-de-registros-1)**
    - **[`get_resource_id` — Obtención de ID de recurso](#get_resource_id-obtención-de-id-de-recurso)**
- **[`ExecutionContext` — Contexto de ejecución](#executioncontext-contexto-de-ejecución)**
    - **[`commit` — Commit en la base de datos](#commit-commit-en-la-base-de-datos)**
- **[`ActionContext` — Contexto de acción](#actioncontext-contexto-de-acción)**
    - **[`data` Datos del registro](#data-datos-del-registro-contexto-de-acción)**
    - **[`record_id` ID de registro](#record_id-id-de-registro-contexto-de-acción)**
- **[`AutomationContext` — Contexto de automatización](#automationcontext-contexto-de-automatización)**
    - **[`records` — Lista de registros](#records-lista-de-registros-contexto-de-automatización)**
- **[`ServerTaskContext` — Contexto de tarea de servidor](#servertaskcontext-contexto-de-tarea-de-servidor)**

**[ACCIONES](#acciones)**

- **[Registro de acciones](#registro-de-acciones)**
- **[Ejecución de acciones](#ejecución-de-acciones)**

**[TAREAS DE SERVIDOR](#tareas-de-servidor)**

- **[Registro de tareas de servidor](#registro-de-tareas-de-servidor)**
- **[Ejecución de tareas de servidor](#ejecución-de-tareas-de-servidor)**

**[AUTOMATIZACIONES](#automatizaciones)**
- **[Registro de automatizaciones](#registro-de-automatizaciones)**
- **[Ejecucución de automatizaciones](#ejecucución-de-automatizaciones)**

**[TIPADOS](#tipados)**
- **[`_M` — Nombre de modelo personalizado](#_m-nombre-de-modelo-personalizado)**
- **[`_T` — Parámetro de tipo _T](#_t-parámetro-de-tipo-_t)**
- **[`_Aliased` — Alias de tipo _T para declaración de campos](#_aliased-alias-de-tipo-_t-para-declaración-de-campos)**
- **[`ComputeFieldFn` — Función de cómputo de campo](#computefieldfn-función-de-cómputo-de-campo)**
- **[`CriteriaStructure` — Estructura de criterio de búsqueda](#criteriastructrure-estructura-de-criterio-de-búsqueda)**
- **[`DMLTransaction` — Transacción DML](#dmltransaction-transacción-dml)**
- **[`FieldComputation` — Cómputo de campo](#fieldcomputation-cómputo-de-campo)**
- **[`FieldName` — Nombre de campo existente en el modelo](#fieldname-nombre-de-campo-existente-en-el-modelo)**
- **[`FieldReadDeclaration` — Declaración de campos a leer](#fieldreaddeclaration-declaración-de-campos-a-leer)**
- **[`ItemOrList` — Elemento o lista de elementos](#itemorlist-elemento-o-lista-de-elementos)**
- **[`MaybeNone` — Posiblemente nulo](#maybenone-posiblemente-nulo)**
- **[`ModelName` — Nombre de modelo](#modelname-nombre-de-modelo)**
- **[`TTypeName` — Nombre de tipo de dato de campo](#ttypename-nombre-de-tipo-de-dato-de-campo)**

----

## Métodos
Lylac pone a disposición métodos convenientes para llevar a cabo transacciones de datos con instrucciones anidadas, filtros extremadamente poderosos, lecturas de datos flexibles ya sea de campos existentes en los modelos de la base de datos o computándolos en tiempo real o en funciones previamente registradas.

----

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

> **Desfase de registros para paginación**
> 
> Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que una búsqueda normal arrojaría los siguientes resultados:
> ```py
> db.search(session_uuid, 'base.users')
> # [1, 2, 3, 4, 5, 6, 7]
> ```
> 
> Se puede especificar que el retorno de los registros considerará solo a partir desde cierto desfase numérico, como por ejemplo lo siguiente:
> ```py
> db.search(session_uuid, 'base.users', offset= 2)
> # [3, 4, 5, 6, 7]
> ```

> **Límite de registros retornados para paginación**
> 
> También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
> ```py
> db.search(session_uuid, 'base.users')
> # [1, 2, 3, 4, 5, 6, 7]
> ```
> 
> Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un número provisto:
> ```py
> db.search(session_uuid, 'base.users', limit= 3)
> # [1, 2, 3]
> ```

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

> **Desfase de registros para paginación**
> 
> Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que una búsqueda normal arrojaría los siguientes resultados:
> ```py
> db.search_read(session_uuid, 'base.users')
> # [
> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
> #   ...
> # ]
> ```
> 
> Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como por ejemplo lo siguiente:
> ```py
> db.search_read(session_uuid, 'base.users', offset= 2)
> # [
> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
> #   {'id': 7, 'name': 'Sarko Zuimx', 'login': 'sarzu', ...},
> #   {'id': 8, 'name': 'Leo Minnix', 'login': 'minnleo', ...},
> #   ...
> # ]
> ```

> **Límite de registros retornados para paginación**
> 
> También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
> ```py
> db.search_read(session_uuid, 'base.users')
> # [
> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
> #   ...
> # ]
> ```
> 
> Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un número provisto:
> ```py
> db.search_read(session_uuid, 'base.users', limit= 3)
> # [
> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...}
> # ]
> ```

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
Este método realiza la eliminación de uno o más registros de la base de datos a partir de su respectiva ID provista.

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

### `action` Ejecución de una acción
Este método ejecuta una acción sobre un registro de un modelo en la base de datos. Para más información véase la sección [Acciones](#acciones).

Ejemplo:
```py
db.action(session_uuid, 'base.users', 'archive', 3)
# True
```

En el fragmento de código ejecutamos una acción que archiva al registro con ID `3` del modelo `base.users`.

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `name`: *str* — Nombre de la acción.
- `record_id`: *int* — ID del registro sobre el que se va a ejecutar la acción.

**Retorno**
- `response`: *Literal[True]* — Respuesta de que la operación se realizó correctamente.

----

### `task` Ejecución de tarea de servidor
Este método ejecuta una tarea de servidor en la base de datos. Para más información véase la sección [Tareas de servidor](#tareas-de-servidor).

Ejemplo:
```py
db.task(session_uuid, 'update_data_from_api')
# True
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `name`: *str* — Nombre de la tarea de servidor.

**Retorno**
- `response`: *Literal[True]* — Respuesta de que la operación se realizó correctamente.

### `execute_transaction` Ejecutar transacción
Este método ejecuta una transacción compleja construida mediante una función que es provista a este método como argumento. La función debe estar preparada para recibir como argumento un [ExecutionContext](#executioncontext-contexto-de-ejecución)[[_M](#_m-nombre-de-modelo-personalizado)] para poder declarar instrucciones de operaciones en la base de datos. Al estar asociadas a una misma transacción, las instrucciones pueden confirmarse o revertirse como una sola unidad. Si ocurre un error durante la ejecución, la transacción puede realizar un rollback, evitando que los cambios realizados hasta ese momento sean persistidos parcialmente en la base de datos.

Uso:
```py
# Definición de función de lectura del perfil del usuario de la sesión
def me(ctx: Lylac.ExecutionContext):

    # Obtención de los datos del usuario de la sesión
    [ user_data ] = ctx.read(
        'base.users',
        ctx.uid,
        fields = [
            'name',
            'active',
            'login',
            'profile_picture',
        ],
    )

    return user_data

# Ejecución de la transacción desde la instancia principal
profile_data = db.execute_transaction(session_uuid, me)
```

**Parámetros**

- `session_uuid`: *str* — UUID de sesión.
- `callback`: *Callable[[[ExecutionContext](#executioncontext-contexto-de-ejecución)[[_M](#_m-nombre-de-modelo-personalizado)]], [_T](#_t-parámetro-de-tipo-_t)]* — Función de transacción.

**Retorno**

- `result`: *[_T](#_t-parámetro-de-tipo-_t)* — El valor u objeto que retorna la función de transacción.

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

## Contextos

Los contextos son objetos que reúnen el estado y los recursos necesarios para ejecutar una operación dentro de un determinado ámbito de ejecución.

En Lylac, un contexto se utiliza durante la ejecución de una función que forma parte de una misma transacción de base de datos. El contexto proporciona a la función acceso a información y recursos relevantes para dicha ejecución, como la ID del usuario que inició la transacción, la conexión de base de datos asociada a ella y otros recursos necesarios para realizar la operación.

Los contextos permiten que varias instrucciones compartan el mismo estado y formen parte de una misma unidad de trabajo. Esto resulta especialmente útil para operaciones que requieren ejecutar múltiples instrucciones de forma conjunta.

Al estar asociadas a una misma transacción, las instrucciones pueden confirmarse o revertirse como una sola unidad. Si ocurre un error durante la ejecución, la transacción puede realizar un rollback, evitando que los cambios realizados hasta ese momento sean persistidos parcialmente en la base de datos.

----

### `BaseContext` Contexto base
La clase de contexto base reúne los métodos y atributos comunes entre los contextos de Acción, Ambiente, Automatización, Tareas de servidor, Políticas y Validación.

#### `uid` ID del usuario que ejecuta la transacción
Este es un atributo de solo lectura. Muestra la ID del usuario que está ejecutando la transacción.

**Retorno**
- `user_uid`: *int* — ID del usuario que ejecuta la transacción.

----

#### `create` Creación de uno o muchos registros
Este método realiza la creación de uno o muchos registros.

Uso:
```py
# Para un solo registro
record = {
    'login': 'onnymm',
    'name': 'Onnymm Azzur',
}

ctx.create('base.users', record)

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

ctx.create('base.users', records)
```

**Parámetros**
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `data`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[RecordData]* — Diccionario o lista de diccionarios de los datos a crear.

**Retorno**
- `record_ids`: *list[int]* — Lista de IDs del registro o de los registros creados.

----

#### `search` Búsqueda de registros
Este método retorna todas las IDs de los registros de un modelo o los registros que cumplan con la condición de búsqueda provista.

Uso:
```py
# Registros existentes en el modelo base.users
ctx.search('base.users')
# [1, 2, 3, 4, 5, 6, 7]

# Registros en el modelo base.users que hayan sido creados
#   por el usuario con la ID 2
ctx.search('base.users', [('create_uid', '=', 2)])
# [3, 5, 6]
```

> **Desfase de registros para paginación**
> 
> Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que una búsqueda normal arrojaría los siguientes resultados:
> ```py
> ctx.search('base.users')
> # [1, 2, 3, 4, 5, 6, 7]
> ```
> 
> Se puede especificar que el retorno de los registros considerará solo a partir desde cierto desfase numérico, como por ejemplo lo siguiente:
> ```py
> ctx.search('base.users', offset= 2)
> # [3, 4, 5, 6, 7]
> ```

> **Límite de registros retornados para paginación**
> 
> También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
> ```py
> ctx.search('base.users')
> # [1, 2, 3, 4, 5, 6, 7]
> ```
> 
> Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un número provisto:
> ```py
> ctx.search('base.users', limit= 3)
> # [1, 2, 3]
> ```

**Parámetros**
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)* — Criterio de búsqueda.
- `offset` **(Opcional)**: *int* — Desfase de resultados retornados.
- `limit` **(Opcional)**: *int* — Límite de cantidad de resultados retornados.

**Retorno**
- `record_ids`: *list[int]* — Lista de IDs de los registros encontrados.

----

#### `read` Lectura de registros
Este método retorna una lista de diccionarios con el contenido de los registros de un modelo de la base de datos a partir de una lista de IDs, en el orden en el que se especificaron los campos o todos los campos en caso de no haber sido especificados.

Uso:
```py
# Ejemplo 1
ctx.read('base.users', [2])
# [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]

# Ejemplo 2
ctx.read('base.users', [2, 3])
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
# ]

# Ejemplo 3
ctx.read('base.users', [2, 3], ['login', 'create_date'])
# [
#   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
#   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
# ]
```

**Parámetros**
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[int]* — ID o lista de IDs de los registros a leer.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer.
- `sortby` **(Opcional)**: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)]* — Nombre o nombres de campo a usar para ordenar los registros.
- `ascending` **(Opcional)**: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[bool]* — Dirección de ordenamiento, ascendente (*True*) o descendente (*False*). Este y el parámetro `sortby` deben coincidir. Si se especificó 1 campo, 1 dirección de ordenamiento debe ser especificada. Si se especificaron $n$ campos de ordenamiento, $n$ direcciones de ordenamiento deben ser especificadas.

**Retorno**
- `records`: *list[RecordData]* — Lista de diccionarios con los datos de los registros solicitados.

----

#### `search_read` Búsqueda y lectura de registros
Este método retorna una lista de diccionarios con el contenido de los registros de un modelo de la base de datos, en el orden en el que se especificaron los campos o todos los campos en caso de no haber sido especificados.

Uso:
```py
# Ejemplo 1
ctx.search_read('base.users')
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   ...
# ]

# Ejemplo 2
ctx.search_read('base.users', [('user', '=', 'onnymm')])
# [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]

# Ejemplo 3
ctx.search_read('base.users', fields= ['user', 'create_date'])
# [
#   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
#   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
#   ...
# ]
```

> **Desfase de registros para paginación**
> 
> Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que una búsqueda normal arrojaría los siguientes resultados:
> ```py
> ctx.search_read('base.users')
> # [
> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
> #   ...
> # ]
> ```
> 
> Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como por ejemplo lo siguiente:
> ```py
> ctx.search_read('base.users', offset= 2)
> # [
> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
> #   {'id': 7, 'name': 'Sarko Zuimx', 'login': 'sarzu', ...},
> #   {'id': 8, 'name': 'Leo Minnix', 'login': 'minnleo', ...},
> #   ...
> # ]
> ```

> **Límite de registros retornados para paginación**
> 
> También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
> ```py
> ctx.search_read('base.users')
> # [
> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
> #   ...
> # ]
> ```
> 
> Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un número provisto:
> ```py
> ctx.search_read('base.users', limit= 3)
> # [
> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...}
> # ]
> ```

**Parámetros**
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

#### `search_count` Conteo de búsqueda
Este método retorna el conteo de de todos los registros de un modelo o los registros que cumplan con la condición de búsqueda provista, ideal para funcionalidades de paginación que muestran un total de registros.

Uso:
```py
# Ejemplo 1
ctx.search_count('base.users')
# 5

# Ejemplo 2
ctx.search_count('base.permissions', [('create_uid', '=', 5)])
# 126
```

**Parámetros**
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)* — Criterio de búsqueda.

**Retorno**
- `count`: *int* — Total de registros encontrados.

----

#### `update` Actualización de registros
Este método realiza la actualización de uno o más registros a partir de su respectiva ID provista, actualizando uno o más campos con el valor provisto. Este método solo sobreescribe un mismo valor por cada campo a todos los registros provistos.

Uso:
```py
ctx.search_read('base.users', fields= ['login', 'name'])
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii'},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim'},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio'},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
#   ...
# ]

# Modificación
ctx.update('base.users', [3, 4, 5], {'name': 'Cambiado'})
# True

ctx.search_read('base.users', fields= ['login', 'name'])
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
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[int]* — ID o lista de IDs de los registros a actualizar.
- `data`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[RecordData]* — Diccionario o lista de diccionarios de los datos a crear.

**Retorno**
- `response`: *Literal[True]* — Respuesta de que la operación se realizó correctamente.

----

#### `delete` Eliminación de registros
Este método realiza la eliminación de uno o más registros de la base de datos a partir de su respectiva ID provista.

Uso:
```py
ctx.search_read('base.users')
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
#   ...
# ]

# Eliminación del registro con ID 2

ctx.delete('base.users', 2)
# True

ctx.search_read('base.users')
# [
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
#   ...
# ]
```

**Parámetros**

- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ItemOrList](#itemorlist-elemento-o-lista-de-elementos)[int]* — ID o lista de IDs de los registros a eliminar.

**Retorno**
- `response`: *Literal[True]* — Respuesta de que la operación se realizó correctamente.

----

#### `get_resource_id` Obtención de ID de recurso
Este método se usa para obtener la ID de un registro en la base de datos señalado por su referencia única de mapeo.

**Parámetros**

- `ref`: *str* Referencia única de mapeo de datos.

**Retorno**

- `record_id`: *[MaybeNone](#maybenone-posiblemente-nulo)[int]* — ID del registro referenciado o `None` si no existe.

----

### `ExecutionContext` Contexto de ejecución
La clase de contexto de ejecución es la usada en todas las transacciones CRUD expuestas en los [métodos](#métodos) de la instancia principal y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listas a continuación:

- **[`uid` — ID del usuario que ejecuta la transacción](#uid-id-del-usuario-que-ejecuta-la-transacción)**
- **[`create` — Creación de registros](#create-creación-de-uno-o-muchos-registros-1)**
- **[`search` — Búsqueda de registros](#search-búsqueda-de-registros-1)**
- **[`read` — Lectura de registros](#read-lectura-de-registros-1)**
- **[`search_read` — Búsqueda y lectura de registros](#search_read-búsqueda-y-lectura-de-registros-1)**
- **[`search_count` — Conteo de búsqueda](#search_count-conteo-de-búsqueda-1)**
- **[`update` — Actualización de registros](#update-actualización-de-registros-1)**
- **[`delete` — Eliminación de registros](#delete-eliminación-de-registros-1)**
- **[`get_resource_id` — Obtención de ID de recurso](#get_resource_id-obtención-de-id-de-recurso)**

Además de ello, cuenta también con los métodos listados.

----

#### `commit` Commit en la base de datos
Este método realiza un commit en la base de datos usando el método `commit` de la clase `Connection` de SQLAlchemy.

**Parámetros**

*No se requieren parámetros de entrada.*

**Retorno**

*Este método no retorna ningún valor.*

----

### `ActionContext` Contexto de acción
La clase de contexto de acción es usada como argumento en las funciones de acción y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listas a continuación:

- **[`uid` — ID del usuario que ejecuta la transacción](#uid-id-del-usuario-que-ejecuta-la-transacción)**
- **[`create` — Creación de registros](#create-creación-de-uno-o-muchos-registros-1)**
- **[`search` — Búsqueda de registros](#search-búsqueda-de-registros-1)**
- **[`read` — Lectura de registros](#read-lectura-de-registros-1)**
- **[`search_read` — Búsqueda y lectura de registros](#search_read-búsqueda-y-lectura-de-registros-1)**
- **[`search_count` — Conteo de búsqueda](#search_count-conteo-de-búsqueda-1)**
- **[`update` — Actualización de registros](#update-actualización-de-registros-1)**
- **[`delete` — Eliminación de registros](#delete-eliminación-de-registros-1)**
- **[`get_resource_id` — Obtención de ID de recurso](#get_resource_id-obtención-de-id-de-recurso)**

Además de ello, cuenta también con los métodos listados.

----

#### `data` Datos del registro (Contexto de acción)
Atributo por el cual se puede acceder a los datos del registro sobre el que se ejecuta una acción. Estos datos están definidos por el parámetro `fields` al registrar la acción. Para mayor información, véase [Registro de acciones](#registro-de-acciones).

**Retorno**
- `data`: *[_R](#_r-parámetro-de-estructura-de-registro-dinámico)* — Datos del registro.

----

#### `record_id` ID de registro (Contexto de acción)
Atributo por el cual se puede acceder a la ID del registro sobre el que se ejecuta una acción.

**Retorno**
- `record_id`: *int* — ID del registro sobre el que se ejecuta una acción.

----

### `AutomationContext` Contexto de automatización
La clase de contexto de automatización es usada como argumento en las funciones de automatización y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listas a continuación:

- **[`uid` — ID del usuario que ejecuta la transacción](#uid-id-del-usuario-que-ejecuta-la-transacción)**
- **[`create` — Creación de registros](#create-creación-de-uno-o-muchos-registros-1)**
- **[`search` — Búsqueda de registros](#search-búsqueda-de-registros-1)**
- **[`read` — Lectura de registros](#read-lectura-de-registros-1)**
- **[`search_read` — Búsqueda y lectura de registros](#search_read-búsqueda-y-lectura-de-registros-1)**
- **[`search_count` — Conteo de búsqueda](#search_count-conteo-de-búsqueda-1)**
- **[`update` — Actualización de registros](#update-actualización-de-registros-1)**
- **[`delete` — Eliminación de registros](#delete-eliminación-de-registros-1)**
- **[`get_resource_id` — Obtención de ID de recurso](#get_resource_id-obtención-de-id-de-recurso)**

Además de ello, cuenta también con los métodos listados.

----

#### `records` Lista de registros (Contexto de automatización)
Lista de registros de tipo [_R](#_r-parámetro-de-estructura-de-registro-dinámico) sobre los que se ejecuta una automatización

**Retorno**
- `records`: *list[[_R](#_r-parámetro-de-estructura-de-registro-dinámico)]* Lista de registros sobre los que se ejecuta la automatización.

----

### `ServerTaskContext` Contexto de tarea de servidor
La clase de contexto de tarea de servidor es usada como argumento en las funciones de tarea de servidor y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listas a continuación:

- **[`uid` — ID del usuario que ejecuta la transacción](#uid-id-del-usuario-que-ejecuta-la-transacción)**
- **[`create` — Creación de registros](#create-creación-de-uno-o-muchos-registros-1)**
- **[`search` — Búsqueda de registros](#search-búsqueda-de-registros-1)**
- **[`read` — Lectura de registros](#read-lectura-de-registros-1)**
- **[`search_read` — Búsqueda y lectura de registros](#search_read-búsqueda-y-lectura-de-registros-1)**
- **[`search_count` — Conteo de búsqueda](#search_count-conteo-de-búsqueda-1)**
- **[`update` — Actualización de registros](#update-actualización-de-registros-1)**
- **[`delete` — Eliminación de registros](#delete-eliminación-de-registros-1)**
- **[`get_resource_id` — Obtención de ID de recurso](#get_resource_id-obtención-de-id-de-recurso)**

----

## Acciones
Una acción es una operación ejecutable asociada a un modelo que permite realizar una serie de operaciones a partir de un registro de dicho modelo.

Las acciones son implementadas mediante funciones que reciben un [contexto de acción](#actioncontext-contexto-de-acción) que contiene la ID del registro sobre el que deben operar así como campos declarados por en el [registro](#registro-de-acciones) de la acción para poder leerse y consumirse. A partir de este registro, una acción puede consultar o modificar sus valores, crear registros relacionados, modificar otros registros y ejecutar otras acciones.

Una acción puede estar compuesta por múltiples operaciones. Todas estas operaciones forman parte de la misma ejecución y, cuando corresponda, de la misma transacción, por lo que un error durante su ejecución puede provocar que los cambios realizados sean revertidos conjuntamente.

Por ejemplo, una acción de confirmación podría validar el estado de un registro, modificar sus valores, crear un registro relacionado y ejecutar posteriormente otra acción. Para el sistema, todas estas operaciones forman parte de una única acción.

----

### Registro de acciones
Una acción es básicamente una función en Python pero que cumple con una estructura especial para ser ejecutada por Lylac directamente cuando se invoca ésta por su nombre.

La convención de nomenclatura de las acciones sigue la siguiente estructura:

`_action` + `__` + *nombre del modelo* + `__` + *nombre de la acción*

Los dobles `__` sirven para delimitar cada parte del nombre de la función y asegurar que no existan colisiones en nombres cuando comienzan a haber muchas acciones parecidas en modelos parecidos.

Por ejemplo, si quisiéramos construir una acción para el modelo `base.users` para archivar un usuario nombrando nuestra acción como `archive` la nomenclatura dice que la función se llamaría:

`_action` + `__` + `base_users` + `__` + `archive`

`_action__base_users__archive`

En este caso, los `.` en el nombre del modelo se reemplazan por `_` para ser caracteres válidos en el nombre de una función.

Para tipar el argumento `ctx` se puede usar el tipado `.ActionContext` integrado en Lylac que nos ahorra el tener que importar tipados desde algún submódulo especial.

Ejemplo de la construcción de la acción:
```py
def _action__base_users__archive(ctx: Lylac.ActionContext):

    # Obtención de la ID del registro
    record_id = ctx.record_id

    # Actualización del valor de usuario activo
    ctx.update('base.users', record_id, {'active': True})
```

El commit en la base de datos se hará automáticamente al finalizar todas las operaciones de la transacción.

Una vez creada nuestra función de acción, falta decorarla con la API integrada accesible desde la instancia creada:
```py
@db.api.actions.register(
    'base.users',
    'archive',
)
def _action__base_users__archive(ctx: Lylac.ActionContext):

    # Obtención de la ID del registro
    record_id = ctx.record_id

    # Actualización del valor de usuario activo
    ctx.update('base.users', record_id, {'active': True})
```

**Parámetros del decorador**

- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `name`: *str* — Nombre de la acción.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer antes de la ejecución de la acción, accesibles por el atributo `data`. Si el parámetro no se especifica, solo el valor `'id'` estará disponible.

**Parámetros de la función decorada**

- `ctx`: *[ActionContext](#actioncontext-contexto-de-acción)[[_R](#_r-parámetro-de-estructura-de-registro-dinámico)]* Contexto de acción.

> ℹ️ Las funciones de acción no deben retornar ningún valor u objeto ya que éste no será retornado en la ejecución de éstas. Si se desea retornar un valor u objeto véase [Ejecutar transacción](#execute_transaction-ejecutar-transacción).

----

### Ejecución de acciones
Las acciones se ejecutan sobre un registro especificado, en un modelo especificado.

Ejemplo:
```py
db.action(session_uuid, 'base.users', 'archive', 3)
# True
```

En el fragmento de código ejecutamos una acción que archiva al registro con ID `3` del modelo `base.users`.

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `name`: *str* — Nombre de la acción.
- `record_id`: *int* — ID del registro sobre el que se va a ejecutar la acción.

**Retorno**
- `response`: *Literal[True]* — Respuesta de que la operación se realizó correctamente.

----

## Automatizaciones
Una automatización es una regla asociada a un modelo que permite ejecutar una operación automáticamente cuando ocurre un evento determinado.

Una automatización define las circunstancias bajo las cuales debe ejecutarse y la operación que debe realizarse cuando dichas circunstancias se cumplen. La operación puede consistir en modificar el registro que originó el evento, crear o modificar otros registros, ejecutar una acción o realizar cualquier otra operación permitida por el framework.

Las automatizaciones permiten asociar comportamiento a determinados eventos sin que el código que origina dicho evento tenga que invocar explícitamente la operación correspondiente.

Las automatizaciones pueden ejecutarse tras un evento de creación, modificación o eliminación de registros, en un modelo especificado.

----

### Registro de automatizaciones

Una automatización es básicamente una función en Python pero que cumple con una estructura especial para ser ejecutada por Lylac directamente cuando se desencadena ésta tras una operación CRUD en un modelo en específico.

La convención de nomenclatura de las automatizaciones sigue la siguiente estructura:

`_automation` + `__` + *nombre del modelo* + `__` + *tipo de transacción CRUD* + `__` + *nombre de la automatización*

Los dobles `__` sirven para delimitar cada parte del nombre de la función y asegurar que no existan colisiones en nombres cuando comienzan a haber muchas automatizaciones parecidas en modelos parecidos.

Por ejemplo, si quisiéramos construir una automatización para el modelo `base.users` para añadirle permisos prestablecidos a un usuario cuando éste se crea, nombraríamos nuestra función a algo como `add_preset_permissions` la nomenclatura dice que la función se llamaría:

`_automation` + `__` + `base_users` + `__` + `create` + `__` + `add_preset_permissions`

`_automation__base_users__create__add_preset_permissions`

En este caso, los `.` en el nombre del modelo se reemplazan por `_` para ser caracteres válidos en el nombre de una función.

Para tipar el argumento `ctx` se puede usar el tipado `.AutomationContext` integrado en Lylac que nos ahorra el tener que importar tipados desde algún submódulo especial.

Ejemplo de la construcción de la automatización:
```py
def _automation__base_users__create__add_preset_permissions(ctx: Lylac.AutomationContext):
    # Iteración por cada registro de usuario creado
    for user_record in ctx.records
        # Obtención de la ID del usuario
        user_id = user_record['id']
        # Actualización del registro
        ctx.update('base.users', user_id, {'role_ids': {'add': [basic_role_1_id, basic_role_2_id, ...]}})
```

El commit en la base de datos se hará automáticamente al finalizar todas las operaciones de la transacción.

Una vez creada nuestra función de automatización, falta decorarla con la API integrada accesible desde la instancia creada:
```py
@db.api.automations.register(
    'create',
    'base.users'
)
def _automation__base_users__create__add_preset_permissions(ctx: Lylac.AutomationContext):
    # Iteración por cada registro de usuario creado
    for user_record in ctx.records
        # Obtención de la ID del usuario
        user_id = user_record['id']
        # Actualización del registro
        ctx.update('base.users', user_id, {'role_ids': {'add': [basic_role_1_id, basic_role_2_id, ...]}})
```

**Parámetros del decorador**
- `on`: *[DMLTransaction](#dmltransaction-transacción-dml)* — Transacción tras la que se ejecutará la automatización.
- `model_name`: *[ModelName](#modelname_m-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer antes de la ejecución de la acción, accesibles por el atributo `data`. Si el parámetro no se especifica, solo el valor `'id'` estará disponible.
- `execute_only_when` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)* — Criterio requerido para que la automatización se ejecute sobre el registro.

**Parámetros de la función decorada**

- `ctx`: *[AutomationContext](#automationcontext-contexto-de-automatización)[[_R](#_r-parámetro-de-estructura-de-registro-dinámico)]* — Contexto de automatización.

> ℹ️ Las funciones de automatización no deben retornar ningún valor u objeto ya que éste no será retornado en la ejecución de éstas. Si se desea retornar un valor u objéto véase [Ejecutar transacción](#execute_transaction-ejecutar-transacción).

----

### Ejecucución de automatizaciones
Las automatizaciones no pueden ejecutarse de forma manual. Éstas se ejecutan tras una operación de creación, modificación o eliminación de registros en un modelo especificado y, opcionalmente, si los registros involucrados cumplen con el criterio establecido para la automatización.

----

## Tareas de servidor
Una tarea de servidor es una operación que permite ejecutar una serie de procesos con alcance a uno o muchos modelos de la base de datos, tal como lo haría una función común en Python pero sin retornar un valor en concreto.

Las tareas de servidor son útiles para realizar actualizaciones, sincronizaciones periódicas o funciones complejas que involucran muchos registros en uno o varios modelos. Son implementadas mediante funciones que reciben un contexto de tarea de servidor y no deben retornar un valor.

Una tarea de servidor puede estar compuesta por múltiples operaciones. Todas estas operaciones forman parte de la misma ejecución y, cuando corresponda, de la misma transacción, por lo que un error durante su ejecución puede provocar que los cambios realizados sean revertidos conjuntamente.

Por ejemplo, una tarea de servidor podría actualizar un estado o una serie de registros conectándose a una API externa o realizar un reporte a partir una serie de registros al finalizar el día.

### Registro de tareas de servidor
Una tarea de servidor es básicamente una función en Python pero que cumple con una estructura especial para ser ejecutada por Lylac directamente cuando se invoca ésta por su nombre.

La convención de nomenclatura de las tareas de servidor sigue la siguiente estructura:

`_task` + `__` + *nombre de la tarea de servidor*

Los dobles `__` sirven para delimitar cada parte del nombre de la función y asegurar que no existan colisiones en nombres cuando comienzan a haber muchas tareas de servidor parecidas en modelos parecidos.

Por ejemplo, si quisiéramos construir una tarea de servidor que se conecta a la API de un tercero para actualizar un estado, una serie de registros o algo por el estilo, la nomenclatura dice que la función se llamaría:

`_task` + `__` + `update_data_from_api`

`_task__update_data_from_api`

Para tipar el argumento `ctx` se puede usar el tipado `.ServerTaskContext` integrado en Lylac que nos ahorra el tener que importar tipados desde algún submódulo especial.

Ejemplo de la construcción de la tarea de servidor:
```py
def _task__update_data_from_api(ctx: Lylac.ServerTaskContext):

    # Obtención de datos externos
    data = some_service.fetch_data(...)

    # Procesamiento interno
    formatted_data = process_data(data)

    # Se guardan los datos en la API
    ctx.create('service.registry', formatted_data)
```

El commit en la base de datos se hará automáticamente al finalizar todas las operaciones de la transacción.

Una vez creada nuestra función de tarea de servidor, falta decorarla la API integrada accesible desde la instancia creada:
```py
@db.api.server_tasks.register('update_data_from_api')
def _task__update_data_from_api(ctx: Lylac.ServerTaskContext):

    # Obtención de datos externos
    data = some_service.fetch_data(...)

    # Procesamiento interno
    formatted_data = process_data(data)

    # Se guardan los datos en la API
    ctx.create('service.registry', formatted_data)
```

**Parámetros del decorador**

- `name`: *str* — Nombre de la tarea de servidor.

> ℹ️ Las funciones de tarea de servidor no deben retornar ningún valor u objeto ya que éste no será retornado en la ejecución de éstas. Si se desea retornar un valor u objeto véase [Ejecutar transacción](#execute_transaction-ejecutar-transacción).

### Ejecución de tareas de servidor
Las tareas de servidor se ejecutan invocándolas con el nombre con el que fueron registradas. Para más información, véase [Registro de tareas de servidor](#registro-de-tareas-de-servidor)

Ejemplo:
```py
db.task(session_uuid, 'update_data_from_api')
# True
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `name`: *str* — Nombre de la tarea de servidor.

**Retorno**
- `response`: *Literal[True]* — Respuesta de que la operación se realizó correctamente.

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

### `_R` Parámetro de estructura de registro dinámico
Este parámetro es usado para definir la estructura de un registro dentro de un diccionario tipado.

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

### `DMLTransaction` Transacción DML
Alias usado para describir el literal de nombres de transacciones CRUD que excluye lectura. Los valores disponibles son:
- `'create'`: Creación de registros.
- `'update'`: Modificación de registros.
- `'delete'`: Eliminación de registros.

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

### `MaybeNone` Posiblemente nulo
Este tipado es un alias equivalente al tipo `Optional` de la biblioteca estándar `typing`, utilizado para indicar que un valor puede ser del tipo especificado o None. Su nombre está orientado a tipar valores principalmente de retorno que pueden ser de un tipo especificado o `None`.

```py
MaybeNone[int] # Equivalente a Optional[int]
MaybeNone[str] # Equivalente a Optional[str]
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
