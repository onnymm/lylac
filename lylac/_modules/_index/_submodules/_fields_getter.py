from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from ...._core import (
    BaseFieldsGetter,
    BaseIndex,
    _Lylac,
)

class _FieldsGetter(BaseFieldsGetter):

    def __init__(
        self,
        instance: BaseIndex,
    ) -> None:

        # Asignación de instancia propietaria
        self._index = instance

    def __getitem__(
        self,
        field_name: str,
    ) -> InstrumentedAttribute:

        # Obtención de instancia del campo solicitado
        field_instance = self._index._models.get_table_field(
            self._available_model,
            field_name,
        )

        return field_instance
