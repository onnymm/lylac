from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._module_types import ModelName
from ._base import FieldsGetter_Spec

class Index_Interface():

    def __getitem__(
        self,
        model: ModelName | type[DeclarativeBase],
    ) -> FieldsGetter_Spec:
        ...
