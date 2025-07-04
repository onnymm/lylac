from ._base_base_lylac import BaseBaseLylac

class BaseAuth():
    _main: BaseBaseLylac

    def identify_user(
        self,
        token: str,
    ) -> int:
        ...
