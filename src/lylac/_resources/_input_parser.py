from datetime import date
from datetime import datetime
from datetime import time
from typing import Any
from typing import Callable
from typing import Union
from .._constants import TTYPE_NAME
from .._typing.aliases import FieldName
from .._typing.aliases import DMLScalarCompatible
from .._typing.generics import _Record
from .._typing.literals import TTypeName
from .._typing.structures import InputRecordData
from .._typing.structures import JSONLike
from .._typing.structures import ParsedFromInput
from .._typing.structures import RelationCommands
from .._typing.type_parameters import _T

ParsedDataType = Union[DMLScalarCompatible, JSONLike]

class ParseCallback:

    @classmethod
    def bypass(
        cls,
        value: _T,
    ) -> _T:
        return value

    @classmethod
    def parse_date(
        cls,
        value: date | str,
    ) -> date:
        # Si el valor es cadena de texto...
        if isinstance(value, str):
            # Parseo a fecha
            return date.fromisoformat(value)

    @classmethod
    def parse_time(
        cls,
        value: time | str,
    ) -> time:
        # Si el valor es cadena de texto...
        if isinstance(value, str):
            # Parseo a hora
            return time.fromisoformat(value)

    @classmethod
    def parse_datetime(
        cls,
        value: datetime | str,
    ) -> datetime:
        # Si el valor es cadena de text...
        if isinstance(value, str):
            # Parseo a fecha y hora
            return datetime.fromisoformat(value)

class InputParser:
    _ADAPTER: dict[TTypeName, Callable[[Union[DMLScalarCompatible, JSONLike, RelationCommands, InputRecordData[Any]]], ParsedFromInput]] = {
        TTYPE_NAME.INTEGER: ParseCallback.bypass,
        TTYPE_NAME.CHAR: ParseCallback.bypass,
        TTYPE_NAME.BOOLEAN: ParseCallback.bypass,
        TTYPE_NAME.FLOAT: ParseCallback.bypass,
        TTYPE_NAME.SELECTION: ParseCallback.bypass,
        TTYPE_NAME.DATE: ParseCallback.parse_date,
        TTYPE_NAME.TIME: ParseCallback.parse_time,
        TTYPE_NAME.DATETIME: ParseCallback.parse_datetime,
        TTYPE_NAME.DURATION: ParseCallback.bypass,
        TTYPE_NAME.MANY2ONE: ParseCallback.bypass,
        TTYPE_NAME.TEXT: ParseCallback.bypass,
        TTYPE_NAME.FILE: ParseCallback.bypass,
        TTYPE_NAME.JSON: ParseCallback.bypass,
    }

    def __init__(
        self,
        field_ttypes: dict[FieldName, TTypeName],
    ) -> None:

        # Asignación de tipos de dato de campos
        self._field_ttypes = field_ttypes

    def parse(
        self,
        record: InputRecordData[Any],
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

            # Obtención del valor del registro
            value = record[field_name]

            # Parseo del valor y almacenamiento en el diccionario de registro parseado
            parsed_record[field_name] = self._ADAPTER[ttype](value)

        return parsed_record
