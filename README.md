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
- **[`ValueResolutionContext` — Contexto de resolución de valor](#valueresolutioncontext-contexto-de-resolución-de-valor)**
    - **[`record_data` — Datos de registro](#record_data-datos-de-registro-contexto-de-resolución-de-valor)**

**[ACCIONES](#acciones)**

- **[Registro de acciones](#registro-de-acciones)**
- **[Ejecución de acciones](#ejecución-de-acciones)**

**[TAREAS DE SERVIDOR](#tareas-de-servidor)**

- **[Registro de tareas de servidor](#registro-de-tareas-de-servidor)**
- **[Ejecución de tareas de servidor](#ejecución-de-tareas-de-servidor)**

**[AUTOMATIZACIONES](#automatizaciones)**
- **[Registro de automatizaciones](#registro-de-automatizaciones)**
- **[Ejecucución de automatizaciones](#ejecucución-de-automatizaciones)**

**[COMANDOS DE RELACIÓN](#comandos-de-relación)**
- **[`RelationCommand.Create` — Comando de relación de creación](#relationcommandcreate-comando-de-relación-de-creación)**
- **[`RelationCommand.Add` — Comando de relación de adición](#relationcommandadd-comando-de-relación-de-adición)**
- **[`RelationCommand.Update` — Comando de relación de actualización](#relationcommandupdate-comando-de-relación-de-actualización)**
- **[`RelationCommand.Replace` — Comando de relación de reemplazo](#relationcommandreplace-comando-de-relación-de-reemplazo)**
- **[`RelationCommand.Unlink` — Comando de relación de desvinculación](#relationcommandunlink-comando-de-relación-de-desvinculación)**
- **[`RelationCommand.Delete` — Comando de relación de eliminación](#relationcommanddelete-comando-de-relación-de-eliminación)**
- **[`RelationCommand.Clear` — Comando de relación de limpieza](#relationcommandclear-comando-de-relación-de-limpieza)**

**[TIPADOS](#tipados)**
- **[`_M` — Nombre de modelo personalizado](#_m-nombre-de-modelo-personalizado)**
- **[`_T` — Parámetro de tipo _T](#_t-parámetro-de-tipo-_t)**
- **[`_Aliased` — Alias de tipo _T para declaración de campos](#_aliased-alias-de-tipo-_t-para-declaración-de-campos)**
- **[`ComputeFieldFn` — Función de cómputo de campo](#computefieldfn-función-de-cómputo-de-campo)**
- **[`CriteriaStructure` — Estructura de criterio de búsqueda](#criteriastructrure-estructura-de-criterio-de-búsqueda)**
- **[`DMLScalarCompatible` — Escalar compatible con PostgreSQL](#dmlscalarcompatible-escalar-compatible-con-postgresql)**
- **[`DMLTransaction` — Transacción DML](#dmltransaction-transacción-dml)**
- **[`FieldComputation` — Cómputo de campo](#fieldcomputation-cómputo-de-campo)**
- **[`FieldName` — Nombre de campo existente en el modelo](#fieldname-nombre-de-campo-existente-en-el-modelo)**
- **[`FieldReadDeclaration` — Declaración de campos a leer](#fieldreaddeclaration-declaración-de-campos-a-leer)**
- **[`InputRecordData` — Datos de registro](#inputrecorddata-datos-de-registro)**
- **[`JSONLikeObjShape` — Diccionario serializable](#jsonlikeobjshape-diccionario-serializable)**
- **[`JSONLikeScalar` — Escalar serializable](#jsonlikescalar-escalar-serializable)**
- **[`JSONLike` — Estructura equivalente a JSON](#jsonlike-estructura-equivalente-a-json)**
- **[`MaybeNone` — Posiblemente nulo](#maybenone-posiblemente-nulo)**
- **[`ModelName` — Nombre de modelo](#modelname-nombre-de-modelo)**
- **[`ScalarOrIterable` — Elemento o iterable de elementos](#scalaroriterable-elemento-o-iterable-de-elementos)**
- **[`TTypeName` — Nombre de tipo de dato de campo](#ttypename-nombre-de-tipo-de-dato-de-campo)**
- **[`ValueResolutionFn` — Función de resolución de valor](#valueresolutionfn-función-de-resolución-de-valor)**

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

Pueden crearse registros referenciados a través de la declaración del valor del campo usando un [comando de relación](#comandos-de-relación):
```py
db.create(
    'base.users',
    {
        'login': 'onnymm',
        'name': 'Onnymm Azzur',
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de creación
            'create': {
                # Datos de registro de un rol en el modelo [base.users.role]
                'name': 'super_admin_role',
                'label': 'Rol de superadministrador',
                ...
            }
        }
    }
)
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `data`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[InputRecordData](#inputrecorddata-datos-de-registro)]* — Diccionario o iterable de diccionarios de datos de los registros a crear:
    1. Las llaves deben ser de tipo *[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)* — Nombre de campo existente en el modelo.
    2. Los valores pueden ser cualquiera de los siguientes tipos de entrada:
        - *[DMLScalarCompatible](#dmlscalarcompatible-escalar-compatible-con-postgresql)* — Tipo de dato que se puede usar como valor para un campo de modelo. El tipo de dato puede ser:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `datetime.date`
            - `datetime.datetime`
            - `datetime.time`
            - `datetime.timedelta`
            - `None`
        - *[JSONLike](#jsonlike-estructura-equivalente-a-json)* — Estructura equivalente a JSON. El tipo de dato puede ser escalar o iterable de:
            - [JSONLikeScalar](#jsonlikescalar-escalar-serializable) que representa los tipos:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `None`
            - [JSONLikeObjShape](#jsonlikeobjshape-diccionario-serializable) que representa un diccionario serializable conformado
            por:
                - Llaves que deben ser de tipo `str`
                - Valores que pueden ser escalar o iterable de:
                    - [JSONLikeScalar](#jsonlikescalar-escalar-serializable)
                    - [JSONLike](#jsonlike-estructura-equivalente-a-json)
        - *[InputRecordData](#inputrecorddata-datos-de-registro)* — Datos para crear un registro vinculado, en campos de tipo `many2one`.
        - *[RelationCommands](#comandos-de-relación)[[_M](#_m-nombre-de-modelo-personalizado)]* — Comandos de modificación de los registros referenciados en campos de tipo `one2many` y `many2many` desde el registro que los referencía. Las llaves y valores del diccionario pueden ser:
            - `'create'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Create](#relationcommandcreate-comando-de-relación-de-creación)]* — Comando de relación de creación.
            - `'add'`: *[RelationCommand.Add](#relationcommandadd-comando-de-relación-de-adición)* — Comando de relación de adición.
            - `'update'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Update](#relationcommandupdate-comando-de-relación-de-actualización)]* — Comando de relación de actualización.
            - `'replace'`: *[RelationCommand.Replace](#relationcommandreplace-comando-de-relación-de-reemplazo)* — Comando de relación de reemplazo.
            - `'unlink'`: *[RelationCommand.Unlink](#relationcommandunlink-comando-de-relación-de-desvinculación)* — Comando de relación de desvinculación.
            - `'delete'`: *[RelationCommand.Delete](#relationcommanddelete-comando-de-relación-de-eliminación)* — Comando de relación de eliminación.
            - `'clear'`: *[RelationCommand.Clear](#relationcommandclear-comando-de-relación-de-limpieza)* — Comando de relación de limpieza.
        - *[Función de resolución de valor](#valueresolutionfn-función-de-resolución-de-valor)[[_M](#_m-nombre-de-modelo-personalizado)]* Función de resolución de valor que se usa para resolver y retornar un valor que se usará en el campo para almacenarse en la base de datos.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)[[_M](#_m-nombre-de-modelo-personalizado)]* — Criterio de búsqueda.
- `offset` **(Opcional)**: *int* — Desfase de resultados retornados.
- `limit` **(Opcional)**: *int* — Límite de cantidad de resultados retornados.

**Retorno**
- `record_ids`: *list[int]* — Lista de IDs de los registros encontrados.

----

### `read` Lectura de registros
Este método retorna una lista de diccionarios con el contenido de los registros de un modelo de la base de datos a partir de un iterable de IDs, en el orden en el que se especificaron los campos o todos los campos en caso de no haber sido especificados.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[int]* — ID o iterable de IDs de los registros a leer.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer.
- `sortby` **(Opcional)**: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)]* — Nombre o nombres de campo a usar para ordenar los registros.
- `ascending` **(Opcional)**: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[bool]* — Dirección de ordenamiento, ascendente (*True*) o descendente (*False*). Este y el parámetro `sortby` deben coincidir. Si se especificó 1 campo, 1 dirección de ordenamiento debe ser especificada. Si se especificaron $n$ campos de ordenamiento, $n$ direcciones de ordenamiento deben ser especificadas.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)[[_M](#_m-nombre-de-modelo-personalizado)]* — Criterio de búsqueda.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer.
- `offset` **(Opcional)**: *int* — Desfase de resultados retornados.
- `limit` **(Opcional)**: *int* — Límite de cantidad de resultados retornados.
- `sortby` **(Opcional)**: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)]* — Nombre o nombres de campo a usar para ordenar los registros.
- `ascending` **(Opcional)**: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[bool]* — Dirección de ordenamiento, ascendente (*True*) o descendente (*False*). Este y el parámetro `sortby` deben coincidir. Si se especificó 1 campo, 1 dirección de ordenamiento debe ser especificada. Si se especificaron $n$ campos de ordenamiento, $n$ direcciones de ordenamiento deben ser especificadas.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)[[_M](#_m-nombre-de-modelo-personalizado)]* — Criterio de búsqueda.

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

Pueden crearse registros referenciados a través de la declaración del valor del campo usando un [comando de relación](#comandos-de-relación):
```py
db.search_read(session_uuid, 'base.users', 2, fields= ['login', 'name', 'role_ids'])
# [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', 'role_ids': [1, 2, 3, ..., 18]}]

db.update(
    'base.users',
    2
    {
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de creación
            'create': {
                # Datos de registro de un rol en el modelo [base.users.role]
                'name': 'super_admin_role',
                'label': 'Rol de superadministrador',
                ...
            }
        }
    }
)

db.search_read(session_uuid, 'base.users', 2, fields= ['login', 'name', 'role_ids'])
# [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', 'role_ids': [1, 2, 3, ..., 18, 19]}]
```

**Parámetros**
- `session_uuid`: *str* — UUID de sesión.
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[int]* — ID o iterable de IDs de los registros a actualizar.
- `data`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[InputRecordData](#inputrecorddata-datos-de-registro)]* — Diccionario o iterable de diccionarios de los datos a modificar.
    1. Las llaves deben ser de tipo *[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)* — Nombre de campo existente en el modelo.
    2. Los valores pueden ser cualquiera de los siguientes tipos de entrada:
        - *[DMLScalarCompatible](#dmlscalarcompatible-escalar-compatible-con-postgresql)* — Tipo de dato que se puede usar como valor para un campo de modelo. El tipo de dato puede ser:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `datetime.date`
            - `datetime.datetime`
            - `datetime.time`
            - `datetime.timedelta`
            - `None`
        - *[JSONLike](#jsonlike-estructura-equivalente-a-json)* — Estructura equivalente a JSON. El tipo de dato puede ser escalar o iterable de:
            - [JSONLikeScalar](#jsonlikescalar-escalar-serializable) que representa los tipos:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `None`
            - [JSONLikeObjShape](#jsonlikeobjshape-diccionario-serializable) que representa un diccionario serializable conformado
            por:
                - Llaves que deben ser de tipo `str`
                - Valores que pueden ser escalar o iterable de:
                    - [JSONLikeScalar](#jsonlikescalar-escalar-serializable)
                    - [JSONLike](#jsonlike-estructura-equivalente-a-json)
        - *[InputRecordData](#inputrecorddata-datos-de-registro)* — Datos para crear un registro vinculado, en campos de tipo `many2one`.
        - *[RelationCommands](#comandos-de-relación)[[_M](#_m-nombre-de-modelo-personalizado)]* — Comandos de modificación de los registros referenciados en campos de tipo `one2many` y `many2many` desde el registro que los referencía. Las llaves y valores del diccionario pueden ser:
            - `'create'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Create](#relationcommandcreate-comando-de-relación-de-creación)]* — Comando de relación de creación.
            - `'add'`: *[RelationCommand.Add](#relationcommandadd-comando-de-relación-de-adición)* — Comando de relación de adición.
            - `'update'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Update](#relationcommandupdate-comando-de-relación-de-actualización)]* — Comando de relación de actualización.
            - `'replace'`: *[RelationCommand.Replace](#relationcommandreplace-comando-de-relación-de-reemplazo)* — Comando de relación de reemplazo.
            - `'unlink'`: *[RelationCommand.Unlink](#relationcommandunlink-comando-de-relación-de-desvinculación)* — Comando de relación de desvinculación.
            - `'delete'`: *[RelationCommand.Delete](#relationcommanddelete-comando-de-relación-de-eliminación)* — Comando de relación de eliminación.
            - `'clear'`: *[RelationCommand.Clear](#relationcommandclear-comando-de-relación-de-limpieza)* — Comando de relación de limpieza.
        - *[Función de resolución de valor](#valueresolutionfn-función-de-resolución-de-valor)[[_M](#_m-nombre-de-modelo-personalizado)]* Función de resolución de valor que se usa para resolver y retornar un valor que se usará en el campo para almacenarse en la base de datos.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[int]* — ID o iterable de IDs de los registros a eliminar.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
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

ctx.create(session_uuid, 'base.users', record)

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

ctx.create(session_uuid, 'base.users', records)
```

Pueden crearse registros referenciados a través de la declaración del valor del campo usando un [comando de relación](#comandos-de-relación):
```py
ctx.create(
    'base.users',
    {
        'login': 'onnymm',
        'name': 'Onnymm Azzur',
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de creación
            'create': {
                # Datos de registro de un rol en el modelo [base.users.role]
                'name': 'super_admin_role',
                'label': 'Rol de superadministrador',
                ...
            }
        }
    }
)
```

**Parámetros**
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `data`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[InputRecordData](#inputrecorddata-datos-de-registro)]* — Diccionario o iterable de diccionarios de datos de los registros a crear:
    1. Las llaves deben ser de tipo *[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)* — Nombre de campo existente en el modelo.
    2. Los valores pueden ser cualquiera de los siguientes tipos de entrada:
        - *[DMLScalarCompatible](#dmlscalarcompatible-escalar-compatible-con-postgresql)* — Tipo de dato que se puede usar como valor para un campo de modelo. El tipo de dato puede ser:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `datetime.date`
            - `datetime.datetime`
            - `datetime.time`
            - `datetime.timedelta`
            - `None`
        - *[JSONLike](#jsonlike-estructura-equivalente-a-json)* — Estructura equivalente a JSON. El tipo de dato puede ser escalar o iterable de:
            - [JSONLikeScalar](#jsonlikescalar-escalar-serializable) que representa los tipos:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `None`
            - [JSONLikeObjShape](#jsonlikeobjshape-diccionario-serializable) que representa un diccionario serializable conformado
            por:
                - Llaves que deben ser de tipo `str`
                - Valores que pueden ser escalar o iterable de:
                    - [JSONLikeScalar](#jsonlikescalar-escalar-serializable)
                    - [JSONLike](#jsonlike-estructura-equivalente-a-json)
        - *[InputRecordData](#inputrecorddata-datos-de-registro)* — Datos para crear un registro vinculado, en campos de tipo `many2one`.
        - *[RelationCommands](#comandos-de-relación)[[_M](#_m-nombre-de-modelo-personalizado)]* — Comandos de modificación de los registros referenciados en campos de tipo `one2many` y `many2many` desde el registro que los referencía. Las llaves y valores del diccionario pueden ser:
            - `'create'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Create](#relationcommandcreate-comando-de-relación-de-creación)]* — Comando de relación de creación.
            - `'add'`: *[RelationCommand.Add](#relationcommandadd-comando-de-relación-de-adición)* — Comando de relación de adición.
            - `'update'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Update](#relationcommandupdate-comando-de-relación-de-actualización)]* — Comando de relación de actualización.
            - `'replace'`: *[RelationCommand.Replace](#relationcommandreplace-comando-de-relación-de-reemplazo)* — Comando de relación de reemplazo.
            - `'unlink'`: *[RelationCommand.Unlink](#relationcommandunlink-comando-de-relación-de-desvinculación)* — Comando de relación de desvinculación.
            - `'delete'`: *[RelationCommand.Delete](#relationcommanddelete-comando-de-relación-de-eliminación)* — Comando de relación de eliminación.
            - `'clear'`: *[RelationCommand.Clear](#relationcommandclear-comando-de-relación-de-limpieza)* — Comando de relación de limpieza.
        - *[Función de resolución de valor](#valueresolutionfn-función-de-resolución-de-valor)[[_M](#_m-nombre-de-modelo-personalizado)]* Función de resolución de valor que se usa para resolver y retornar un valor que se usará en el campo para almacenarse en la base de datos.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)[[_M](#_m-nombre-de-modelo-personalizado)]* — Criterio de búsqueda.
- `offset` **(Opcional)**: *int* — Desfase de resultados retornados.
- `limit` **(Opcional)**: *int* — Límite de cantidad de resultados retornados.

**Retorno**
- `record_ids`: *list[int]* — Lista de IDs de los registros encontrados.

----

#### `read` Lectura de registros
Este método retorna una lista de diccionarios con el contenido de los registros de un modelo de la base de datos a partir de un iterable de IDs, en el orden en el que se especificaron los campos o todos los campos en caso de no haber sido especificados.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[int]* — ID o iterable de IDs de los registros a leer.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer.
- `sortby` **(Opcional)**: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)]* — Nombre o nombres de campo a usar para ordenar los registros.
- `ascending` **(Opcional)**: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[bool]* — Dirección de ordenamiento, ascendente (*True*) o descendente (*False*). Este y el parámetro `sortby` deben coincidir. Si se especificó 1 campo, 1 dirección de ordenamiento debe ser especificada. Si se especificaron $n$ campos de ordenamiento, $n$ direcciones de ordenamiento deben ser especificadas.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)[[_M](#_m-nombre-de-modelo-personalizado)]* — Criterio de búsqueda.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer.
- `offset` **(Opcional)**: *int* — Desfase de resultados retornados.
- `limit` **(Opcional)**: *int* — Límite de cantidad de resultados retornados.
- `sortby` **(Opcional)**: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)]* — Nombre o nombres de campo a usar para ordenar los registros.
- `ascending` **(Opcional)**: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[bool]* — Dirección de ordenamiento, ascendente (*True*) o descendente (*False*). Este y el parámetro `sortby` deben coincidir. Si se especificó 1 campo, 1 dirección de ordenamiento debe ser especificada. Si se especificaron $n$ campos de ordenamiento, $n$ direcciones de ordenamiento deben ser especificadas.

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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `search_criteria` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)[[_M](#_m-nombre-de-modelo-personalizado)]* — Criterio de búsqueda.

**Retorno**
- `count`: *int* — Total de registros encontrados.

----

#### `update` Actualización de registros
Este método realiza la actualización de uno o más registros a partir de su respectiva ID provista, actualizando uno o más campos con el valor provisto. Este método solo sobreescribe un mismo valor por cada campo a todos los registros provistos.

Uso:
```py
ctx.search_read(session_uuid, 'base.users', fields= ['login', 'name'])
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
#   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii'},
#   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim'},
#   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio'},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
#   ...
# ]

# Modificación
ctx.update(session_uuid, 'base.users', [3, 4, 5], {'name': 'Cambiado'})
# True

ctx.search_read(session_uuid, 'base.users', fields= ['login', 'name'])
# [
#   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
#   {'id': 3, 'name': 'Cambiado', 'login': 'lumii'},
#   {'id': 4, 'name': 'Cambiado', 'login': 'meshkim'},
#   {'id': 5, 'name': 'Cambiado', 'login': 'luunafio'},
#   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
#   ...
# ]
```

Pueden crearse registros referenciados a través de la declaración del valor del campo usando un [comando de relación](#comandos-de-relación):
```py
ctx.search_read(session_uuid, 'base.users', 2, fields= ['login', 'name', 'role_ids'])
# [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', 'role_ids': [1, 2, 3, ..., 18]}]

ctx.update(
    'base.users',
    2
    {
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de creación
            'create': {
                # Datos de registro de un rol en el modelo [base.users.role]
                'name': 'super_admin_role',
                'label': 'Rol de superadministrador',
                ...
            }
        }
    }
)

ctx.search_read(session_uuid, 'base.users', 2, fields= ['login', 'name', 'role_ids'])
# [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', 'role_ids': [1, 2, 3, ..., 18, 19]}]
```

**Parámetros**
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[int]* — ID o iterable de IDs de los registros a actualizar.
- `data`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[RecordData]* — Diccionario o iterable de diccionarios de los datos a modificar:
    1. Las llaves deben ser de tipo *[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)* — Nombre de campo existente en el modelo.
    2. Los valores pueden ser cualquiera de los siguientes tipos de entrada:
        - *[DMLScalarCompatible](#dmlscalarcompatible-escalar-compatible-con-postgresql)* — Tipo de dato que se puede usar como valor para un campo de modelo. El tipo de dato puede ser:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `datetime.date`
            - `datetime.datetime`
            - `datetime.time`
            - `datetime.timedelta`
            - `None`
        - *[JSONLike](#jsonlike-estructura-equivalente-a-json)* — Estructura equivalente a JSON. El tipo de dato puede ser escalar o iterable de:
            - [JSONLikeScalar](#jsonlikescalar-escalar-serializable) que representa los tipos:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `None`
            - [JSONLikeObjShape](#jsonlikeobjshape-diccionario-serializable) que representa un diccionario serializable conformado
            por:
                - Llaves que deben ser de tipo `str`
                - Valores que pueden ser escalar o iterable de:
                    - [JSONLikeScalar](#jsonlikescalar-escalar-serializable)
                    - [JSONLike](#jsonlike-estructura-equivalente-a-json)
        - *[InputRecordData](#inputrecorddata-datos-de-registro)* — Datos para crear un registro vinculado, en campos de tipo `many2one`.
        - *[RelationCommands](#comandos-de-relación)[[_M](#_m-nombre-de-modelo-personalizado)]* — Comandos de modificación de los registros referenciados en campos de tipo `one2many` y `many2many` desde el registro que los referencía. Las llaves y valores del diccionario pueden ser:
            - `'create'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Create](#relationcommandcreate-comando-de-relación-de-creación)]* — Comando de relación de creación.
            - `'add'`: *[RelationCommand.Add](#relationcommandadd-comando-de-relación-de-adición)* — Comando de relación de adición.
            - `'update'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Update](#relationcommandupdate-comando-de-relación-de-actualización)]* — Comando de relación de actualización.
            - `'replace'`: *[RelationCommand.Replace](#relationcommandreplace-comando-de-relación-de-reemplazo)* — Comando de relación de reemplazo.
            - `'unlink'`: *[RelationCommand.Unlink](#relationcommandunlink-comando-de-relación-de-desvinculación)* — Comando de relación de desvinculación.
            - `'delete'`: *[RelationCommand.Delete](#relationcommanddelete-comando-de-relación-de-eliminación)* — Comando de relación de eliminación.
            - `'clear'`: *[RelationCommand.Clear](#relationcommandclear-comando-de-relación-de-limpieza)* — Comando de relación de limpieza.
        - *[Función de resolución de valor](#valueresolutionfn-función-de-resolución-de-valor)[[_M](#_m-nombre-de-modelo-personalizado)]* Función de resolución de valor que se usa para resolver y retornar un valor que se usará en el campo para almacenarse en la base de datos.

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

- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `record_ids`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[int]* — ID o iterable de IDs de los registros a eliminar.

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
La clase de contexto de ejecución es la usada en todas las transacciones CRUD expuestas en los [métodos](#métodos) de la instancia principal y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listadas a continuación:

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
La clase de contexto de acción es usada como argumento en las funciones de acción y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listadas a continuación:

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
La clase de contexto de automatización es usada como argumento en las funciones de automatización y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listadas a continuación:

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
La clase de contexto de tarea de servidor es usada como argumento en las funciones de tarea de servidor y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listadas a continuación:

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

### `ValueResolutionContext` Contexto de resolución de valor
La clase de contexto de resolución de valor es usada como argumento en las funciones de resolución de valor y hereda todas las propiedades de la clase [BaseContext](#basecontext-contexto-base)[[_M](#_m-nombre-de-modelo-personalizado)] listadas a continuación:

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

#### `record_data` Datos de registro (Contexto de resolución de valor)
Datos de registro del que proviene la función a ejecutar.

**Retorno**
- `record_data`: *[`InputRecordData` — Datos de registro](#inputrecorddata-datos-de-registro)* Datos de registro del que proviene la función a ejecutar.

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

- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
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
- `model_name`: *[ModelName](#modelname-nombre-de-modelo)[[_M](#_m-nombre-de-modelo-personalizado)]* — Nombre de modelo en la base de datos.
- `fields` **(Opcional)**: *list[[FieldReadDeclaration](#fieldreaddeclaration-declaración-de-campos-a-leer)]* — Declaración de campos a leer antes de la ejecución de la acción, accesibles por el atributo `data`. Si el parámetro no se especifica, solo el valor `'id'` estará disponible.
- `execute_only_when` **(Opcional)**: *[CriteriaStructure](#criteriastructrure-estructura-de-criterio-de-búsqueda)[[_M](#_m-nombre-de-modelo-personalizado)]* — Criterio requerido para que la automatización se ejecute sobre el registro.

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
Las tareas de servidor se ejecutan invocándolas con el nombre con el que fueron registradas. Para más información, véase [Registro de tareas de servidor](#registro-de-tareas-de-servidor).

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

----

## Comandos de relación
Este tipo de dato representa un diccionario que contiene comandos de modificación de los registros referenciados en campos de tipo `one2many` y `many2many` ya sea crear, añadir, desvincular, reemplazar o limpiar la lista de registros relacionados o modificando registros específicos desde el registro que los referencía.

Las llaves y valores del diccionario pueden ser:
- `'create'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Create](#relationcommandcreate-comando-de-relación-de-creación)]* — Comando de relación de creación.
- `'add'`: *[RelationCommand.Add](#relationcommandadd-comando-de-relación-de-adición)* — Comando de relación de adición.
- `'update'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Update](#relationcommandupdate-comando-de-relación-de-actualización)]* — Comando de relación de actualización.
- `'replace'`: *[RelationCommand.Replace](#relationcommandreplace-comando-de-relación-de-reemplazo)* — Comando de relación de reemplazo.
- `'unlink'`: *[RelationCommand.Unlink](#relationcommandunlink-comando-de-relación-de-desvinculación)* — Comando de relación de desvinculación.
- `'delete'`: *[RelationCommand.Delete](#relationcommanddelete-comando-de-relación-de-eliminación)* — Comando de relación de eliminación.
- `'clear'`: *[RelationCommand.Clear](#relationcommandclear-comando-de-relación-de-limpieza)* — Comando de relación de limpieza.

### `RelationCommand.Create` Comando de relación de creación
El comando de relación de creación permite enviar instrucciones de creación de registros hijos que luego se van a vincular al campo de relación `one2many` o `many2many` (según sea el caso) del registro desde el que se ha codificado el comando.

> El tipo de dato del comando es un diccionario de datos del tipo [InputRecordData](#inputrecorddata-datos-de-registro) que cumple con la forma de los registros del modelo relacionado al campo.

Ejemplo:
```py
db.update(
    'base.users',
    record_id,
    {
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de relación de creación
            'create': {
                'name': 'command_admin',
                'label': 'Administrador de comandos',
                ...
            }
        }
    }
)
```

### `RelationCommand.Add` Comando de relación de adición
El comando de relación de adición permite enviar instrucciones de adición de registros hijos que luego se van a vincular al campo de relación `many2many` del registro desde el que se ha codificado el comando.

> El tipo de dato del comando es un escalar o iterable de IDs de registros del modelo relacionado al campo.

Ejemplo:
```py
db.create(
    'base.users',
    {
        'login': 'lumii',
        'name': 'Lumii Mynx',
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de relación de adición
            'add': [1, 2, 3] # Registros que ya existen
        }
    }
)
```

### `RelationCommand.Update` Comando de relación de actualización
El comando de relación de actualización permite enviar instrucciones de modificación de los registros hijos vinculados al campo de relación `one2many` o `many2many` (según sea el caso) del registro desde el que se ha codificado el comando.

> El tipo de dato del comando es una tupla que contiene:
> 1. Escalar o iterable de IDs de registro a modificar.
> 2. Diccionario de datos del tipo [InputRecordData](#inputrecorddata-datos-de-registro) que cumple con la forma de los registros del modelo relacionado al campo.

Ejemplo:
```py
db.update(
    'base.users',
    record_id,
    {
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de relación de actualización
            'update': (
                # ID a modificar
                2,
                {
                    'name': 'Administrador supremo de comandos',
                    ...
                }
            )
        }
    }
)
```

### `RelationCommand.Replace` Comando de relación de reemplazo
El comando de relación de reemplazo permite enviar instrucciones de reemplazo de los registros hijos vinculados al campo de relación `many2many` del registro desde el que se ha codificado el comando por los registros provistos en el comando.

> El tipo de dato del comando es un escalar o iterable de IDs de registros del modelo relacionado al campo.

Ejemplo:
```py
db.update(
    'base.users',
    record_id,
    {
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de relación de reemplazo
            'replace': [4, 5] # Cualquier otra ID vinculada es reemplazada por estas
        }
    }
)
```

### `RelationCommand.Unlink` Comando de relación de desvinculación
El comando de relación de desvinculación permite enviar instrucciones para desvincular registros hijos vinculados al campo de relación `one2many` o `many2many` (según sea el caso) del registro desde el que se ha codificado el comando.

> El tipo de dato del comando es un escalar o iterable de IDs de registros del modelo relacionado al campo.

Ejemplo:
```py
db.update(
    'base.users',
    {
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de relación de desvinculación
            'unlink': [2, 3]
        }
    }
)
```

### `RelationCommand.Delete` Comando de relación de eliminación
El comando de relación de eliminación permite enviar instrucciones para eliminar registros hijos vinculados al campo de relación `one2many` o `many2many` (según sea el caso) del registro desde el que se ha codificado el comando.

> El tipo de dato del comando es un escalar o iterable de IDs de registros del modelo relacionado al campo.

Ejemplo:
```py
db.update(
    'base.users',
    {
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de relación de eliminación
            'delete': [6]
        }
    }
)
```

### `RelationCommand.Clear` Comando de relación de limpieza
El comando de relación de limpieza permite enviar instrucciones para limpiar la relación con todos los registros hijos vinculados al campo de relación `one2many` o `many2many` (según sea el caso) del registro desde el que se ha codificado el comando. Este comando desvincula los registros sin eliminarlos, tal como lo haría el comando *[RelationCommand.Unlink](#relationcommandunlink-comando-de-relación-de-desvinculación)* pero sin especificar explícitamente las IDs y desvinculando todos los registros sin importar cuáles son.

> El tipo de dato del comando es un Literal el `True`.

Ejemplo:
```py
db.update(
    'base.users',
    {
        # Campo de tipo [many2many]
        'role_ids': {
            # Comando de relación de eliminación
            'clear': True # Se le remueven todos los roles al usuario
        }
    }
)
```

----

## Tipados

### `_M` Nombre de modelo personalizado
Genérico usado para extender los nombres de modelo a nombres de modelo personalizados originalmente representados por el tipo [ModelName](#modelname-nombre-de-modelo).

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
La estructura del criterio de búsqueda expresa un conjunto de condiciones que se pueden usar para filtrar registros en la base de datos al momento de leer o invocar registros para un fin específico.

La estructura se conforma de un iterable con los tipos:
- `TripletStructure`: Tupla de 3 posiciones que representa una condición.
- `LogicOperator`: Operador lógico que une tripletas de condiciones.

> **ESTRUCTURA DE TRIPLETAS DE CONDICIÓN**
> 
> Este tipo de dato representa una condición para usarse en una transacción en
> base de datos.
> 
> La estructura de una tripleta consiste en 3 diferentes parámetros:
> 1. Referencia de campo. Puede ser alguno de los siguientes tipos:
>     - [FieldName](#fieldname-nombre-de-campo-existente-en-el-modelo) — Nombre del campo del modelo o referencia *Many2One*
>     - [FieldComputation](#fieldcomputation-cómputo-de-campo)[[_M](#_m-nombre-de-modelo-personalizado)] — Cómputo de campo.
> 2. Operador de comparación. Puede ser alguno de los siguientes literales:
>     - `'='`: Igual a
>     - `'!='`: Diferente de
>     - `'=?'`: No está establecido o es igual a
>     - `'>'`: Mayor a
>     - `'>='`: Mayor o igual a
>     - `'<'`: Menor que
>     - `'<='`: Menor o igual que
>     - `'in'`: Está en
>     - `'not in'`: No está en
>     - `'like'`: Contiene (sensible a mayúsculas y minúsculas)
>     - `'ilike'`: Contiene (no sensible a mayúsculas y minúsculas)
>     - `'not like'`: No contiene (sensible a mayúsculas y minúsculas)
>     - `'not ilike'`: No contiene (no sensible a mayúsculas y minúsculas)
>     - `'starts with'`: Comienza con (sensible a mayúsculas y minúsculas)
>     - `'ends with'`: Termina con (sensible a mayúsculas y minúsculas)
>     - `'~'`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
>     - `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)
>     - `!'~'`: No coincide con expresión regular (sensible a mayúsculas y minúsculas)
>     - `!'~*'`: No coincide con expresión regular (no sensible a mayúsculas y minúsculas)
> 3. Valor de comparación. Puede ser alguno de los siguientes tipos:
>     - *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[DMLScalarCompatible](#dmlscalarcompatible-escalar-compatible-con-postgresql)]* — Escalar o iterable de Tipo de dato que se puede usar como valor para un campo de modelo. El tipo de dato puede ser:
>         - `int`
>         - `float`
>         - `str`
>         - `bool`
>         - `datetime.date`
>         - `datetime.datetime`
>         - `datetime.time`
>         - `datetime.timedelta`
>         - `None`
>     - *[ValueResolutionFn](#valueresolutionfn-función-de-resolución-de-valor)[[_M](#_m-nombre-de-modelo-personalizado)]* Función de resolución de valor que se usa para resolver y retornar un valor que se usará en el campo para almacenarse en la base de datos.
> 
> Algunos ejemplos de tripletas:
> ```py
> ('name', 'like', 'Onnymm')
> # El nombre contiene 'Onnymm'
> ('id', '=', 5)
> # La ID es igual a 5
> ('create_uid.name', 'ends with', 'Azzur')
> # El nombre del usuario creador del registro termina con "Azzur"
> ('device_id.type_id.create_date', '=', lambda ctx: ctx.today())
> # La fecha de creación del tipo de dispostivo del dispositivo es igual a hoy
> (('subtotal', 'float', lambda ctx: ctx['qty'] * ctx['price']), '<', 500)
> # El cómputo del subtotal es menor a 500
> ```
> 
> Las tuplas de estructura se deben unir por medio de un operador lógico que va
> al principio. Por ejemplo:
> ```py
> ('amount', '>', 500)
> # El monto es mayor a 500
> ('name', 'ilike', 'as')
> # El nombre contiene "as"
> 
> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
> # El monto es mayor a 500 y el nombre contiene "as"
> ```
> 
> ----
> 
> **OPERADOR LÓGICO**
> 
> Tipo de dato que representa un operador lógico.
> 
> Los operadores lógicos disponibles son:
> - `'&'`: AND
> - `'|'`: OR

### `DMLScalarCompatible` Escalar compatible con PostgreSQL
Tipo de dato que se puede usar como valor para un campo de modelo en la base datos al crear o modificar registros y para usarse como valor en filtros de búsqueda.

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

### `DMLTransaction` Transacción DML
Alias usado para describir el literal de nombres de transacciones CRUD que excluye lectura. Los valores disponibles son:
- `'create'`: Creación de registros.
- `'update'`: Modificación de registros.
- `'delete'`: Eliminación de registros.

### `FieldComputation` Cómputo de campo
Representación para declarar el cómputo de un campo en tiempo real. La estructura está conformada por una tupla de 3 elementos:
1. [FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo) — Nombre de campo existente en el modelo.
2. [TTypeName](#ttypename-nombre-de-tipo-de-dato-de-campo) — Nombre de tipo de dato de campo.
3. [ComputeFieldFn](#computefieldfn-función-de-cómputo-de-campo)[[_M](#_m-nombre-de-modelo-personalizado)] — Función de cómputo de campo.

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
Este tipado representa un iterable de cualquiera de los siguientes tipos o representaciones:
- [FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo) — Nombre de campo existente en el modelo.
- [_Aliased](#_aliased-alias-de-tipo-_t-para-declaración-de-campos)[[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)] — Nombre de campo con alias.
- [FieldComputation](#fieldcomputation-cómputo-de-campo)[[_M](#_m-nombre-de-modelo-personalizado)] — Cómputo de campo.

### `InputRecordData` Datos de registro
Diccionario que contiene los datos de un registro para ser creado o modificado.

1. Las llaves deben ser de tipo *[FieldName](#_fieldname-nombre-de-campo-existente-en-el-modelo)* — Nombre de campo existente en el modelo.
2. Los valores pueden ser cualquiera de los siguientes tipos de entrada:
    - *[DMLScalarCompatible](#dmlscalarcompatible-escalar-compatible-con-postgresql)* — Tipo de dato que se puede usar como valor para un campo de modelo. El tipo de dato puede ser:
        - `int`
        - `float`
        - `str`
        - `bool`
        - `datetime.date`
        - `datetime.datetime`
        - `datetime.time`
        - `datetime.timedelta`
        - `None`
    - *[JSONLike](#jsonlike-estructura-equivalente-a-json)* — Estructura equivalente a JSON. El tipo de dato puede ser escalar o iterable de:
        - [JSONLikeScalar](#jsonlikescalar-escalar-serializable) que representa los tipos:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `None`
        - [JSONLikeObjShape](#jsonlikeobjshape-diccionario-serializable) que representa un diccionario serializable conformado
        por:
            - Llaves que deben ser de tipo `str`
            - Valores que pueden ser escalar o iterable de:
                - [JSONLikeScalar](#jsonlikescalar-escalar-serializable)
                - [JSONLike](#jsonlike-estructura-equivalente-a-json)
    - *[InputRecordData](#inputrecorddata-datos-de-registro)* — Datos para crear un registro vinculado, en campos de tipo `many2one`.
    - *[RelationCommands](#comandos-de-relación)[[_M](#_m-nombre-de-modelo-personalizado)]* — Comandos de modificación de los registros referenciados en campos de tipo `one2many` y `many2many` desde el registro que los referencía. Las llaves y valores del diccionario pueden ser:
        - `'create'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Create](#relationcommandcreate-comando-de-relación-de-creación)]* — Comando de relación de creación.
        - `'add'`: *[RelationCommand.Add](#relationcommandadd-comando-de-relación-de-adición)* — Comando de relación de adición.
        - `'update'`: *[ScalarOrIterable](#scalaroriterable-elemento-o-iterable-de-elementos)[[RelationCommand.Update](#relationcommandupdate-comando-de-relación-de-actualización)]* — Comando de relación de actualización.
        - `'replace'`: *[RelationCommand.Replace](#relationcommandreplace-comando-de-relación-de-reemplazo)* — Comando de relación de reemplazo.
        - `'unlink'`: *[RelationCommand.Unlink](#relationcommandunlink-comando-de-relación-de-desvinculación)* — Comando de relación de desvinculación.
        - `'delete'`: *[RelationCommand.Delete](#relationcommanddelete-comando-de-relación-de-eliminación)* — Comando de relación de eliminación.
        - `'clear'`: *[RelationCommand.Clear](#relationcommandclear-comando-de-relación-de-limpieza)* — Comando de relación de limpieza.
    - *[Función de resolución de valor](#valueresolutionfn-función-de-resolución-de-valor)[[_M](#_m-nombre-de-modelo-personalizado)]* Función de resolución de valor que se usa para resolver y retornar un valor que se usará en el campo para almacenarse en la base de datos.

### `JSONLikeObjShape` Diccionario serializable
Diccionario compatible para ser serializado a tipo de dato `JSONB` por el motor
de PostgreSQL.

- El tipo de dato de la llave debe ser `str`.
- El tipo de dato del valor puede ser escalar o iterable de:
    - [JSONLikeScalar](#jsonlikescalar-escalar-serializable)
    - [JSONLike](#jsonlike-estructura-equivalente-a-json)

### `JSONLikeScalar` Escalar serializable
Tipo de dato escalar serializable a JSON.

El tipo de dato puede ser:
- `int`
- `float`
- `str`
- `bool`
- `None`

### `JSONLike` Estructura equivalente a JSON
Tipo de dato compatible para ser serializado a tipo de dato `JSONB` por el
motor de PostgreSQL.

El tipo de dato puede ser escalar o iterable de:
- [JSONLikeScalar](#jsonlikescalar-escalar-serializable) que representa los tipos:
    - `int`
    - `float`
    - `str`
    - `bool`
    - `None`
- [JSONLikeObjShape](#jsonlikeobjshape-diccionario-serializable) que representa un diccionario serializable conformado
por:
    - Llaves que deben ser de tipo `str`
    - Valores que pueden ser escalar o iterable de:
        - [JSONLikeScalar](#jsonlikescalar-escalar-serializable)
        - [JSONLike](#jsonlike-estructura-equivalente-a-json)

Los valores son convertidos a notación *JSON* (JavaScript Object Notation):
- `int` → `number` (Sin punto decimal)
- `float` → `number` (Con punto decimal)
- `str` → `string`
- `bool` → `boolean`
- `dict` → `object`
- `list` → `array`
- `tuple` → `array`

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

### `ScalarOrIterable` Elemento o iterable de elementos
Genérico que representa la unión de un escalar y un iterable de tipos [_T](#_t-parámetro-de-tipo-_t).

Ejemplo:
```py
# Una función f que recibe un entero o un iterable de enteros, como una lista
def f(x: int | Iterable[int]):
    ...

# ScalarOrIterable usado como abstracción del mismo tipo
def f(x: ScalarOrIterable[int]):
    ...
```

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

----

## `ValueResolutionFn` Función de resolución de valor
Las funciones de resolución de valor se usan como valor en los datos de entrada para crear o modificar registros por medio de los métodos correspondientes de la instancia principal o los contextos usados en funciones de ejecución de transacciones, automatizaciones, acciones, tareas de servidor, validaciones y políticas. Estas funciones se usan para resolver y retornar un valor que se usará como valor del campo para almacenarse en la base de datos.

Por ejemplo, si quisiéramos crear un campo vinculado a un modelo específico cuyo ID desconocemos podemos usar el método [Obtención de ID de recurso](#get_resource_id-obtención-de-id-de-recurso) usando la referencia única del modelo:
```py
db.create(
    'base.model.field',
    {
        'name': 'hire_date',
        'label': 'Fecha de contrato',
        'ttype': 'date',
        # Función de resolución para asignar una ID
        'model_id': lambda ctx: ctx.get_resource_id('base_model.hr_employee'),
    },
)
```

Antes de que el registro sea ingresado para ser creado en la base de datos, la función de resolución de valor es ejecutada usando un contexto de resolución de valor. La ID del modelo se obtiene, se reemplaza la función por el valor y entonces el registro es enviado para ser creado:
```py
{
    'name': 'hire_date',
    'label': 'Fecha de contrato',
    'ttype': 'date',
    'model_id': 27,
},
```

> ℹ️ Para este caso también podríamos modificar directamente el registro del modelo `hr.employee` (Si contamos con la ID) y modificar el campo de `field_ids` usando un [comando de relación de creación](#relationcommandcreate-comando-de-relación-de-creación) proporcionando los datos del campo a crear.

Existen casos más complejos como cuando se lleva a cabo un registro de asistencia de los empleados donde cada uno registra su hora de inicio de jornada laboral, inicio de comida, fin de comida y fin de jornada laboral. Si se quisiera poder ver métricas diarias como si el empleado tuvo un retraso al iniciar su jornada laboral o saber cuánto tiempo se tomó en su tiempo de comida sería ideal computar esos valores dentro de un registro diario. Entonces, cuando se crea el primer registro de evento de asistencia, también se crea un registro de día de asistencia. Pero al crearse el segundo, solo queremos que se vincule el registro (ya existente a este punto) de día de asistencia del empleado. Podemos entonces hacer una función para resolver en la ID de registro de día de asistencia a vincular al momento de crear el registro de evento de asistencia:
```py
# Modelo de día de asistencia: [assistance.registry.day]
# Modelo de evento de asistencia: [assistance.registry.event]

def create_or_link_day_record(ctx: Lylac.ValueResolutionContext):

    # Obtención de los valores relevantes
    employee_id = ctx.record_data['employee_id']
    date = ctx.record_data['date']

    # Búsqueda del registro
    results = ctx.search(
        'assistance.registry.day',
        ['&', ('employe_id.id', '=', employee_id), ('date', '=', date)]
    )

    # Si se encontró un resultado...
    if results:
        # Obtención de la ID del registro de día de asistencia
        [ day_id ] = results
    # Si no se encontró resultado...
    [ day_id ] = ctx.create(
        'assistance.registry.day',
        {
            'date': date,
            'employee_id': employee_id,
        },
    )

    return day_id

# Creación de registro de evento
db.create(
    'assistance.registry.event',
    {
        'employee_id': employee_id,
        'registry_time': registry_time,
        'status': status,
        # Función provista como valor del campo
        'day_id': create_or_link_day_record,
        ...,
    }
)
```

**Parámetros de la función de resolución de valor**

- `ctx`: *[ValueResolutionContext](#valueresolutioncontext-contexto-de-resolución-de-valor)[[_M](#_m-nombre-de-modelo-personalizado)]* — Contexto de resolución de valor.

**Retorno**
- `response`: *Any* — Lo que sea que la función tenga que retornar para resolver el valor.
