from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause
from ...._module_types import NewField
from ._base import _BaseDDLManager, _BaseDatabase
from ...._module_types import TType

class _Database(_BaseDatabase):
    """
    ### Métodos de base de datos
    Este submódulo agrupa todos los métodos relacionados con la manipulación de la
    base de datos.
    """

    # Mapeo de nombres a tipos de dato en SQL
    _name_to_type: dict[TType, str] = {
        'integer': 'INTEGER',
        'char': 'VARCHAR(255)',
        'float': 'FLOAT',
        'boolean': 'BOOLEAN',
        'date': 'DATE',
        'datetime': 'TIMESTAMP',
        'time': 'TIME',
        'file': 'BYTEA',
        'text': 'TEXT',
        'selection': 'VARCHAR(100)',
        'many2one': 'INTEGER',
    }

    def __init__(
        self,
        instance: _BaseDDLManager,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance

    def add_column(
        self,
        params: NewField,
    ) -> TextClause:
        """
        ### Añadir columna a tabla
        Este método añade una columna a la tabla especificada con los atributos
        especificados en la declaración del objeto entrante.
        """

        # Creación de la sentencia
        stmt = text(
            self._add_column_query(params)
            + self._default_value(params)
        )

        # Ejecución de la transacción
        self._ddl._main._connection.execute(stmt, commit= True)

    def _add_column_query(
        self,
        params: NewField,
    ) -> str:

        # Obtención de los atributos
        table_name = params.table_model.__tablename__
        field_name = params.field_name
        field_type = self._name_to_type[params.ttype].upper()

        # Retorno del framento "add column"
        return f'ALTER TABLE {table_name} ADD COLUMN {field_name} {field_type}'

    def _default_value(
        self,
        params: NewField,
    ) -> str:

        # Si no existe un valor por defecto
        if params.default_value is None:
            return ''

        # Si el valor es de tipo cadena de texto...
        if isinstance(params.default_value, str):
            value = f"'{params.default_value}'"
        # Si el valor es de tipo booleano...
        elif isinstance(params.default_value, bool):
            value = str(params.default_value).upper()
        # Si el valor es de otro tipo de dato...
        else:
            value = str(params.default_value)

        # Retorno del framgento "default value"
        return f' DEFAULT {value}'

    def drop_column(
        self,
        table_name: str,
        column_name: str,
    ) -> None:

        # Creación del query a ejecutar
        stmt = text(f'ALTER TABLE {table_name} DROP COLUMN {column_name}')

        # Ejecución de la transacción en la base de datos
        self._ddl._main._connection.execute(stmt, commit= True)
