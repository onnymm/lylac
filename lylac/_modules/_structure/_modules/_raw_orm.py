from typing import Any, Tuple
import pandas as pd
from sqlalchemy import inspect, select
from sqlalchemy.orm import DeclarativeBase, aliased
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty
from ...._core import (
    _Lylac,
    _BaseModels,
    _BaseStructure,
)
from ...._models import (
    BaseModel_,
    BaseModelField,
)
from ...._module_types import TType

class _RawORM():

    def __init__(
        self,
        instance: _BaseStructure,
    ) -> None:

        self._strc = instance

        self._main = instance._main

    def get_model_fields(
        self,
        model_name,
    ) -> list[Tuple[str, TType, None | str]]:

        # Creación de alias de modelos
        FieldModel = aliased(BaseModel_)
        RelatedModel = aliased(BaseModel_)

        # Creación del query
        stmt = (
            select(
                BaseModelField.name,
                BaseModelField.ttype,
                RelatedModel.model,
            )
            .outerjoin(
                FieldModel,
                BaseModelField.model_id == FieldModel.id,
            )
            .outerjoin(
                RelatedModel,
                BaseModelField.related_model_id == RelatedModel.id,
            )
            .where(
                FieldModel.model == model_name
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



    # def get_all_model_fields(
    #     self,
    #     model_name: str,
    #     fields: list[str] = [],
    # ) -> list[str]:

    #     filters = [BaseModel_.model == model_name]

    #     if len(fields) > 0:
    #         fields.append()

    #     # Creación de sentencia SQL
    #     stmt = (
    #         # Nombre del campo
    #         select(BaseModelField.name)
    #         # JOIN con el modelo de modelos
    #         .outerjoin(
    #             BaseModel_,
    #             BaseModelField.model_id == BaseModel_.id
    #         )
    #         # Filtro por los campos cuyo nombre de modelo vinculado sea el provisto
    #         .where(BaseModel_.model == model_name)
    #     )

    #     # Obtención de los datos
    #     response = self._main._connection.execute(stmt)

    #     # Transformación y retorno
    #     return (
    #         pd.DataFrame(response.fetchall())
    #         ['name']
    #         .to_list()
    #     )
