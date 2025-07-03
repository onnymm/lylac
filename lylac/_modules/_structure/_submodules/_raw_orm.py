from typing import Tuple
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import aliased
from ...._constants import (
    FIELD_NAME,
    MODEL_NAME,
)
from ...._core import (
    BaseStructure,
    _Lylac,
)
from ...._module_types import TType

class _RawORM():

    def __init__(
        self,
        instance: BaseStructure,
    ) -> None:

        # Asignación de instancia propietaria
        self._strc = instance
        # Asignación de instancia
        self._main: _Lylac = instance._main

    def get_model_fields(
        self,
        model_name,
    ) -> list[Tuple[str, TType, None | str, None | str]]:

        # Obtención de modelos base
        BaseModel = self._main._models.get_table_model(MODEL_NAME.BASE_MODEL)
        BaseModelField = self._main._models.get_table_model(MODEL_NAME.BASE_MODEL_FIELD)

        # Creación de alias de modelos
        FieldModel = aliased(BaseModel)
        RelatedModel = aliased(BaseModel)

        # Creación del query
        stmt = (
            select(
                self._main._index[BaseModelField]['name'],
                self._main._index[BaseModelField]['ttype'],
                self._main._index[RelatedModel]['model'],
                self._main._index[BaseModelField]['related_field'],
            )
            .outerjoin(
                FieldModel,
                self._main._index[BaseModelField]['model_id'] == self._main._index[FieldModel][FIELD_NAME.ID],
            )
            .outerjoin(
                RelatedModel,
                self._main._index[BaseModelField]['related_model_id'] == self._main._index[RelatedModel][FIELD_NAME.ID],
            )
            .where(
                self._main._index[FieldModel]['model'] == model_name
            )
        )

        # Ejecución del query
        response = self._main._connection.execute(stmt)

        return (
            [
                tuple(item) for item in (
                    pd.DataFrame(
                        response
                        .fetchall()
                    )
                    .T
                    .to_dict('list')
                    .values()
                )
            ]
        )
