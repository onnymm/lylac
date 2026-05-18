from typing import Any
from typing import Callable
from typing import Sequence
from typing import TYPE_CHECKING
from sqlalchemy.engine import Row
from .._constants import FIELD_SUFFIX
from .._typing.interfaces import Many2One
from .._typing.generics import MaybeNone
from .._typing.generics import _Record
from .._typing.literals import TTypeName

if TYPE_CHECKING:
    from . import FieldTarget

class OutputParser:

    def __init__(
        self,
    ) -> None:

        # Inicialización de atributo de funciones
        self._functions = self.Functions()

        # Inicialización de adatador
        self._adapter: dict[TTypeName, Callable[[str, Row], Any]] = {
            'integer': self._functions.get_generic_value,
            'char': self._functions.get_generic_value,
            'boolean': self._functions.get_generic_value,
            'float': self._functions.get_generic_value,
            'selection': self._functions.get_generic_value,
            'date': self._functions.get_generic_value,
            'time': self._functions.get_generic_value,
            'datetime': self._functions.get_datetime_value,
            'duration': self._functions.get_timedelta_value,
            'text': self._functions.get_generic_value,
            'file': self._functions.get_generic_value,
            'json': self._functions.get_generic_value,
            'many2one': self._functions.get_m2o_value,
            'one2many': self._functions.get_array_value,
            'many2many': self._functions.get_array_value,
        }

    def ids_from_database(
        self,
        records_data: list[tuple[int]]
    ) -> list[int]:

        # Obtención de las IDs de registros encontrados
        record_ids = [record_id for ( record_id, ) in records_data]

        return record_ids

    def records_from_database(
        self,
        records_data: Sequence[Row],
        field_targets: list['FieldTarget'],
    ) -> list[_Record]:

        # Inicialización de lista de registros a retornar
        records: list[_Record] = []

        # Iteración por cada fila de la secuencia
        for row in records_data:
            # Obtención del diccionario de datos del registro
            record = self._create_record_dict(row, field_targets)
            # Se añaden los datos a la lista
            records.append(record)

        return records

    def _create_record_dict(
        self,
        record_data: Row,
        field_targets: list['FieldTarget'],
    ) -> _Record:

        # Inicialización del diccionario a retornar
        record = {}

        # Iteración por cada uno de los objetivos de campo
        for field_target in field_targets:
            # Obtención del tipo de dato del campo
            field_ttype = field_target.ttype
            # Obtención del título del campo
            field_label = field_target.label
            # Obtención de la función para obtención del atributo de la instancia de fila
            get_attribute_fn = self._adapter[field_ttype]
            # Obtención del valor del campo
            field_value = get_attribute_fn(field_label, record_data)
            # Se añade el valor al diccionario
            record[field_label] = field_value

        return record

    class Functions:

        def get_generic_value(
            self,
            label: str,
            row: Row,
        ) -> Any:

            # Obtención del valor de la fila de registro
            value = getattr(row, label)

            return value

        def get_datetime_value(
            self,
            label: str,
            row: Row,
        ) -> str | None:

            # Obtención del valor de la fila de registro
            value: str | None = getattr(row, label)

            if value is None:
                return value
            else:
                value = str(value).split('.')[0]

                return value

        def get_timedelta_value(
            self,
            label: str,
            row: Row,
        ) -> str | None:

            # Obtención del valor de la fila de registro
            value: str | None = getattr(row, label)

            if value is None:
                return value
            else:
                return str(value)

        def get_array_value(
            self,
            label: str,
            row: Row,
        ) -> list[int]:

            # Obtención del valor
            value: list[int | None] = getattr(row, label)

            if value == [None] or value is None:
                value: list[int] = []

            return value

        def get_m2o_value(
            self,
            label: str,
            row: Row,
        ) -> Many2One:

            # Construcción de los títulos para obtención de los valores
            id_label = f'{label}{FIELD_SUFFIX.ID}'
            name_label = f'{label}{FIELD_SUFFIX.NAME}'

            # Obtención del valor de ID
            id_value: MaybeNone[int] = getattr(row, id_label)

            # Si el valor es None...
            if id_value is None:
                return None

            # Obtención del valor del nombre
            name_value: str = getattr(row, name_label)
            # Construcción del valor completo
            value = [id_value, name_value]

            return value
