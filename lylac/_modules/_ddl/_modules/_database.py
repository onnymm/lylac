from sqlalchemy import text
from ...._module_types import (
    FieldAttributes,
    TType,
)
from ._base import _BaseDDLManager, _BaseDatabase

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
        # Referencia del módulo principal
        self._main = instance._main
        # Referencia del módulo de conexión
        self._connection = instance._main._connection

    def add_column(
        self,
        params: FieldAttributes,
    ):
        """
        ### Añadir columna a tabla
        Este método añade una columna a la tabla especificada con los atributos
        especificados en la declaración del objeto entrante.
        """

        # Creación de la sentencia
        stmt = text(
            f"""
            {self._query_add_column(params)}
            {self._query_default_value(params)}
            {self._query_foreign_key(params)}
            """
        )

        # Ejecución de la transacción
        self._connection.execute(stmt, commit= True)

    def drop_column(
        self,
        table_name: str,
        column_name: str,
    ) -> None:

        # Creación del query a ejecutar
        stmt = text(f'ALTER TABLE {table_name} DROP COLUMN {column_name};')

        # Ejecución de la transacción en la base de datos
        self._connection.execute(stmt, commit= True)

    def _query_add_column(
        self,
        params: FieldAttributes,
    ) -> str:

        # Obtención de los atributos
        table_name = params.table_model.__tablename__
        field_name = params.field_name
        field_type = self._name_to_type[params.ttype].upper()

        # Retorno del framento "add column"
        return f'ALTER TABLE {table_name} ADD COLUMN {field_name} {field_type}'

    def _query_default_value(
        self,
        params: FieldAttributes,
    ) -> str:

        # Si no existe un valor por defecto
        if params.default is None:
            return ';'

        # Si el valor es de tipo cadena de texto...
        if isinstance(params.default, str):
            value = f"'{params.default}'"
        # Si el valor es de tipo booleano...
        elif isinstance(params.default, bool):
            value = str(params.default).upper()
        # Si el valor es de otro tipo de dato...
        else:
            value = str(params.default)

        # Retorno del framgento "default value"
        return f' DEFAULT {value};'

    def _query_foreign_key(
        self,
        params: FieldAttributes,
    ) -> str:

        if params.ttype != 'many2one':
            return ''

        # Obtención de los atributos
        table_name = params.table_model.__tablename__
        column_name = params.field_name
        constraint_name = f'{table_name}_{column_name}_fkey'
        referenced_table_name = self._ddl._main.get_value('base.model', params.related_model_id, 'name')

        return (
            f"""
            ALTER TABLE {table_name}
            ADD CONSTRAINT {constraint_name}
            FOREIGN KEY ({column_name})
            REFERENCES {referenced_table_name}(id)
            ON DELETE SET NULL;
            """
        )
