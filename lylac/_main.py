from typing import Callable
import pandas as pd
from sqlalchemy import (
    select,
    delete,
    asc,
    update,
    func,
)
from ._constants import FIELD_NAME
from ._core import _Lylac
from ._module_types import (
    _T,
    CriteriaStructure,
    DataPerRecord,
    RecordData,
    CredentialsAlike,
    OutputOptions,
    Transaction,
    RecordValue,
    ExecutionMethod,
)
from ._modules import (
    Algorythms,
    Auth,
    Automations,
    Compiler,
    Connection,
    DDLManager,
    Index,
    Metadata,
    Models,
    Output,
    Preprocess,
    Select,
    Structure,
    Query,
    Validations,
    Where,
)

class Lylac(_Lylac):

    def __init__(
        self,
        credentials: CredentialsAlike = None,
        output_format: OutputOptions | None = None,
    ) -> None:

        # Asignación del modelo base
        self._metadata = Metadata(self)
        # Inicialización del módulo de manejo de formato de salida
        self._output = Output(self, output_format)
        # Creación de la instancia de conexión con la base de datos
        self._connection = Connection(self, credentials)

        # Inicialización de submódulos
        self._algorythms = Algorythms(self)
        self._strc = Structure(self)
        self._models = Models(self)
        self._index = Index(self)
        self._compiler = Compiler(self)
        self._auth = Auth(self)
        self._ddl = DDLManager(self)
        self._where = Where(self)
        self._preprocess = Preprocess(self)
        self._query = Query(self)
        self._select = Select(self)
        self._automations = Automations(self)
        self._validations = Validations(self)

        # Registro de las automatizaciones predeterminadas
        self._automations.create_preset_automations()
        # Inicialización de estructura de modelos de la instancia
        self._ddl._m_reset.initialize_from_data()
        # Inicialización de los datos de validaciones
        self._validations.initialize()

    def login(
        self,
        login: str,
        password: str,
    ) -> str | bool:

        return self._auth.login(login, password)

    def register_automation(
        self,
        model_name: str,
        transation: Transaction,
        fields: list[str] = [FIELD_NAME.ID],
        execute_if: CriteriaStructure = [],
        method: ExecutionMethod = 'record',
    ):
        """
        ### Registro de automatización
        Este decorador permite registrar una automatización en la instancia del
        módulo.
        Ejemplo de uso:
        >>> @lylac.register_automation(
        >>>     # Modelo donde se ejecutará la automatización
        >>>     'custom.model',
        >>>     # La automatización se ejecuta tras crearse un registro
        >>>     'create',
        >>>     # Campos del registro a usar en la automatización
        >>>     ['name'],
        >>> )
        >>> def do_something(params) -> None:
        >>>     record_id = params.id
        >>>     record_name = params.record_data['name']
        >>>     print(f'Se creó un registro con ID {record_id} y nombre {record_name}')

        Automatización más específica:
        >>> @lylac.register_automation(
        >>>     # Tabla donde se ejecutará la automatización
        >>>     'custom.model',
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

        #### Tipado dinámico
        Puede utilizarse tipado dedicado para mejorar el flujo de desarrollo de la
        función a registrar en el decorador. Se utilizan tipos de dato nativos de
        Python.
        Ejemplo:
        >>> from lylac.utils import BaseRecordData, DataPerRecord
        >>> 
        >>> class CustomModel(BaseRecordData):
        >>>     value: str
        >>>     sync: bool
        >>> 
        >>> @lylac.register_automation(...)
        >>> def do_something(params: DataPerRecord[CustomModel]) -> None:
        >>>     ...

        De esta manera el editor de código realizará el autocompletado al acceder a
        las llaves de la información.

        #### Nota:
        En el argumento `fields` se debe especificar qué campos se van a utilizar
        en la lectura del registro dentro de la automatización. Esto es
        indispensable para reducir las cargas de información solicitadas a la base
        de datos.
        """

        # Creación del decorador que registrará la automatización
        def decorator(new_automation: Callable[[DataPerRecord[_T]], None]):

            # Registro de la automatización en la estructura central
            self._automations.register_automation(
                model_name,
                transation,
                new_automation,
                fields,
                execute_if,
                method,
            )

            return new_automation

        # Retorno del decorador
        return decorator

    def create(
        self,
        model_name: str,
        data: RecordData | list[RecordData],
    ) -> list[int]:
        """
        ### Creación de registros
        Este método realiza la creación de uno o muchos registros a partir del
        nombre de un modelo proporcionado y un diccionario (un único registro)
        o una lista de diccionarios (muchos registros).

        Uso:
        >>> # Para un solo registro
        >>> record = {
        >>>     'login': 'onnymm',
        >>>     'name': 'Onnymm Azzur',
        >>> }
        >>> 
        >>> db.create('base.users', record)
        >>> #    id   login          name
        >>> # 0   2  onnymm  Onnymm Azzur
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
        >>> db.create('base.users', records)
        >>> #    id   login          name
        >>> # 0   2  onnymm  Onnymm Azzur
        >>> # 1   3   lumii    Lumii Mynx
        """

        # Conversión de datos entrantes si es necesaria
        data = self._preprocess.convert_to_list(data)

        # Preprocesamiento de datos en creación
        pos_creation_callback = self._preprocess.process_data_on_create(model_name, data)

        # Ejecución de validaciones
        self._validations.run_validations_on_create(model_name, data)

        # Creación de los registros y obtención de las IDs creadas
        inserted_records = self._compiler.create(model_name, data)

        # Ejecución de las automatizaciones correspondientes
        self._automations.run_after_transaction(
            model_name,
            'create',
            inserted_records,
        )

        # Ejecución de la función poscreación
        pos_creation_callback(inserted_records)

        # Retorno de las IDs creadas
        return inserted_records

    def search(
        self,
        model_name: str,
        search_criteria: CriteriaStructure = [],
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[int]:
        """
        ### Búsqueda de registros
        Este método retorna todos los registros de una tabla o los registros que cumplan
        con la condición de búsqueda provista, además de segmentar desde un índice
        inicial de desfase y/o un límite de cantidad de registros retornada.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.search('base.users')
        >>> # [1, 2, 3, 4, 5]
        >>> 
        >>> # Ejemplo 2
        >>> lylac.search('base.model.field', [('create_uid', '=', 2)])
        >>> # [7, 9, 12, 13, 17, 21, ...]

        ----
        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
        unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
        primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        ----
        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        ----
        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
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

        ----
        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que
        una búsqueda normal arrojaría los siguientes resultados:
        >>> lylac.search('base.users')
        >>> # [1, 2, 3, 4, 5, 6, 7]

        Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como
        por ejemplo lo siguiente:
        >>> lylac.search('base.users', offset= 2)
        >>> # [3, 4, 5, 6, 7]

        ----
        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una
        búsqueda normal arrojaría los siguientes registros:
        >>> lylac.search('base.users')
        >>> # [3, 4, 5, 6, 7]

        Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un
        número provisto:
        >>> lylac.search('base.users', limit= 3)
        >>> # [1, 2, 3]
        """

        # Obtención de la instancia de la tabla
        model_model = self._models.get_table_model(model_name)
        # Creación del query SELECT
        ( stmt, _ ) = self._select.build(model_name, [FIELD_NAME.ID])

        # Si hay criterios de búsqueda se genera el 'where'
        if len(search_criteria) > 0:
            # Creación del query where
            where_query = self._where.build_where(model_model, search_criteria)
            # Conversión del query SQL
            stmt = stmt.where(where_query)

        # Ordenamiento de los datos
        stmt = stmt.order_by( asc(FIELD_NAME.ID) )

        # Segmentación de inicio y fin en caso de haberlos
        stmt = self._query.build_segmentation(stmt, offset, limit)

        # Ejecución de la transacción
        response = self._connection.execute(stmt)

        # Obtención de las IDs encontradas
        found_ids = self._output.get_found_ids(response)

        return found_ids

    def get_value(
        self,
        model_name: str,
        record_id: int,
        field: str,
    ) -> RecordValue:
        """
        ### Obtención de un valor
        Este método retorna el valor especificado de un registro en la base de
        datos a partir de una ID proporcionada y el campo del que se desea
        obtener su valor.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.get_value('base.users', 2, 'name')
        >>> # 'onnymm'
        >>> 
        >>> # Ejemplo 2
        >>> lylac.get_value('base.permissions', 5, 'create_date')
        >>> # '2025-07-01 10:00:00'
        """

        # Obtención del único elemento contenido en la lista
        [ value ] = (
            # Se utiliza el método de lectura con el registro específico
            self.read(
                model_name,
                record_id,
                [field],
                output_format= 'dataframe',
                only_ids_in_relations= True,
            )
            # Se accede a la columna
            [field]
            # Se convierte la serie de una lista de un elemento
            .to_list()
        )

        return value

    def get_values(
        self,
        model_name: str,
        record_id: int,
        fields: list[str],
    ) -> tuple:
        """
        ### Obtención de valores
        Este método retorna los valores especificados de un registro en la base
        de datos a partir de una ID proporcionada y los campos de los cuales se
        desea obtener sus valores.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.get_values('base.users', 1, ['name', 'create_date'])
        >>> # ('onnymm', '2024-11-04 11:16:59')
        >>> 
        >>> # Ejemplo 2
        >>> lylac.get_values('base.permissions', 5, ['label', 'create_uid'])
        >>> # ('Valores de selección de campos - Administrador', 3)
        """

        # Obtención de la lista de valores
        values = (
            # Se utiliza el método de lectura con el registro específico
            self.read(
                model_name,
                record_id,
                fields,
                output_format= 'dataframe',
                only_ids_in_relations= True,
            )
            # Se accede a la columna
            [fields]
            # Se transpone el DataFrame
            .T
            # Se accede a la columna creada
            [0]
            # Se convierte la serie de una lista de valores
            .to_list()
        )

        # Se convierte el resultado a tupla
        values = tuple(values)

        return values

    def read(
        self,
        model_name: str,
        record_ids: int | list[int],
        fields: list[str] = [],
        sortby: str | list[str] = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | list[dict[str, RecordValue]]:
        """
        ### Lectura de registros
        Este método retorna un DataFrame con el contenido de los registros de
        una tabla de la base de datos a partir de una lista de IDs, en el orden
        en el que se especificaron los campos o todos los campos en caso de no
        haber sido especificados.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.search_read('base.users', [2])
        >>> #    id   login          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> lylac.search_read('base.users', [2, 3])
        >>> #    id   login          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> # 1   3   lumii    Lumii Mynx 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 3
        >>> lylac.search_read('base.users', [2, 3], ['user', 'create_date'])
        >>> #    id         name         create_date
        >>> # 0   2 Onnymm Azzur 2024-11-04 11:16:59
        >>> # 1   3   Lumii Mynx 2024-11-04 11:16:59
        """

        # Conversión de datos entrantes si es necesaria
        record_ids = self._preprocess.convert_to_list(record_ids)

        # Obtención de la instancia de la tabla
        model_model = self._models.get_table_model(model_name)

        # Creación del query base
        ( stmt, ttypes ) = self._select.build(model_name, fields)

        # Creación del query where
        where_query = self._where.build_where(model_model, [(FIELD_NAME.ID, 'in', record_ids)])

        # Conversión del query SQL
        stmt = stmt.where(where_query)

        # Creación de parámetros de ordenamiento
        stmt = self._query.build_sort(
            stmt,
            model_model,
            sortby,
            ascending,
        )

        # Ejecución de la transacción
        response = self._connection.execute(stmt)

        # Inicialización del DataFrame de retorno
        data = pd.DataFrame( response.fetchall() )

        # Retorno en formato de salida configurado
        return self._output.build_output(data, ttypes, output_format, 'dataframe', only_ids_in_relations)

    def search_read(
        self,
        model_name: str,
        search_criteria: CriteriaStructure = [],
        fields: list[str] = [],
        offset: int | None = None,
        limit: int | None = None,
        sortby: str | list[str] | None = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | dict[str, RecordValue]:
        """
        ### Búsqueda y lectura de registros
        Este método retorna un DataFrame con el contenido de los registros de una
        tabla de la base de datos, en el orden en el que se especificaron los campos
        o todos los campos en caso de no haber sido especificados.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.search_read('base.users')
        >>> #    id   login          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> # 1   3   lumii    Lumii Mynx 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 2
        >>> lylac.search_read('base.users', [('user', '=', 'onnymm')])
        >>> #    id   login          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 3
        >>> lylac.search_read('base.users', [], ['user', 'create_date'])
        >>> #    id         name         create_date
        >>> # 0   2 Onnymm Azzur 2024-11-04 11:16:59
        >>> # 1   3   Lumii Mynx 2024-11-04 11:16:59

        ----
        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
        unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
        primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        ----
        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        ----
        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
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

        ----
        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que
        una búsqueda normal arrojaría los siguientes resultados:
        >>> lylac.search_read('base.users')
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como
        por ejemplo lo siguiente:
        >>> lylac.search_read('base.users', offset= 2)
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        ----
        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una
        búsqueda normal arrojaría los siguientes registros:
        >>> lylac.search_read('base.users')
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un
        número provisto:
        >>> lylac.search_read('base.users', limit= 3)
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        """

        # Obtención de la instancia de la tabla
        model_model = self._models.get_table_model(model_name)

        # Creación del query base
        ( stmt, ttypes ) = self._select.build(model_name, fields)

        # Creación del segmento WHERE en caso de haberlo
        stmt = self._where.add_query(stmt, model_model, search_criteria)

        # Creación de parámetros de ordenamiento
        stmt = self._query.build_sort(
            stmt,
            model_model,
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
        return self._output.build_output(data, ttypes, output_format, 'dataframe', only_ids_in_relations)

    def search_count(
        self,
        model_name: str,
        search_criteria: CriteriaStructure = [],
    ) -> int:
        """
        ### Búsqueda y conteo de resultados
        Este método retorna el conteo de de todos los registros de una tabla o los
        registros que cumplan con la condición de búsqueda provista, ideal para funcionalidades
        de paginación que muestran un total de registros.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.search_count('base.users')
        >>> # 5
        >>> 
        >>> # Ejemplo 2
        >>> lylac.search_count('base.permissions', [('create_uid', '=', 5)])
        >>> # 126

        ----
        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
        unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
        primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        ----
        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        ----
        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
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
        """

        # Obtenciónde la instancia de la tabla
        model_model = self._models.get_table_model(model_name)

        # Creación del query base
        stmt = (
            select( func.count() )
            .select_from(model_model)
        )

        # Creación del segmento WHERE en caso de haberlo
        stmt = self._where.add_query(stmt, model_model, search_criteria)

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
        ### Actualización de registros
        Este método realiza la actualización de uno o más registros a partir de su respectiva
        ID provista, actualizando uno o más campos con el valor provisto. Este método solo
        sobreescribe un mismo valor por cada campo a todos los registros provistos.

        Uso:
        >>> lylac.search_read('base.users', fields= ['login', 'name'])
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        >>> 
        >>> # Modificación
        >>> lylac.update('base.users', [3, 4, 5], {'name': 'Cambiado'})
        >>> #    id    login                  name
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
        return self.update_where(table_name, [('id', 'in', record_ids)], data, record_ids)

    def update_where(
        self,
        model_name: str,
        search_criteria: CriteriaStructure,
        data: RecordData,
        _record_ids: list[int] = []
    ) -> bool:
        """
        ### Actualización de registros donde...
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
        >>> lylac.search_read('base.users', fields= ['login', 'name'])
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        >>> 
        >>> # Modificación
        >>> db.update('base.users', [('name', 'ilike', 'sin nombre')], {'name': 'Zopilote'})
        >>> #    id    login          name
        >>> # 0   3   onnymm  Onnymm Azzur
        >>> # 1   4    lumii    Lumii Mynx
        >>> # 2   5  user001      Zopilote
        >>> # 3   6  user002      Zopilote
        >>> # 4   7  user003      Zopilote
        """

        # Ejecución de validaciones
        self._validations.run_validations_on_update(model_name, search_criteria, data)

        # Obtención de la instancia de la tabla
        model_model = self._models.get_table_model(model_name)

        # Preprocesamiento de datos en actualización y obtención de función posactualización
        after_update_callback = self._preprocess.process_data_on_update(model_name, _record_ids, data)

        # Creación del query base
        stmt = update(model_model)

        # Creación del segmento WHERE
        stmt = self._where.add_query(stmt, model_model, search_criteria)

        # Declaración de valores a cambiar
        stmt = stmt.values(data)

        # Declaración para obtener las IDs modificadas
        stmt = stmt.returning(self._models.get_id_field(model_model))

        # Ejecución de la transacción
        response = self._connection.execute(stmt, commit= True)

        # Obtención de las IDs creadas
        updated_records: list[int] = [getattr(row, 'id') for row in response]

        # Ejecución de las automatizaciones correspondientes
        self._automations.run_after_transaction(
            model_name,
            'update',
            updated_records,
        )

        # Ejecución de función posactualización
        after_update_callback()

        # Retorno de confirmación de movimientos
        return True

    def delete(
        self,
        model_name: str,
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
        record_ids = self._preprocess.convert_to_list(record_ids)

        # Creación de función de ejecución de automatizaciones
        run_post_delete_automations = self._automations.generate_before_transaction(
            model_name,
            record_ids,
        )

        # Obtención de la instancia de la tabla
        model_model = self._models.get_table_model(model_name)

        # Creación del query
        stmt = (
            delete(model_model)
            .where(getattr(model_model, FIELD_NAME.ID).in_(record_ids))
            .returning(self._models.get_id_field(model_model))
        )

        # Ejecución de la transacción
        response = self._connection.execute(stmt, commit= True)

        # Obtención de las IDs encontradas
        deleted_ids: list[int] = [getattr(row, FIELD_NAME.ID) for row in response]

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
