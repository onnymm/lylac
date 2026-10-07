from typing import Any
from typing import Generic
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from ..._resources import ModelDataIndex
from ..._typing.generics import ScalarOrIterable
from ..._typing.generics import MaybeNone
from ..._typing.generics import ModelName
from ..._typing.generics import _Record
from ..._typing.structures import CriteriaStructure
from ..._typing.structures import InputRecordData
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
        data: ScalarOrIterable[InputRecordData[_M]],
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
        >>> 
        >>> # Podemos crear o añadir registros referenciados directamente
        >>> #    con un comando de relación
        >>> ctx.create(
        >>>     'base.users',
        >>>     {
        >>>         'login': 'onnymm',
        >>>         'name': 'Onnymm Azzur',
        >>>         # Campo de tipo [many2many]
        >>>         'role_ids': {
        >>>             # Comando de relación de creación
        >>>             'create': {
        >>>                 'name': 'command_admin',
        >>>                 'label': 'Administrador de comandos',
        >>>                 ...
        >>>             },
        >>>             # Comando de relación de adición
        >>>             'add': {
        >>>                 'add': [1, 2, 3] # Registros que ya existen
        >>>             },
        >>>         },
        >>>     },
        >>> )

        Se pueden proporcionar también funciones de resolución de valor:
        >>> ctx.create(
        >>>     'base.model.field',
        >>>     {
        >>>         'name': 'hire_date',
        >>>         'label': 'Fecha de contrato',
        >>>         'ttype': 'date',
        >>>         # Función de resolución para asignar una ID
        >>>         'model_id': lambda ctx: ctx.get_resource_id('base_model.hr_employee'),
        >>>     },
        >>> )

        Antes de que el registro sea ingresado para ser creado en la base de datos, la
        función de resolución de valor es ejecutada usando un contexto de resolución de
        valor. La ID del modelo se obtiene, se reemplaza la función por el valor y
        entonces el registro es enviado para ser creado:
        >>> {
        >>>     'name': 'hire_date',
        >>>     'label': 'Fecha de contrato',
        >>>     'ttype': 'date',
        >>>     'model_id': 27,
        >>> }

        `i` Para este caso también podríamos modificar directamente el registro del
        modelo `hr.employee` (Si contamos con la ID) y modificar el campo de
        `field_ids` usando un *Comando de Relación* de creación proporcionando los
        datos del campo a crear.

        Los valores para cada valor pueden ser cualquiera de:
        - `DMLScalarCompatible` — Tipo de dato que se puede usar como valor para un
        campo de modelo. El tipo de dato puede ser:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `datetime.date`
            - `datetime.datetime`
            - `datetime.time`
            - `datetime.timedelta`
            - `None`
        - `JSONLike` — Estructura equivalente a JSON. El tipo de dato puede ser escalar
        o iterable de:
            - `JSONLikeScalar` — Representa los tipos:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `None`
            - `JSONLikeObjShape` — Representa un diccionario serializable conformado
        por:
                - Llaves que deben ser de tipo `str`
                - Valores que pueden ser escalar o iterable de:
                    - `JSONLikeScalar`
                    - `JSONLike`
        - `InputRecordData` — Datos para crear un registro vinculado, en campos de tipo
        `many2one`.
        - `RelationCommands` — Comandos de modificación de los registros referenciados
        en campos de tipo `one2many` y `many2many` desde el registro que los
        referencía. Las llaves y valores del diccionario pueden ser:
            - `'create'` — Comando de relación de creación.
            - `'add'` — Comando de relación de adición.
            - `'update'` — Comando de relación de actualización.
            - `'replace'` — Comando de relación de reemplazo.
            - `'unlink'` — Comando de relación de desvinculación.
            - `'delete'` — Comando de relación de eliminación.
            - `'clear'` — Comando de relación de limpieza.
        - `ValueResolutionFn` — Función de resolución de valor que se usa para resolver
        y retornar un valor que se usará en el campo para almacenarse en la base de
        datos.

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :data: Diccionario o iterable de diccionarios de los datos a crear.

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
        search_criteria: CriteriaStructure[_M] = [],
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

        Pueden buscarse registros que cumplan múltiples condiciones:
        >>> ctx.search(
        >>>     'base.users',
        >>>     [
        >>>         # Las siguientes dos condiciones deben cumplirse
        >>>         '&',
        >>>             # La ID del usuario creador es igual a 2
        >>>             ('create_uid.id', '=', 2),
        >>>             # Nombre de inicio de sesión comienza con "as"
        >>>             ('login', 'starts with', 'as'),
        >>>     ]
        >>> )
        >>> # [5]

        Pueden usarse cadenas de atributos en campos de tipo `many2one`:
        >>> ctx.search(
        >>>     # Modelo de eventos de asistencia de empleados
        >>>     'assistance.registry.event',
        >>>     # La ubicación designada del empleado está activa
        >>>     [('employee_id.location_id.active', '=', True)]
        >>> )
        >>> # [3, 4, 5, 6, 7, ...]

        También pueden usarse cómputos de campo:
        >>> # Función de cómputo
        >>> def compute_total(ctx: Lylac.ComputeContext):
        >>>     total = ctx['subtotal'] * (ctx['tax_id.amount'] + 1)
        >>>     return total

        >>> # Cómputo de campo
        >>> line_total = ('total', 'float', compute_total)

        >>> ctx.search(
        >>>     'sale.order.line',
        >>>     # El subtotal más el monto del impuesto es mayor a $150.00
        >>>     [(line_total, '>', 150)],
        >>> )
        >>> # [24, 31, 56, 89, ...]

        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda expresa un conjunto de condiciones que
        se pueden usar para filtrar registros en la base de datos al momento de leer o
        invocar registros para un fin específico.

        La estructura se conforma de un iterable con los tipos:
        - `TripletStructure`: Tupla de 3 posiciones que representa una condición.
        - `LogicOperator`: Operador lógico que une tripletas de condiciones.

        ----

        #### Estructura de tripletas de condición
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

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

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
        record_ids: ScalarOrIterable[int],
        fields: list[FieldReadDeclaration] = [],
        sortby: Optional[ScalarOrIterable[str]] = None,
        ascending: Optional[ScalarOrIterable[bool]] = None
    ) -> list[_Record]:
        """
        ## Lectura de registros
        Este método retorna una lista de diccionarios con el contenido de los registros
        de un modelo de la base de datos a partir de un iterable de IDs, en el orden en
        el que se especificaron los campos o todos los campos en caso de no haber sido
        especificados.

        Uso:
        >>> # Ejemplo 1
        >>> ctx.read('base.users', [2])
        >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
        >>> 
        >>> ctx.read('base.users', [2, 3])
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> # ]
        >>> 
        >>> # Especificación de campos a leer
        >>> ctx.read('base.users', [2, 3], ['login', 'create_date'])
        >>> # [
        >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
        >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
        >>> # ]
        >>> 
        >>> ctx.read(
        >>>     'sale.order',
        >>>     [1, 2, 3],
        >>>     [
        >>>         # Campos existentes en la base de datos
        >>>         'name',
        >>>         'subtotal',
        >>>         'user_id',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'user_id': [2, 'Onnymm Azzur']},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'user_id': [2, 'Usuario Root']},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'user_id': [3, 'Mynx Lumii']},
        >>> # ]

        Se puede acceder a los atributos de los registros referenciados:
        >>> ctx.read(
        >>>     'sale.order',
        >>>     [1, 2, 3],
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Cadena de referencias [many2one]
        >>>         'user_id.active',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'user_id.active': True},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'user_id.active': False},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'user_id.active': True},
        >>> # ]

        Uso de campos con un alias:
        >>> ctx.read(
        >>>     'sale.order',
        >>>     [1, 2, 3],
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Campo con alias
        >>>         ('user_id.active', 'is_user_active'),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'is_user_active': True},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'is_user_active': False},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'is_user_active': True},
        >>> # ]

        Uso de cómputo de campo:
        >>> ctx.read(
        >>>     'sale.order',
        >>>     [1, 2, 3],
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Cómputo de campo
        >>>         ('total', 'float', lambda ctx: ctx['subtotal'] * 1.16),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'total': 272.77},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'total': 281.95},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'total': 1174.15},
        >>> # ]

        Con expansión de campos en campos de tipo `one2many` y `many2many`:
        >>> ctx.read(
        >>>     'sale.order',
        >>>     1,
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Campo [one2many]
        >>>         'line_ids',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [1, 2],
        >>> #     },
        >>> # ]
        >>> ctx.read(
        >>>     'sale.order',
        >>>     1,
        >>>     [
        >>>         ...,
        >>>         (
        >>>             'line_ids',
        >>>             # Campos de los registros de líneas
        >>>             [
        >>>                 'product_id',
        >>>                 'quantity',
        >>>                 'subtotal',
        >>>             ],
        >>>         ),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [
        >>> #             {'id': 1, 'product_id': [13, 'Café sencillo'], 'quantity': 1, 'subtotal': 35.15},
        >>> #             {'id': 2, 'product_id': [2, 'Taza de café'], 'quantity': 1, 'subtotal': 200.00},
        >>> #         ],
        >>> #     },
        >>> # ]

        Se pueden usar múltiples tipos de entrada:
        >>> ctx.read(
        >>>     'sale.order',
        >>>     1,
        >>>     [
        >>>         ...,
        >>>         (
        >>>             'line_ids',
        >>>             # Campos de los registros de líneas
        >>>             [
        >>>                 # Cadena de referencia
        >>>                 'product_id.code',
        >>>                 # Alias
        >>>                 ('quantity', 'qty'),
        >>>                 # Cómputo de campo
        >>>                 ('total', 'float', lambda ctx: ctx['subtotal'] * 1.16),
        >>>             ],
        >>>         ),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [
        >>> #             {'id': 1, 'product_id.code': '00COFFEE', 'qty': 1, 'subtotal': 40.77},
        >>> #             {'id': 2, 'product_id.code': 'CUP-BK', 'qty': 1, 'subtotal': 232.00},
        >>> #         ],
        >>> #     },
        >>> # ]

        Alias a la expansión de campos:
        >>> ctx.read(
        >>>     'sale.order',
        >>>     1,
        >>>     [
        >>>         ...,
        >>>         (
        >>>             # Expansión de campos
        >>>             (
        >>>                 'line_ids',
        >>>                 [
        >>>                     'product_id.code',
        >>>                     ...,
        >>>                 ],
        >>>             ),
        >>>             # Asignación de alias
        >>>             'detail',
        >>>         )
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'detail': [
        >>> #             {'id': 1, 'product_id.code': '00COFFEE', 'qty': 1, 'subtotal': 40.77},
        >>> #             {'id': 2, 'product_id.code': 'CUP-BK', 'qty': 1, 'subtotal': 232.00},
        >>> #         ],
        >>> #     },
        >>> # ]

        **Parámetros**

        :model_name: Nombre de modelo en la base de datos.
        :record_ids: ID o iterable de IDs de los registros a leer.
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
        search_criteria: CriteriaStructure[_M] = [],
        fields: list[FieldReadDeclaration] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ScalarOrIterable[str]] = None,
        ascending: Optional[ScalarOrIterable[bool]] = None,
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

        Pueden buscarse registros que cumplan múltiples condiciones:
        >>> ctx.search_read(
        >>>     'base.users',
        >>>     [
        >>>         # Las siguientes dos condiciones deben cumplirse
        >>>         '&',
        >>>             # La ID del usuario creador es igual a 2
        >>>             ('create_uid.id', '=', 2),
        >>>             # Nombre de inicio de sesión comienza con "as"
        >>>             ('login', 'starts with', 'as'),
        >>>     ]
        >>> )
        >>> # [...]

        Pueden usarse cadenas de atributos en campos de tipo `many2one`:
        >>> ctx.search_read(
        >>>     # Modelo de eventos de asistencia de empleados
        >>>     'assistance.registry.event',
        >>>     # La ubicación designada del empleado está activa
        >>>     [('employee_id.location_id.active', '=', True)]
        >>> )
        >>> # [...]

        También pueden usarse cómputos de campo:
        >>> # Función de cómputo
        >>> def compute_total(ctx: Lylac.ComputeContext):
        >>>     total = ctx['subtotal'] * (ctx['tax_id.amount'] + 1)
        >>>     return total
        >>> 
        >>> # Cómputo de campo
        >>> line_total = ('total', 'float', compute_total)
        >>> 
        >>> ctx.search_read(
        >>>     'sale.order.line',
        >>>     # El subtotal más el monto del impuesto es mayor a $150.00
        >>>     [(line_total, '>', 150)],
        >>> )
        >>> # [...]

        Para lectura de campos:
        >>> ctx.search_read(
        >>>     'sale.order',
        >>>     [
        >>>         # Campos existentes en la base de datos
        >>>         'name',
        >>>         'subtotal',
        >>>         'user_id',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'user_id': [2, 'Onnymm Azzur']},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'user_id': [2, 'Usuario Root']},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'user_id': [3, 'Mynx Lumii']},
        >>> #     ...,
        >>> # ]

        Se puede acceder a los atributos de los registros referenciados:
        >>> ctx.search_read(
        >>>     'sale.order',
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Cadena de referencias [many2one]
        >>>         'user_id.active',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'user_id.active': True},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'user_id.active': False},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'user_id.active': True},
        >>> #     ...
        >>> # ]

        Uso de campos con un alias:
        >>> ctx.search_read(
        >>>     'sale.order',
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Campo con alias
        >>>         ('user_id.active', 'is_user_active'),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'is_user_active': True},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'is_user_active': False},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'is_user_active': True},
        >>> #     ...,
        >>> # ]

        Uso de cómputo de campo:
        >>> ctx.search_read(
        >>>     'sale.order',
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Cómputo de campo
        >>>         ('total', 'float', lambda ctx: ctx['subtotal'] * 1.16),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'total': 272.77},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'total': 281.95},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'total': 1174.15},
        >>> #     ...,
        >>> # ]

        Con expansión de campos en campos de tipo `one2many` y `many2many`:
        >>> ctx.search_read(
        >>>     'sale.order',
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Campo [one2many]
        >>>         'line_ids',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [1, 2],
        >>> #     },
        >>> #     ...,
        >>> # ]
        >>> ctx.search_read(
        >>>     'sale.order',
        >>>     [
        >>>         ...,
        >>>         (
        >>>             'line_ids',
        >>>             # Campos de los registros de líneas
        >>>             [
        >>>                 'product_id',
        >>>                 'quantity',
        >>>                 'subtotal',
        >>>             ],
        >>>         ),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [
        >>> #             {'id': 1, 'product_id': [13, 'Café sencillo'], 'quantity': 1, 'subtotal': 35.15},
        >>> #             {'id': 2, 'product_id': [2, 'Taza de café'], 'quantity': 1, 'subtotal': 200.00},
        >>> #         ],
        >>> #     },
        >>> #     ...,
        >>> # ]

        Se pueden usar múltiples tipos de entrada:
        >>> ctx.search_read(
        >>>     'sale.order',
        >>>     [
        >>>         ...,
        >>>         (
        >>>             'line_ids',
        >>>             # Campos de los registros de líneas
        >>>             [
        >>>                 # Cadena de referencia
        >>>                 'product_id.code',
        >>>                 # Alias
        >>>                 ('quantity', 'qty'),
        >>>                 # Cómputo de campo
        >>>                 ('total', 'float', lambda ctx: ctx['subtotal'] * 1.16),
        >>>             ],
        >>>         ),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [
        >>> #             {'id': 1, 'product_id.code': '00COFFEE', 'qty': 1, 'subtotal': 40.77},
        >>> #             {'id': 2, 'product_id.code': 'CUP-BK', 'qty': 1, 'subtotal': 232.00},
        >>> #         ],
        >>> #     },
        >>> #     ...,
        >>> # ]

        Alias a la expansión de campos:
        >>> ctx.search_read(
        >>>     'sale.order',
        >>>     [
        >>>         ...,
        >>>         (
        >>>             # Expansión de campos
        >>>             (
        >>>                 'line_ids',
        >>>                 [
        >>>                     'product_id.code',
        >>>                     ...,
        >>>                 ],
        >>>             ),
        >>>             # Asignación de alias
        >>>             'detail',
        >>>         )
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'detail': [
        >>> #             {'id': 1, 'product_id.code': '00COFFEE', 'qty': 1, 'subtotal': 40.77},
        >>> #             {'id': 2, 'product_id.code': 'CUP-BK', 'qty': 1, 'subtotal': 232.00},
        >>> #         ],
        >>> #     },
        >>> #     ...,
        >>> # ]

        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda expresa un conjunto de condiciones que
        se pueden usar para filtrar registros en la base de datos al momento de leer o
        invocar registros para un fin específico.

        La estructura se conforma de un iterable con los tipos:
        - `TripletStructure`: Tupla de 3 posiciones que representa una condición.
        - `LogicOperator`: Operador lógico que une tripletas de condiciones.

        ----

        #### Estructura de tripletas de condición
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

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

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
        search_criteria: CriteriaStructure[_M] = [],
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

        Pueden buscarse registros que cumplan múltiples condiciones:
        >>> ctx.search(
        >>>     'base.users',
        >>>     [
        >>>         # Las siguientes dos condiciones deben cumplirse
        >>>         '&',
        >>>             # La ID del usuario creador es igual a 2
        >>>             ('create_uid.id', '=', 2),
        >>>             # Nombre de inicio de sesión comienza con "as"
        >>>             ('login', 'starts with', 'as'),
        >>>     ]
        >>> )
        >>> # 2

        Pueden usarse cadenas de atributos en campos de tipo `many2one`:
        >>> ctx.search(
        >>>     # Modelo de eventos de asistencia de empleados
        >>>     'assistance.registry.event',
        >>>     # La ubicación designada del empleado está activa
        >>>     [('employee_id.location_id.active', '=', True)]
        >>> )
        >>> # 136

        También pueden usarse cómputos de campo:
        >>> # Función de cómputo
        >>> def compute_total(ctx: Lylac.ComputeContext):
        >>>     total = ctx['subtotal'] * (ctx['tax_id.amount'] + 1)
        >>>     return total
        >>> 
        >>> # Cómputo de campo
        >>> line_total = ('total', 'float', compute_total)
        >>> 
        >>> ctx.search(
        >>>     'sale.order.line',
        >>>     # El subtotal más el monto del impuesto es mayor a $150.00
        >>>     [(line_total, '>', 150)],
        >>> )
        >>> # 215

        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda expresa un conjunto de condiciones que
        se pueden usar para filtrar registros en la base de datos al momento de leer o
        invocar registros para un fin específico.

        La estructura se conforma de un iterable con los tipos:
        - `TripletStructure`: Tupla de 3 posiciones que representa una condición.
        - `LogicOperator`: Operador lógico que une tripletas de condiciones.

        ----

        #### Estructura de tripletas de condición
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

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

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
        record_ids: ScalarOrIterable[int],
        data: InputRecordData[_M],
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
        :record_ids: ID o iterable de IDs de los registros a actualizar.
        :data: Diccionario o iterable de diccionarios de los datos a crear.

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
        record_ids: ScalarOrIterable[int],
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
        :record_ids: ID o iterable de IDs de los registros a eliminar.

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
        """
        ## Ejecución de tarea de servidor
        Este método ejecuta una tarea de servidor en la base de datos.

        Ejemplo:
        >>> ctx.task('update_data_from_api')
        >>> # True

        **Parámetros**

        :name: Nombre de la tarea de servidor.

        **Retorno**

        :response: Respuesta de que la operación se realizó correctamente.
        """

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
