from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.types import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    Time,
    LargeBinary,
)
from ...._module_types import (
    NewField,
    TType,
)
from .._module_types import ColumnGenerator
from ._base import (
    _BaseDDLManager,
    _BaseModels,
)

class _Models(_BaseModels):

    build_column: dict[TType, ColumnGenerator]
    """
    ### Construcción de columna
    Este mapa de métodos construye una columna tipada para un modelo de SQLALchemy.
    """

    def __init__(
        self,
        instance: _BaseDDLManager,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance

        # Inicialización de mapa de funciones
        self.build_column = self._initialize_column_builder()

    def _build_args(self, field: NewField) -> dict:

        # Inicialización de objeto a retornar
        kwargs = {
            'nullable': field.nullable,
            'default': field.default_value,
            'unique': field.unique
        }

        return kwargs

    def _initialize_column_builder(
        self
    ) -> dict[TType, ColumnGenerator]:

        return {
            'integer': lambda field: Column(Integer, **self._build_args(field)),
            'char': lambda field: Column(String(255), **self._build_args(field)),
            'float': lambda field: Column(Float, **self._build_args(field)),
            'boolean': lambda field: Column(Boolean, **self._build_args(field)),
            'date': lambda field: Column(Date, **self._build_args(field)),
            'datetime': lambda field: Column(DateTime, **self._build_args(field)),
            'time': lambda field: Column(Time, **self._build_args(field)),
            'file': lambda field: Column(LargeBinary, **self._build_args(field)),
            'text': lambda field: Column(Text, **self._build_args(field)),
            'selection': lambda field: Column(String, **self._build_args(field)),
            'many2one': lambda field: Column(ForeignKey(f'{field.table_model.__tablename__}.id'), **self._build_args(field)),
        }

    def delete_model(
        self,
        model_name: str,
    ) -> None:

        # Se elimina el modelo de SQLAlchemy de los modelos heredados de Base
        self._ddl._main._base.metadata.remove(
            self._ddl._main._base.metadata.tables[model_name]
        )

        # Se elimina la tabla de los registros del mapa de tablas
        self._ddl._main._strc.unregister_table(model_name.replace("_", "."))
