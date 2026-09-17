from typing import Any
from typing import Generic
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from ..._resources import ModelDataIndex
from ..._typing.generics import ItemOrList
from ..._typing.generics import MaybeNone
from ..._typing.generics import ModelName
from ..._typing.generics import _Record
from ..._typing.structures import CriteriaStructure
from ..._typing.structures import RecordData
from ..._typing.structures import NotificationTarget
from ..._typing.structures import FieldReadDeclaration
from ..._typing.type_parameters import _M

if TYPE_CHECKING:
    from ..._contexts import ExecutionContext
    from ..._orchestrator import CRUD

class BaseContext(Generic[_M]):
    _crud: CRUD[_M]
    _execution_ctx: ExecutionContext[_M]
    _model_data_index: ModelDataIndex

    @property
    def uid(
        self,
    ) -> int:
        """
        ID del usuario que ejecuta la transacción.
        """

        # Obtención de la ID del usuario en la ejecución
        uid = self._execution_ctx.uid

        return uid

    def create(
        self,
        model_name: ModelName[_M],
        data: ItemOrList[RecordData],
    ) -> list[int]:
        """
        ## Creación de uno o muchos registros
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

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :data: Diccionario o lista de diccionarios de los
        datos a crear.

        **Retorna**

        :record_ids: Lista de IDs del registro o de los registros creados.
        """

        # Creación de registros y obtención de sus IDs
        created_ids = self._crud.create(
            self._execution_ctx,
            model_name,
            data,
        )

        return created_ids

    def search(
        self,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[int]:
        """
        ## Búsqueda de registros
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

        ### Criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una
        condición, se deben unir por operadores lógicos `AND` u `OR`. Siendo el
        operador lógico el que toma la primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos. La estructura de una tripleta consiste en 3
        diferentes parámetros:
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

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        #### Operador de comparación

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

        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado
        por éste. Suponiendo que una búsqueda normal arrojaría los siguientes
        resultados:
        >>> ctx.search('base.users')
        >>> # [1, 2, 3, 4, 5, 6, 7]

        Se puede especificar que el retorno de los registros considerará solo a partir
        desde cierto desfase numérico, como por ejemplo lo siguiente:
        >>> ctx.search('base.users', offset= 2)
        >>> # [3, 4, 5, 6, 7]

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de
        datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
        >>> ctx.search('base.users')
        >>> # [1, 2, 3, 4, 5, 6, 7]

        Se puede especificar que solo se requiere obtener una cantidad máxima de
        registros a partir de un número provisto:
        >>> ctx.search('base.users', limit= 3)
        >>> # [1, 2, 3]

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :search_criteria: Criterio de búsqueda.
        :offset: Desfase de resultados retornados.
        :limit: Límite de cantidad de resultados retornados.

        **Retorna**

        :record_ids: Lista de IDs del registro o de los registros creados.
        """

        # Búsqueda de registros
        record_ids = self._crud.search(
            self._execution_ctx,
            model_name,
            search_criteria,
            offset,
            limit,
        )

        return record_ids

    def read(
        self,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        fields: list[FieldReadDeclaration] = [],
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None
    ) -> list[_Record]:
        """
        ## Lectura de registros
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

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :record_ids: ID o lista de IDs de los registros a leer.
        :fields: Declaración de campos a leer.
        :sortby: Nombre o nombres de campo a usar para ordenar los registros.
        :ascending: Dirección de ordenamiento, ascendente (*True*) o descendente
        (*False*).

        **Retorna**

        :records: Lista de diccionarios con los datos de los registros solicitados.
        """

        # Obtención de los datos
        records_data = self._crud.read(
            self._execution_ctx,
            model_name,
            record_ids,
            fields,
            sortby,
            ascending,
        )

        return records_data

    def search_read(
        self,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        fields: list[FieldReadDeclaration] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None,
    ) -> list[_Record]:
        """
        ## Búsqueda y lectura de registros
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

        ### Criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una
        condición, se deben unir por operadores lógicos `AND` u `OR`. Siendo el
        operador lógico el que toma la primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos. La estructura de una tripleta consiste en 3
        diferentes parámetros:
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

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        #### Operador de comparación

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

        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado
        por éste. Suponiendo que una búsqueda normal arrojaría los siguientes
        resultados:
        >>> ctx.search_read('base.users')
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
        >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
        >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
        >>> #   ...
        >>> # ]

        Se puede especificar que el retorno de los registros considerará solo a partir
        desde cierto registro, como por ejemplo lo siguiente:
        >>> ctx.search_read('base.users', offset= 2)
        >>> # [
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
        >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
        >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
        >>> #   {'id': 7, 'name': 'Sarko Zuimx', 'login': 'sarzu', ...},
        >>> #   {'id': 8, 'name': 'Leo Minnix', 'login': 'minnleo', ...},
        >>> #   ...
        >>> # ]

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de
        datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
        >>> ctx.search_read('base.users')
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
        >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
        >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
        >>> #   ...
        >>> # ]

        Se puede especificar que solo se requiere obtener una cantidad máxima de
        registros a partir de un número provisto:
        >>> ctx.search_read('base.users', limit= 3)
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...}
        >>> # ]

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :search_criteria: Criterio de búsqueda.
        :fields: Declaración de campos a leer.
        :offset: Desfase de resultados retornados.
        :limit: Límite de cantidad de resultados retornados.
        :sortby: Nombre o nombres de campo a usar para ordenar los registros.
        :ascending: Dirección de ordenamiento, ascendente (*True*) o descendente
        (*False*).

        **Retorna**

        :records: Lista de diccionarios con los datos de los registros solicitados.
        """

        # Obtención de los datos
        records_data = self._crud.search_read(
            self._execution_ctx,
            model_name,
            search_criteria,
            fields,
            offset,
            limit,
            sortby,
            ascending,
        )

        return records_data

    def search_count(
        self,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
    ) -> int:
        """
        ## Conteo de búsqueda
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

        ### Criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una
        condición, se deben unir por operadores lógicos `AND` u `OR`. Siendo el
        operador lógico el que toma la primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos. La estructura de una tripleta consiste en 3
        diferentes parámetros:
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

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        #### Operador de comparación

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
        - `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y
        minúsculas)

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :search_criteria: Criterio de búsqueda.

        **Retorna**

        :count: Total de registros encontrados.
        """

        # Obtención del conteo de resultados
        count = self._crud.search_count(
            self._execution_ctx,
            model_name,
            search_criteria,
        )

        return count

    def update(
        self,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        data: RecordData,
    ) -> Literal[True]:
        """
        ## Actualización de registros
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

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :record_ids: ID o lista de IDs de los registros a actualizar.
        :data: Diccionario o lista de diccionarios de los datos a crear.

        **Retorna**

        :response: Respuesta de que la operación se realizó correctamente.
        """

        # Modificación de los registros
        result = self._crud.update(
            self._execution_ctx,
            model_name,
            record_ids,
            data,
        )

        return result

    def delete(
        self,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
    ) -> Literal[True]:
        """
        ## Eliminación de registros
        Este método realiza la eliminaciónd e uno o más registros de la base de datos a
        partir de su respectiva ID provista.

        Uso:
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

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :record_ids: ID o lista de IDs de los registros a eliminar.

        **Retorna**

        :response: Respuesta de que la operación se realizó correctamente.
        """

        # Eliminación de los registros
        result = self._crud.delete(
            self._execution_ctx,
            model_name,
            record_ids,
        )

        return result

    def action(
        self,
        model_name: ModelName[_M],
        name: str,
        record_id: int,
    ) -> Literal[True]:
        """
        ## Ejecución de una acción
        Este método ejecuta una acción sobre un registro de un modelo en la base de
        datos.

        Ejemplo:
        >>> ctx.action('base.users', 'archive', 3)
        >>> # True

        En el fragmento de código ejecutamos una acción que archiva al registro con ID
        `3` del modelo `base.users`.

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :name: Nombre de la acción.
        :record_id: ID del registro sobre el que se va a ejecutar la acción.

        **Retorno**

        :response: Respuesta de que la operación se realizó correctamente.
        """

        # Ejecución de acción
        result = self._execution_ctx.actions.execute(
            self._execution_ctx,
            model_name,
            name,
            record_id,
        )

        return result

    def task(
        self,
        name: str,
    ) -> Literal[True]:

        # Ejecución de tarea de servidor
        result = self._execution_ctx.server_tasks.execute(
            self._execution_ctx,
            name,
        )

        return result

    def get_resource_id(
        self,
        ref: str,
    ) -> MaybeNone[int]:
        """
        ## Obtención de ID de recurso
        Este método se usa para obtener la ID de un registro en la base de datos
        señalado por su referencia única de mapeo.

        >>> ctx.get_resource_id('base_users.root_user')
        >>> # 1

        **Parámetros**

        :ref: Referencia única de mapeo de datos.

        **Retorno**

        :record_id: `MaybeNone[int]` ID del registro referenciado o *None* si no existe.
        """

        # Obtención de la ID de recurso
        resource_id = self._model_data_index.get_resource_id(ref)

        return resource_id

    def notify(
        self,
        event: str,
        target: NotificationTarget,
        payload: dict[str, Any] = {}
    ) -> None:

        # Notificación usando el contexto de ejecución
        self._execution_ctx._notify(event, target, payload)
