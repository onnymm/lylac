from typing import Callable
import pandas as pd
from sqlalchemy import select, and_
from ...._module_types import TType
from ._base import _BaseOutput

class _RawORM():

    def __init__(
        self,
        instance: _BaseOutput,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance
        # Referencia de la instancia principal
        self._main = instance._main

    def get_fields_ttypes(
        self,
        model_name: str,
        fields: list[str],
    ) -> dict[str, TType]:

        # Obtención de la ID del modelo
        model_id = self._get_model_id(model_name)

        # Obtención del modelo BaseModelField
        BaseModelField = self._main._models.get_table_model('base.model.field')

        # Obtención de instancias de campo
        name_instance = self._main._models.get_table_field(BaseModelField, 'name')
        ttype_instance = self._main._models.get_table_field(BaseModelField, 'ttype')
        model_id_instance = self._main._models.get_table_field(BaseModelField, 'model_id')

        # Creación del query
        stmt = (
            select(name_instance, ttype_instance)
            .where(
                and_(
                    model_id_instance == model_id,
                    name_instance.in_(fields)
                )
            )
        )

        # Ejecución del query
        response = self._main._connection.execute(stmt)

        # Obtención de los datos
        data = pd.DataFrame(response.fetchall()).to_dict('records')

        return {field['name']: field['ttype'] for field in data}

    def _get_model_id(
        self,
        model_name: str
    ) -> None:
        
        # Obtención de la tabla BaseModel
        BaseModel = self._main._models.get_table_model('base.model')

        # Obtención de instancias de campo
        id_instance = self._main._models.get_table_field(BaseModel, 'id')
        model_instance = self._main._models.get_table_field(BaseModel, 'model')

        # Creación del query
        stmt = select(id_instance).where(model_instance == model_name)

        # Ejecución del query
        response = self._main._connection.execute(stmt)

        # Obtención de la ID de modelo
        model_id = int(
            pd.DataFrame(response.fetchall())
            .at[0, 'id']
        )

        return model_id
