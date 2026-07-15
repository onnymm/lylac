from datetime import date
from datetime import datetime
from datetime import time
from typing import Any
from typing import Callable
from .._constants import TTYPE_NAME
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
            TTYPE_NAME.INTEGER: self._functions.bypass,
            TTYPE_NAME.CHAR: self._functions.bypass,
            TTYPE_NAME.BOOLEAN: self._functions.bypass,
            TTYPE_NAME.FLOAT: self._functions.bypass,
            TTYPE_NAME.SELECTION: self._functions.bypass,
            TTYPE_NAME.DATE: self._functions.parse_date,
            TTYPE_NAME.TIME: self._functions.parse_time,
            TTYPE_NAME.DATETIME: self._functions.parse_datetime,
            TTYPE_NAME.DURATION: self._functions.bypass,
            TTYPE_NAME.MANY2ONE: self._functions.bypass,
            TTYPE_NAME.TEXT: self._functions.bypass,
            TTYPE_NAME.FILE: self._functions.bypass,
            TTYPE_NAME.JSON: self._functions.bypass,
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
            # Si el tipo de dato es one2many o many2many
            if ttype in [TTYPE_NAME.ONE2MANY, TTYPE_NAME.MANY2MANY]:
                # Se continúa con la siguiente iteración
                continue

            # Si el tipo de dato es many2one y es creación...
            if ttype == TTYPE_NAME.MANY2ONE and isinstance(record[field_name], dict):
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
