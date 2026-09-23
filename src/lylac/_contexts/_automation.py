from typing import Generic
from typing import TYPE_CHECKING
from .._resources import ModelDataIndex
from .._typing.generics import ModelName
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R
from .engines import BaseContext

if TYPE_CHECKING:
    from .._operations import DDL
    from .._orchestrator import CRUD
    from .._contexts import ExecutionContext

class AutomationContext(Generic[_M, _R], BaseContext[_M]):
    """
    ## Contexto de automatización
    La clase de contexto de automatización es usada como argumento en las funciones de
    automatización y hereda todas las propiedades de la clase `BaseContext`.

    ### Datos de los registros
    Atributo por el cual se puede acceder a los datos de los registros sobre los que se
    ejecuta una automatización. Estos datos están definidos por el parámetro `fields`
    al registrar la automatización.

    Uso:
    >>> ctx.records
    >>> # [{'id': 3, 'name': ...}, {'id': 7, 'name': ...}]

    ### ID de registro
    Atributo por el cual se puede acceder a la ID del registro sobre el que se
    ejecuta una acción.

    Uso:
    >>> ctx.record_id
    >>> # [int]

    ### ID del usuario que ejecuta la transacción
    Este es un atributo de solo lectura. Muestra la ID del usuario que está
    ejecutando la transacción.

    Uso:
    >>> ctx.uid
    >>> # [int]

    ### Creación de uno o muchos registros
    Este método realiza la creación de uno o muchos registros.

    Uso:
    >>> # Para un solo registro
    >>> record = {
    >>>     'login': 'onnymm',
    >>>     'name': 'Onnymm Azzur',
    >>> }
    >>> 
    >>> ctx.create('base.users', record)
    >>> 
    >>> # Para muchos registros
    >>> records = [
    >>>     {
    >>>         'login': 'onnymm',
    >>>         'name': 'Onnymm Azzur',
    >>>     },
    >>>     {
    >>>         'login': 'lumii',
    >>>         'name': 'Lumii Mynx',
    >>>     },
    >>> ]
    >>> 
    >>> ctx.create('base.users', records)

    ### Búsqueda de registros
    Este método retorna todas las IDs de los registros de un modelo o los registros
    que cumplan con la condición de búsqueda provista.

    Uso:
    >>> # Registros existentes en el modelo base.users
    >>> ctx.search('base.users')
    >>> # [1, 2, 3, 4, 5, 6, 7]
    >>> 
    >>> # Registros en el modelo base.users que hayan sido creados
    >>> #   por el usuario con la ID 2
    >>> ctx.search('base.users', [('create_uid', '=', 2)])
    >>> # [3, 5, 6]

    ### Lectura de registros
    Este método retorna una lista de diccionarios con el contenido de los registros
    de un modelo de la base de datos a partir de una lista de IDs, en el orden en
    el que se especificaron los campos o todos los campos en caso de no haber sido
    especificados.

    Uso:
    >>> # Ejemplo 1
    >>> ctx.read('base.users', [2])
    >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
    >>> 
    >>> # Ejemplo 2
    >>> ctx.read('base.users', [2, 3])
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> # ]
    >>> 
    >>> # Ejemplo 3
    >>> ctx.read('base.users', [2, 3], ['login', 'create_date'])
    >>> # [
    >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
    >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
    >>> # ]

    ### Búsqueda y lectura de registros
    Este método retorna una lista de diccionarios con el contenido de los registros
    de un modelo de la base de datos, en el orden en el que se especificaron los
    campos o todos los campos en caso de no haber sido especificados.

    Uso:
    >>> # Ejemplo 1
    >>> ctx.search_read('base.users')
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> #   ...
    >>> # ]
    >>> 
    >>> # Ejemplo 2
    >>> ctx.search_read('base.users', [('user', '=', 'onnymm')])
    >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
    >>> 
    >>> # Ejemplo 3
    >>> ctx.search_read('base.users', fields= ['user', 'create_date'])
    >>> # [
    >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
    >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
    >>> #   ...
    >>> # ]

    ### Conteo de búsqueda
    Este método retorna el conteo de de todos los registros de un modelo o los
    registros que cumplan con la condición de búsqueda provista, ideal para
    funcionalidades de paginación que muestran un total de registros.

    Uso:
    >>> # Ejemplo 1
    >>> ctx.search_count('base.users')
    >>> # 5
    >>> 
    >>> # Ejemplo 2
    >>> ctx.search_count('base.permissions', [('create_uid', '=', 5)])
    >>> # 126

    ### Actualización de registros
    Este método realiza la actualización de uno o más registros a partir de su
    respectiva ID provista, actualizando uno o más campos con el valor provisto.
    Este método solo sobreescribe un mismo valor por cada campo a todos los
    registros provistos.

    Uso:
    >>> ctx.search_read('base.users', fields= ['login', 'name'])
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii'},
    >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim'},
    >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio'},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
    >>> #   ...
    >>> # ]
    >>> 
    >>> # Modificación
    >>> ctx.update('base.users', [3, 4, 5], {'name': 'Cambiado'})
    >>> # True
    >>> 
    >>> ctx.search_read('base.users', fields= ['login', 'name'])
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
    >>> #   {'id': 3, 'name': 'Cambiado', 'login': 'lumii'},
    >>> #   {'id': 4, 'name': 'Cambiado', 'login': 'meshkim'},
    >>> #   {'id': 5, 'name': 'Cambiado', 'login': 'luunafio'},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
    >>> #   ...
    >>> # ]

    >>> ctx.search_read('base.users')
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
    >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
    >>> #   ...
    >>> # ]
    >>> 
    >>> # Eliminación del registro con ID 2
    >>> 
    >>> ctx.delete('base.users', 2)
    >>> # True
    >>> 
    >>> ctx.search_read('base.users')
    >>> # [
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
    >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
    >>> #   ...
    >>> # ]

    ### Obtención de ID de recurso
    Este método se usa para obtener la ID de un registro en la base de datos
    señalado por su referencia única de mapeo.

    >>> ctx.get_resource_id('base_users.root_user')
    >>> # 1

    ### Ejecución de una acción
    Este método ejecuta una acción sobre un registro de un modelo en la base de
    datos.

    Ejemplo:
    >>> ctx.action('base.users', 'archive', 3)
    >>> # True

    En el fragmento de código ejecutamos una acción que archiva al registro con ID
    `3` del modelo `base.users`.

    ### Ejecución de tarea de servidor
    Este método ejecuta una tarea de servidor en la base de datos.

    Ejemplo:
    >>> ctx.task('update_data_from_api')
    >>> # True
    """

    records: list[_R]
    """
    ### Registros
    Lista de registros sobre los que se ejecuta la automatización.
    """

    def __init__(
        self,
        records: list[_R],
        execution_ctx: ExecutionContext[_M],
        crud: CRUD[_M],
        ddl: DDL[_M]
    ) -> None:

        # Asignación de valores
        self.records = records
        self._execution_ctx = execution_ctx
        self._crud = crud
        self._ddl = ddl

        # Inicialización de índice de datos de modelo
        self._model_data_index = ModelDataIndex(execution_ctx.conn)

    def register_model(
        self,
        model_name: ModelName[_M],
    ) -> None:

        # Se añade el modelo en los motores
        self._execution_ctx.automations.add(model_name)
        self._execution_ctx.compute.add(model_name)
        self._execution_ctx.validations.add(model_name)
        self._execution_ctx.actions.add(model_name)
        self._execution_ctx.policies.add(model_name)
