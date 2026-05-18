from typing import Any
from dataclasses import dataclass
from .._typing.type_parameters import _R

@dataclass(slots= True)
class ErrorDetail:
    value: Any
    record: _R
    message_to_show: str

    def __repr__(
        self,
    ) -> str:

        # Construcción de mensaje
        message = f'{self.message_to_show}\nLos datos con error son: [{self.record}].'

        return message
