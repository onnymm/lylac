from typing import Any
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty
from ..._core import (
    _Lylac,
    _BaseModels,
)

class Models(_BaseModels):

    def __init__(
        self,
        instance: _Lylac,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

    def get_table_model(
        self,
        table_name: str,
    ) -> type[DeclarativeBase]:

        # Obtención de la referencia mapeada
        return self._main._strc.models[table_name]['model']

    def get_id_field(
        self,
        table_model: type[DeclarativeBase]
    ) -> InstrumentedAttribute[int]:

        # Retorno de la instancia del campo de ID
        return getattr(table_model, 'id')

    def get_table_field(
        self,
        table: str,
        field: str,
    ) -> InstrumentedAttribute:

        # Obtención del campo, atributo de la instancia de la tabla
        return getattr(table, field)

    def get_table_fields(
        self,
        table_instance: type[DeclarativeBase],
        fields: list[str] = [],
        include_id: bool = True,
    ) -> list[InstrumentedAttribute[Any]]:

        # Inicialización de la lista con el valor de 'id' como primer elemento
        id_field = ['id',]

        # Obtención de todos los campos
        if len(fields) == 0:
            # Obtención de columnas con relación para evitar productos cartesianos
            instance_relationships = { _relationship.key for _relationship in inspect(table_instance).relationships }
            mapper = inspect(table_instance)
            all_columns = [column.key for column in mapper.attrs if isinstance(column, ColumnProperty)]
            instance_fields = [col for col in all_columns if col not in instance_relationships]

            # Asignación de valor a la variable entrante
            fields = instance_fields

        if include_id:
            # Remoción del campo de 'ID en caso de ser solicitado, ara evitar campos duplicados en el retorno de la información
            try:
                fields.remove('id')
            except ValueError:
                pass

            # Suma del campo 'ID' como primer elemento de los campos a retornar
            table_fields = id_field + fields

        # Inclusión del ID solo de forma explícita
        else:
            table_fields = fields


        # Obtención de los atributos de la tabla a partir de los nombres de los campos y retorno en una lista para ser usados en el query correspondiente
        return [ getattr(table_instance, field) for field in table_fields ]
