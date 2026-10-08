from typing import Any
from typing import Generic
from typing import TYPE_CHECKING
from .._contexts.engines import BaseContext
from .._resources import ErrorDetail
from .._resources import ModelDataIndex
from .._typing.generics import ModelName
from .._typing.generics import _Record
from .._typing.structures import CriteriaStructure
from .._typing.structures import TripletStructure
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R

if TYPE_CHECKING:
    from .._contexts import ExecutionContext
    from .._orchestrator import CRUD

class ValidationContext(Generic[_M, _R], BaseContext[_M]):
    """
    ## Contexto de validación
    La clase de contexto de validación es usada como argumento en las funciones de
    validación y hereda todas las propiedades de la clase `BaseContext`.

    ### Datos del registro
    Atributo por el cual se puede acceder a los datos del registro sobre el que se
    ejecuta una validación. Estos datos están definidos por el parámetro `fields`
    al registrar la validación.

    Uso:
    >>> ctx.data
    >>> # {'id': 3, 'name': ...}

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
    de un modelo de la base de datos a partir de un iterable de IDs, en el orden en
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
    model_name: ModelName[_M]
    """
    Nombre de modelo sobre el que se ejecuta la validación.
    """
    records: list[_R]
    """
    Registros sobre los que se ejecuta la validación.
    """

    def __init__(
        self,
        execution_ctx: ExecutionContext[_M],
        crud: CRUD[_M],
        model_name: ModelName[_M],
        records: list[_R],
        errors: list[ErrorDetail],
        message: str,
    ) -> None:

        # Asignación de valores
        self.model_name = model_name
        self.records = records
        self._crud = crud
        self._message = message
        self._errors = errors
        self._execution_ctx = execution_ctx

        # Inicialización de índice de datos de modelo
        self._model_data_index = ModelDataIndex(execution_ctx.conn)

    def catch(
        self,
        record: _R,
        value: Any = None,
        # data: list[Any] = [],
    ) -> None:

        # Construcción de mensaje a mostrar
        message_to_show = self._message.format(value= value)
        # Inicialización de detalle de error
        detail = ErrorDetail(value, record, message_to_show)
        # Se añade el registro como error
        self._errors.append(detail)

    def find_duplicated_composite_keys(
        self,
        records: list[_Record],
        field_names_composite_key: list[str],
    ) -> list[_Record]:

        # Inicialización de lista de registros duplicados
        found_records: list[_Record] = []

        # Mientras la longitud de datos sea mayor a 0...
        while len(records) > 0:
            # Obtención de un registro i
            record_i = records.pop()
            # Indicadores de duplicidad
            duplicated_in_input = False
            duplicated_in_model = False
            # Iteración por por el resto de registros
            for record_j in records:

                # Indicador de duplicidad en comparación
                duplicated_in_input_i = True
                # Iteración por cada nombre de campo que forma la llave compuesta
                for field_name in field_names_composite_key:
                    # Si los valores de ambos registros son diferentes...
                    if record_i[field_name] != record_j[field_name]:
                        # Se apaga el indicador de duplicidad 
                        duplicated_in_input_i = False
                        # Se termina el ciclo
                        break

                # Si el indicador de duplicidad en comparación no se apagó...
                if duplicated_in_input_i:
                    # Se indica que el registro es duplicado
                    duplicated_in_input = True
                    # Se rompe el ciclo para no sobreescribir el valor en falso
                    break

            # Inicialización de criterio de búsqueda
            search_criteria: CriteriaStructure[_M] = []
            # Iteración por cada nombre de campo que forma la llave compuesta
            for field_name in field_names_composite_key:
                # Construcción de condición como tripleta
                condition: TripletStructure = (field_name, '=', record_i[field_name])
                # Si la longitud del criterio de búsqueda es 0...
                if len(search_criteria) == 0:
                    # Se añade la tripleta
                    search_criteria.append(condition)
                # Si la longitud del criterio de búsqueda no es 0...
                else:
                    # Se añade la tripleta en forma de AND
                    search_criteria = ['&', *search_criteria, condition]

            # Búsqueda de cantidad de registros que cumplen con las condiciones provistas
            count = self._crud.search_count(
                self._execution_ctx,
                self.model_name,
                search_criteria,
            )

            # Si fueron encontrados resultados...
            if count:
                # Se enciende el indicador de duplicado en modelo
                duplicated_in_model = True
            # Si algún indicador de duplicidad está encendido...
            if duplicated_in_input or duplicated_in_model:
                # Se añade el registro a los registros duplicados encontrados
                found_records.append(record_i)

        return found_records
