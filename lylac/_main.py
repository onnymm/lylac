from typing import (
    Callable,
    Literal,
)
import pandas as pd
from sqlalchemy import (
    select,
    delete,
    asc,
    update,
    insert,
    func,
)
from ._core import _BaseLylac
from ._models import _Base
from ._module_types import (
    _T,
    CriteriaStructure,
    DBCredentials,
    DataPerRecord,
    RecordData,
    OutputOptions,
    Transaction,
    RecordValue,
)
from ._modules import (
    Automations,
    Connection,
    DDLManager,
    Models,
    Output,
    Structure,
    Query,
    Where,
)

class Lylac(_BaseLylac):

    def __init__(
        self,
        # base: DeclarativeBase,
        credentials: Literal['env'] | DBCredentials | str = 'env',
        output_format: OutputOptions | None = None,
    ) -> None:

        # Asignación del modelo base
        self._base = _Base

        # Inicialización del módulo de manejo de formato de salida
        self._output = Output(self, output_format)

        # Creación de la instancia de conexión con la base de datos
        self._connection = Connection(self, credentials)

        # Inicialización de submódulos
        self._strc = Structure(self)
        self._ddl = DDLManager(self)
        self._models = Models(self)
        self._where = Where(self)
        self._query = Query(self)
        self._automations = Automations(self)

        # Registro de las automatizaciones predeterminadas
        self._automations.create_preset_automations()

    def register_automation(
        self,
        table_name: str,
        transation: Transaction,
        fields: list[str] = ['id'],
        execute_if: CriteriaStructure = [],
        execution: Literal['record', 'all'] = 'record',
    ):
        """
        ## Registro de automatización
        Este decorador permite registrar una automatización en la instancia del
        módulo.
        Ejemplo de uso:
        >>> @lylac.register_automation(
        >>>     # Tabla donde se ejecutará la automatización
        >>>     'my.table',
        >>>     # La automatización se ejecuta tras crearse un registro
        >>>     'create',
        >>> )
        >>> def do_something(params) -> None:
        >>>     print(f'Se creó un registro con ID {params.id}')

        Automatización más específica:
        >>> @lylac.register_automation(
        >>>     # Tabla donde se ejecutará la automatización
        >>>     'my.table',
        >>>     # La automatización se ejecuta tras crearse un registro
        >>>     'create',
        >>>     # Campos a utilizar en la automatización
        >>>     ['id', 'name', 'value'],
        >>>     # Criterios a cumplir para que la automatización se ejecute
        >>>     [('value', '=', 'some_value')],
        >>>     # Tipo de ejecución
        >>>     'record',
        >>> )
        >>> def do_something(params) -> None:
        >>>     print(f'Se creó un registro con ID {params.id}')
        >>>     print(f'El nuevo registro tiene el nombre {params.record_data["name"]}')
        >>>     print(f'El valor del nuevo registro es {params.record_data["value"]})

        ### Tipado dinámico
        Puede utilizarse tipado dedicado para mejorar el flujo de desarrollo de la
        función a registrar en el decorador. Se utilizan tipos de dato nativos de
        Python.
        Ejemplo:
        >>> from lylac.params import BaseRecord, DataPerRecord
        >>> 
        >>> class MyTable(BaseRecord):
        >>>     value: str
        >>>     sync: bool
        >>> 
        >>> @lylac.register_automation(...)
        >>> def do_something(params: DataPerRecord[MyTable]) -> None:
        >>>     ...

        De esta manera el editor de código realizará el autocompletado al acceder a
        las llaves de la información.

        ### Nota:
        En el argumento `fields` se debe especificar qué campos se van a utilizar
        en la lectura del registro dentro de la automatización. Esto es
        indispensable para reducir las cargas de información solicitadas a la base
        de datos.
        """

        # Creación del decorador que registrará la automatización
        def decorator(new_automation: Callable[[DataPerRecord[_T]], None]):

            # Creación de la función envuelta a retornar por el decorador
            def wraper(params: DataPerRecord[_T]) -> None:

                # Ejecución de la automatización provista
                return new_automation(params)

            # Registro de la automatización en la estructura central
            self._automations.register_automation(
                table_name,
                transation,
                wraper,
                execute_if,
                fields,
                execution,
            )

            return wraper

        # Retorno del decorador
        return decorator

    def create(
        self,
        table_name: str,
        data: RecordData | list[RecordData],
    ) -> list[int]:
        """
        ## Creación de registros
        Este método realiza la creación de uno o muchos registros a partir del
        nombre de la tabla proporcionado y un diccionario (un único registro) o
        una lista de diccionarios (muchos registros).

        Uso:
        >>> # Para un solo registro
        >>> record = {
        >>>     'user': 'onnymm',
        >>>     'name': 'Onnymm Azzur',
        >>> }
        >>> 
        >>> db.create('users', record)
        >>> #    id    user          name
        >>> # 0   2  onnymm  Onnymm Azzur
        >>> 
        >>> # Para muchos registros
        >>> records = [
        >>>     {
        >>>         'user': 'onnymm',
        >>>         'name': 'Onnymm Azzur',
        >>>     },
        >>>     {
        >>>         'user': 'lumii',
        >>>         'name': 'Lumii Mynx',
        >>>     },
        >>> ]
        >>> 
        >>> db.create('users', records)
        >>> #    id    user          name
        >>> # 0   2  onnymm  Onnymm Azzur
        >>> # 1   3   lumii    Lumii Mynx
        """

        # Obtención de la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Conversión de datos entrantes si es necesaria
        if isinstance(data, dict):
            data = [data,]

        # Creación de comandos SQL
        stmt = (
            insert(table_model)
            .returning(self._models.get_id_field(table_model))
            .values(data)
        )

        # Ejecución de la transacción
        response = self._connection.execute(stmt, commit= True)

        # Obtención de las IDs creadas
        inserted_records: list[int] = [getattr(row, 'id') for row in response]

        # Ejecución de las automatizaciones correspondientes
        self._automations.run_after_transaction(
            table_name,
            'create',
            inserted_records,
        )

        # Retorno de las IDs creadas
        return inserted_records

    def search(
        self,
        table_name: str,
        search_criteria: CriteriaStructure = [],
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[int]:
        """
        ## Búsqueda de registros
        Este método retorna todos los registros de una tabla o los registros que cumplan
        con la condición de búsqueda provista, además de segmentar desde un índice
        inicial de desfase y/o un límite de cantidad de registros retornada.

        Uso:
        >>> # Ejemplo 1
        >>> db.search('users')
        >>> # [1, 2, 3, 4, 5]
        >>> 
        >>> # Ejemplo 2
        >>> db.search('commisions', [('user_id', '=', 213)])
        >>> # [7, 9, 12, 13, 17, 21, ...]

        ### Los parámetros de entrada son:
        - `table_name`: Nombre de la tabla de donde se tomarán los registros.
        - `search_criteria`: Criterio de búsqueda para retornar únicamente los resultados que
        cumplan con las condiciones provistas (Consultar estructura más abajo).
        - `offset`: Desfase de inicio de primer registro a mostrar.
        - `limit`: Límite de registros retornados por la base de datos.

        ----
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

        ----
        ### Criterios de búsqueda muy específicos
        También es posible formular criterios de búsqueda más avanzados como el que se muestra a
        continuación:
        >>> search_criteria = [
        >>>     '&',
        >>>         '|',
        >>>             ('partner_id', '=', 14418),
        >>>             ('partner_id', '=', 14417),
        >>>         ('salesperson_id', '=', 213)
        >>> ]
        >>> # "partner_id" es igual a 14418 o "partner_id" es igual a 14417 y a su vez "salesperson_id" es igual a 213.
        
        Si el criterio es demasiado largo, también se puede declarar por fuera. También se puede importar
        el tipo de dato `CriteriaStructure` para facilitar la creación apoyandose con el la herramienta de
        autocompletado del editor de código:
        >>> from app.core._types import CriteriaStructure
        >>> search_criteria: CriteriaStructure = ...

        ----
        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que
        una búsqueda normal arrojaría los siguientes resultados:
        >>> db.search('users')
        >>> # [3, 4, 5, 6, 7]

        Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como
        por ejemplo lo siguiente:
        >>> db.search('users', offset= 2)
        >>> # [4, 5, 6, 7]

        ----
        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una
        búsqueda normal arrojaría los siguientes registros:
        >>> db.search('users')
        >>> # [3, 4, 5, 6, 7]

        Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un
        número provisto:
        >>> db.search('users', limit= 3)
        >>> # [3, 4, 5]
        """

        # Obtención de la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Creación del query SELECT
        stmt = select(self._models.get_id_field(table_model))

        # Si hay criterios de búsqueda se genera el 'where'
        if len(search_criteria) > 0:

            # Creación del query where
            where_query = self._where.build_where(table_model, search_criteria)

            # Conversión del query SQL
            stmt = stmt.where(where_query)

        # Ordenamiento de los datos
        stmt = stmt.order_by(asc('id'))

        # Segmentación de inicio y fin en caso de haberlos
        stmt = self._query.build_segmentation(stmt, offset, limit)

        # Ejecución de la transacción
        response = self._connection.execute(stmt)

        # Obtención de las IDs encontradas
        found_ids: list[int] = [getattr(row, 'id') for row in response]

        # Retorno de las IDs encontradas
        return found_ids

    def read(
        self,
        table_name: str,
        record_ids: int | list[int],
        fields: list[str] = [],
        sortby: str | list[str] = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
    ) -> pd.DataFrame | list[dict[str, RecordValue]]:
        """
        ## Lectura de registros
        Este método retorna un DataFrame con el contenido de los registros de
        una tabla de la base de datos a partir de una lista de IDs, en el orden
        en el que se especificaron los campos o todos los campos en caso de no
        haber sido especificados.

        ### Los parámetros de entrada son:
        - `table_name`: Nombre de la tabla de donde se tomarán los registros.
        - `record_ids`: IDs de los respectivos registros a leer.
        - `fields`: Campos a mostrar. En caso de no ser especificado, se toman todos los
        campos de la tabla de la base de datos.
        - `offset`: Desfase de inicio de primer registro a mostrar.
        - `limit`: Límite de registros retornados por la base de datos.

        Uso:
        >>> # Ejemplo 1
        >>> db.search_read('users', [2])
        >>> #    id    user          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> db.search_read('users', [2, 3])
        >>> #    id    user          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> # 1   3   lumii    Lumii Mynx 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 3
        >>> db.search_read('users', [2, 3], ['user', 'create_date'])
        >>> #    id         name         create_date
        >>> # 0   2 Onnymm Azzur 2024-11-04 11:16:59
        >>> # 1   3   Lumii Mynx 2024-11-04 11:16:59
        """

        # Conversión de datos entrantes si es necesaria
        if isinstance(record_ids, int):
            record_ids = [record_ids,]

        # Obtención de la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Obtención de los campos de la tabla
        table_fields = self._models.get_table_fields(table_model, fields)

        # Creación del query base
        stmt = select(*table_fields)

        # Creación del query where
        where_query = self._where.build_where(table_model, [('id', 'in', record_ids)])

        # Conversión del query SQL
        stmt = stmt.where(where_query)

        # Creación de parámetros de ordenamiento
        stmt = self._query.build_sort(
            stmt,
            table_model,
            sortby,
            ascending,
        )

        # Ejecución de la transacción
        response = self._connection.execute(stmt)

        # Inicialización del DataFrame de retorno
        data = pd.DataFrame(response.fetchall())

        # Retorno en formato de salida configurado
        return self._output.build_output(data, table_fields, output_format, 'dataframe')

    def get_value(
        self,
        table_name: str,
        record_id: int,
        field: str,
    ) -> RecordValue:
        """
        ## Obtención de un valor
        Este método retorna el valor especificado de un registro en la base de
        datos a partir de una ID proporcionada y el campo del que se desea
        obtener su valor.

        ### Los parámetros de entrada son:
        - `table_name`: Nombre de la tabla de donde se tomarán los registros.
        - `record_id`: ID del registro a leer.
        - `field`: Nombre del campo de la tabla del que se desea obtener su
        valor.

        Uso:
        >>> # Ejemplo 1
        >>> db_connection.get_value('users', 1, 'name')
        >>> # 'onnymm'
        >>> 
        >>> # Ejemplo 2
        >>> db_connection.get_value('products', 5, 'price')
        >>> # 35.50
        """

        # Obtención de la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Obtención de los campos de la tabla
        table_field = self._models.get_table_field(table_model, field)

        # Creación del query base
        stmt = select(table_field)

        # Creación del query where
        where_query = self._where.build_where(table_model, [('id', '=', record_id)])

        # Conversión del query SQL
        stmt = stmt.where(where_query)

        # Ejecución de la transacción
        response = self._connection.execute(stmt)

        # Destructuración de la tupla dentro de la lista
        [ data ] = response.fetchall()

        # Destructuración del valor dentro de la tupla obtenida
        ( value, ) = data

        # Retorno del valor
        return value

    def get_values(
        self,
        table_name: str,
        record_id: int,
        fields: list[str],
    ) -> tuple:
        """
        ## Obtención de valores
        Este método retorna los valores especificados de un registro en la base
        de datos a partir de una ID proporcionada y los campos de los cuales se
        desea obtener sus valores.

        ### Los parámetros de entrada son:
        - `table_name`: Nombre de la tabla de donde se tomarán los registros.
        - `record_id`: ID del registro a leer.
        - `field`: Nombre de los campos de los cuales se desea obtener sus
        valores.

        Uso:
        >>> # Ejemplo 1
        >>> db_connection.get_values('users', 1, ['name', 'create_date'])
        >>> # ('onnymm', '2024-11-04 11:16:59')
        >>> 
        >>> # Ejemplo 2
        >>> db_connection.get_values('products', 5, ['price', 'create_uid'])
        >>> # (35.50, 3)
        """

        # Obtención de la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Obtención de los campos de la tabla
        table_fields = self._models.get_table_fields(table_model, fields, include_id= False)

        # Creación del query base
        stmt = select(*table_fields)

        # Creación del query where
        where_query = self._where.build_where(table_model, [('id', '=', record_id)])

        # Conversión del query SQL
        stmt = stmt.where(where_query)

        # Ejecución de la transacción
        response = self._connection.execute(stmt)

        # Destructuración de la tupala desde la lista obtenida
        [ data ] = response.fetchall()

        # Retorno de la tupla de valores
        return data

    def search_read(
        self,
        table_name: str,
        search_criteria: CriteriaStructure = [],
        fields: list[str] = [],
        offset: int | None = None,
        limit: int | None = None,
        sortby: str | list[str] | None = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
    ) -> pd.DataFrame | dict[str, RecordValue]:
        """
        ## Búsqueda y lectura de registros
        Este método retorna un DataFrame con el contenido de los registros de una
        tabla de la base de datos, en el orden en el que se especificaron los campos
        o todos los campos en caso de no haber sido especificados.

        ### Los parámetros de entrada son:
        - `table_name`: Nombre de la tabla de donde se tomarán los registros.
        - `search_criteria`: Criterio de búsqueda para retornar únicamente los resultados que
        cumplan con las condiciones provistas (Consultar estructura más abajo).
        - `fields`: Campos a mostrar. En caso de no ser especificado, se toman todos los
        campos de la tabla de la base de datos.
        - `offset`: Desfase de inicio de primer registro a mostrar.
        - `limit`: Límite de registros retornados por la base de datos.

        Uso:
        >>> # Ejemplo 1
        >>> db.search_read('users')
        >>> #    id    user          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> # 1   3   lumii    Lumii Mynx 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 2
        >>> db.search_read('users', [('user', '=', 'onnymm')])
        >>> #    id    user          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 3
        >>> db.search_read('users', [], ['user', 'create_date'])
        >>> #    id         name         create_date
        >>> # 0   2 Onnymm Azzur 2024-11-04 11:16:59
        >>> # 1   3   Lumii Mynx 2024-11-04 11:16:59

        ----
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

        ----
        ### Criterios de búsqueda muy específicos
        También es posible formular criterios de búsqueda más avanzados como el que se muestra a
        continuación:
        >>> search_criteria = [
        >>>     '&',
        >>>         '|',
        >>>             ('partner_id', '=', 14418),
        >>>             ('partner_id', '=', 14417),
        >>>         ('salesperson_id', '=', 213)
        >>> ]
        >>> # "partner_id" es igual a 14418 o "partner_id" es igual a 14417 y a su vez "salesperson_id" es igual a 213.
        
        Si el criterio es demasiado largo, también se puede declarar por fuera. También se puede importar
        el tipo de dato `CriteriaStructure` para facilitar la creación apoyandose con el la herramienta de
        autocompletado del editor de código:
        >>> from app.core._types import CriteriaStructure
        >>> search_criteria: CriteriaStructure = ...

        ----
        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que
        una búsqueda normal arrojaría los siguientes resultados:
        >>> db.search_read('users')
        >>> #    id     user                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como
        por ejemplo lo siguiente:
        >>> db.search_read('users', offset= 2)
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        ----
        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una
        búsqueda normal arrojaría los siguientes registros:
        >>> db.search_read('users')
        >>> #    id     user                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un
        número provisto:
        >>> db.search_read('users', limit= 3)
        >>> #    id     user                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        """

        # Obtención de la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Obtención de los campos de la tabla
        table_fields = self._models.get_table_fields(table_model, fields)

        # Creación del query base
        stmt = select(*table_fields)

        # Creación del segmento WHERE en caso de haberlo
        stmt = self._where.add_query(stmt, table_model, search_criteria)

        # Creación de parámetros de ordenamiento
        stmt = self._query.build_sort(
            stmt,
            table_model,
            sortby,
            ascending,
        )

        # Segmentación de inicio y fin en caso de haberlos
        stmt = self._query.build_segmentation(stmt, offset, limit)

        # Ejecución de la transacción
        response = self._connection.execute(stmt)

        # Inicialización del DataFrame de retorno
        data = pd.DataFrame(response.fetchall())

        # Retorno en formato de salida configurado
        return self._output.build_output(data, table_fields, output_format, 'dataframe')

    def search_count(
        self,
        table_name: str,
        search_criteria: CriteriaStructure = [],
    ) -> int:
        """
        ## Búsqueda y conteo de resultados
        Este método retorna el conteo de de todos los registros de una tabla o los
        registros que cumplan con la condición de búsqueda provista, ideal para funcionalidades
        de paginación que muestran un total de registros.

        Uso:
        >>> # Ejemplo 1
        >>> db.search_count('users')
        >>> # 5
        >>> 
        >>> # Ejemplo 2
        >>> db.search_count('commisions', [('user_id', '=', 213)])
        >>> # 126

        ### Los parámetros de entrada son:
        - `table_name`: Nombre de la tabla de donde se tomarán los registros.
        - `search_criteria`: Criterio de búsqueda para retornar únicamente los resultados que
        cumplan con las condiciones provistas (Consultar estructura más abajo).

        ----
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

        ----
        ### Criterios de búsqueda muy específicos
        También es posible formular criterios de búsqueda más avanzados como el que se muestra a
        continuación:
        >>> search_criteria = [
        >>>     '&',
        >>>         '|',
        >>>             ('partner_id', '=', 14418),
        >>>             ('partner_id', '=', 14417),
        >>>         ('salesperson_id', '=', 213)
        >>> ]
        >>> # "partner_id" es igual a 14418 o "partner_id" es igual a 14417 y a su vez "salesperson_id" es igual a 213.
        
        Si el criterio es demasiado largo, también se puede declarar por fuera. También se puede importar
        el tipo de dato `CriteriaStructure` para facilitar la creación apoyandose con el la herramienta de
        autocompletado del editor de código:
        >>> from app.core._types import CriteriaStructure
        >>> search_criteria: CriteriaStructure = ...
        """

        # Obtenciónde la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Creación del query base
        stmt = (
            select( func.count() )
            .select_from(table_model)
        )

        # Creación del segmento WHERE en caso de haberlo
        stmt = self._where.add_query(stmt, table_model, search_criteria)

        # Ejecución de la transacción
        response = self._connection.execute(stmt)

        # Retorno del conteo de registro
        return response.scalar()

    def update(
        self,
        table_name: str,
        record_ids: int | list[int],
        data: RecordData,
    ) -> bool:
        """
        ## Actualización de registros
        Este método realiza la actualización de uno o más registros a partir de su respectiva
        ID provista, actualizando uno o más campos con el valor provisto. Este método solo
        sobreescribe un mismo valor por cada campo a todos los registros provistos.

        ### Los parámetros de entrada son:
        - `table_name`: Nombre de la tabla en donde se harán los cambios
        - `record_ids`: ID o lista de IDs a actualizar
        - `data`: Diccionario de valores a modificar masivamente

        Uso:
        >>> db.search_read('users', fields= ['user', 'name'])
        >>> #    id     user                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        >>> 
        >>> # Modificación
        >>> db.update("users", [3, 4, 5], {'name': 'Cambiado'})
        >>> #    id     user                  name
        >>> # 0   3   onnymm              Cambiado
        >>> # 1   4    lumii              Cambiado
        >>> # 2   5  user001              Cambiado
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        """

        # Conversión de datos entrantes si es necesaria
        if isinstance(record_ids, int):
            record_ids = [record_ids,]

        # Ejecución del método UPDATE WHERE
        return self.update_where(table_name, [('id', 'in', record_ids)], data)

    def update_where(
        self,
        table_name: str,
        search_criteria: CriteriaStructure,
        data: RecordData,
    ) -> bool:
        """
        "" Actualización de registros donde...
        Este método realiza la actualización de uno o más registros a partir de una
        condición provista, actualizando uno o más campos con el valor provisto. Este
        método solo sobreescribe un mismo valor por cada campo a todos los registros
        encontrados en base a la condición provista.

        ### Los parámetros de entrada son:
        - `table_name`: Nombre de la tabla en donde se harán los cambios
        - `search_criteria`: Condición que deben cumplir los registros a ser
        modificados.
        - `data`: Diccionario de valores a modificar masivamente

        Uso:
        >>> db.search_read('users', fields= ['user', 'name'])
        >>> #    id     user                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        >>> 
        >>> # Modificación
        >>> db.update("users", [('name', 'ilike', 'sin nombre')], {'name': 'Zopilote'})
        >>> #    id     user          name
        >>> # 0   3   onnymm  Onnymm Azzur
        >>> # 1   4    lumii    Lumii Mynx
        >>> # 2   5  user001      Zopilote
        >>> # 3   6  user002      Zopilote
        >>> # 4   7  user003      Zopilote
        """

        # Obtención de la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Creación del query base
        stmt = update(table_model)

        # Creación del segmento WHERE
        stmt = self._where.add_query(stmt, table_model, search_criteria)

        # Declaración de valores a cambiar
        stmt = stmt.values(data)

        # Declaración para obtener las IDs modificadas
        stmt = stmt.returning(self._models.get_id_field(table_model))

        # Ejecución de la transacción
        response = self._connection.execute(stmt, commit= True)

        # Obtención de las IDs creadas
        modified_records: list[int] = [getattr(row, 'id') for row in response]

        # Ejecución de las automatizaciones correspondientes
        self._automations.run_after_transaction(
            table_name,
            'update',
            modified_records,
        )

        # Retorno de confirmación de movimientos
        return True

    def delete(
        self,
        table_name: str,
        record_ids: int | list[int]
    ) -> bool:
        """
        ## Eliminación de registros
        Este método realiza la eliminación de uno o más registros de la base datos a partir de
        su respectiva ID provista.

        Uso:
        >>> #    id     user                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        >>> 
        >>> # Eliminación
        >>> db.delete("users", 3)
        >>> #    id     user                  name
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        """

        # Conversión de datos entrantes si es necesaria
        if isinstance(record_ids, int):
            record_ids = [record_ids,]

        # Creación de función de ejecución de automatizaciones
        run_post_delete_automations = self._automations.generate_before_transaction(
            table_name,
            record_ids,
        )

        # Obtención de la instancia de la tabla
        table_model = self._models.get_table_model(table_name)

        # Creación del query
        stmt = (
            delete(table_model)
            .where(getattr(table_model, 'id').in_(record_ids))
            .returning(self._models.get_id_field(table_model))
        )

        # Ejecución de la transacción
        response = self._connection.execute(stmt, commit= True)

        # Obtención de las IDs encontradas
        deleted_ids: list[int] = [getattr(row, 'id') for row in response]

        # Ejecución de las automatizaciones correspondientes
        run_post_delete_automations(deleted_ids)

        return True

    def and_(
        self,
        cs_1: CriteriaStructure,
        cs_2: CriteriaStructure
    ) -> CriteriaStructure:

        # Si los dos criterios de búsqueda contienen datos
        if len(cs_1) and len(cs_2):

            # Se retornan los criterios de búsqueda unidos por operador `and`
            res: CriteriaStructure = ['&', *cs_1, *cs_2]
            return res

        # Si sólo el primer criterio de búsqueda contiene datos...
        elif len(cs_1):
            # Se retorna sólo el primer criterio de búsqueda
            return cs_1
        """
        ## Método para unir dos criterios de búsqueda por medio de un operador `'&'`.

        Uso:
        >>> # Ejemplo 1
        >>> cs_1 = [('invoice_line_id', '=', 5)]
        >>> cs_2 = [('state', '=', 'sent')]
        >>> merged_cs = lylac.and_(cs_1, cs_2)
        >>> # ['&', ('invoice_line_id', '=', 5), ('state', '=', 'sent')]
        >>> 
        >>> # Ejemplo 2
        >>> cs_1 = [('invoice_line_id', '=', 5)]
        >>> cs_2 = ['|', ('state', '=', 'posted'), ('state', '=', 'sent')]
        >>> merged_cs = lylac.and_(cs_1, cs_2)
        >>> # ['&', ('invoice_line_id', '=', 5), '|', ('state', '=', 'posted'), ('state', '=', 'sent')]
        """

    def or_(
        self,
        cs_1: CriteriaStructure,
        cs_2: CriteriaStructure
    ) -> CriteriaStructure:
        """
        ## Método de clase para unir dos criterios de búsqueda por medio de un operador `'|'`.

        Uso:
        >>> # Ejemplo 1
        >>> cs_1 = [('invoice_line_id', '=', 5)]
        >>> cs_2 = [('state', '=', 'sent')]
        >>> merged_cs = DMLManager.or_(cs_1, cs_2)
        >>> # ['|', ('invoice_line_id', '=', 5), ('state', '=', 'sent')]
        >>> 
        >>> # Ejemplo 2
        >>> cs_1 = [('invoice_line_id', '=', 5)]
        >>> cs_2 = ['|', ('state', '=', 'posted'), ('state', '=', 'sent')]
        >>> merged_cs = DMLManager.or_(cs_1, cs_2)
        >>> # ['|', ('invoice_line_id', '=', 5), '|', ('state', '=', 'posted'), ('state', '=', 'sent')]
        """

        # Si los dos criterios de búsqueda contienen datos
        if len(cs_1) and len(cs_2):

            # Se retornan los criterios de búsqueda unidos por operador `or`
            res: CriteriaStructure = ['|', *cs_1, *cs_2]
            return res

        # Si sólo el primer criterio de búsqueda contiene datos...
        elif len(cs_1):
            # Se retorna sólo el primer criterio de búsqueda
            return cs_1
