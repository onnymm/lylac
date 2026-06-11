from typing import Any
from dataclasses import dataclass
from .._typing.type_parameters import _R

@dataclass(slots= True)
class ErrorDetail:
    value: Any
    record: _R
    message_to_show: str
    show_error_data: bool = True

    def __repr__(
        self,
    ) -> str:

        show_error_data = (
            f'\nLos datos con error son: [{self.record}].'
                if self.show_error_data
                else ''
        )

        # Construcción de mensaje
        message = f'{self.message_to_show}{show_error_data}'

        return message
