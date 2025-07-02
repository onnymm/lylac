from sqlalchemy.engine.cursor import CursorResult
from ...._core import _Lylac

class _BaseOutput():
    _main: _Lylac

    def get_found_ids(
        self,
        response: CursorResult[int],
    ) -> list[int]:
        ...
