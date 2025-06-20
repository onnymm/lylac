from typing import (
    Literal,
    Tuple,
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_api import DeclarativeBase
from ._base import (
    BaseFieldsGetter,
    BaseModels,
)
from ._base_base_lylac import BaseBaseLylac

class BaseIndex():
    _main: BaseBaseLylac
    _models: BaseModels

    def __getitem__(
        self,
        model: str | type[DeclarativeBase],
    ) -> BaseFieldsGetter:
        ...
