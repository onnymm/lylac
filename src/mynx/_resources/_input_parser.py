from datetime import date
from datetime import datetime
from datetime import time
from typing import Any
from typing import Callable
from .._typing.generics import _Record
from .._typing.literals import TTypeName
from .._typing.structures import RecordData
from .._typing.structures import JSONLike

class InputParser:

    def __init__(
        self,
        field_ttypes: dict[str, TTypeName],
    ) -> None:

        # Asignación de tipos de dato de campos
        self._field_ttypes = field_ttypes
        # Inicialización de subclase
        self._functions = self.Functions()

        # Inicialización de adaptador
        self._adapter: dict[TTypeName, Callable[[Any], int | str | float | bool | date | time | datetime | JSONLike]] = {
            'integer': self._functions.bypass,
            'char': self._functions.bypass,
            'boolean': self._functions.bypass,
            'float': self._functions.bypass,
            'selection': self._functions.bypass,
            'date': self._functions.parse_date,
            'time': self._functions.parse_time,
            'datetime': self._functions.parse_datetime,
            'duration': self._functions.bypass,
            'many2one': self._functions.bypass,
            'text': self._functions.bypass,
            'file': self._functions.bypass,
            'json': self._functions.bypass,
        }

    def parse(
        self,
        record: RecordData,
    ) -> _Record:

        # Inicialización de diccionario de registro parseado
        parsed_record = {}

        # Iteración por cada campo en el registro
        for field_name in record:
            # Obtención del tipo de dato del campo
            ttype = self._field_ttypes[field_name]
            # SI el tipo de dato es one2many o many2many
            if ttype in ['one2many', 'many2many']:
                # Se continúa con la siguiente iteración
                continue

            # Obtención del valor del registro
            value = record[field_name]

            # Parseo del valor y almacenamiento en el diccionario de registro parseado
            parsed_record[field_name] = self._adapter[ttype](value)

        return parsed_record

    class Functions:

        def bypass(
            self,
            value: Any,
        ) -> Any:

            return value

        def parse_date(
            self,
            value: date | str,
        ) -> date:

            if isinstance(value, str):
                return date.fromisoformat(value)

        def parse_time(
            self,
            value: time | str,
        ) -> time:

            if isinstance(value, str):
                return time.fromisoformat(value)

        def parse_datetime(
            self,
            value: datetime | str,
        ) -> datetime:

            if isinstance(value, str):
                return datetime.fromisoformat(value)
