from datetime import datetime
from typing import Any
from typing import Generic
from typing import Literal
from typing import overload

from sqlalchemy.orm import InstrumentedAttribute
from .._core import Metadata
from .._typing.aliases import ModelClass
from .._typing.generics import ModelName
from .._typing.generics import _ModelIndex
from .._typing.interfaces import Many2ManyRelation
from .._typing.type_parameters import _M

class ModelsBearer(Generic[_M]):
    _index: _ModelIndex[_M] = {
        'base.users': Metadata.BaseUsers,
        'base.user.session': Metadata.BaseUserSession,
        'base.model': Metadata.BaseModel,
        'base.model.field': Metadata.BaseModelField,
        'base.model.field.selection': Metadata.BaseModelFieldSelection,
        'base.model.data': Metadata.BaseModelData,
        'base.model.data.process': Metadata.BaseModelDataProcess,
        'base.model.data.process.step': Metadata.BaseModelDataProcessStep,
        'base.model.data.process.step.record': Metadata.BaseModelDataProcessStepRecord,
    }

    _m2m: dict[str, ModelClass] = {}

    def get_model(
        self,
        model_name: ModelName[_M],
    ) -> ModelClass:

        # Obtención de la clase del modelo
        model_model = self._index[model_name]

        return model_model

    def add_model(
        self,
        model_name: ModelName[_M],
        model_model: ModelClass,
    ) -> None:

        self._index[model_name] = model_model

    def discard_model(
        self,
        model_name: ModelName[_M],
    ) -> None:

        del self._index[model_name]

    def get_m2m_model(
        self,
        model_name: ModelName[_M],
        field_name: str,
    ) -> type[Many2ManyRelation]:

        # Obtención de nombre de tabla
        model_name = model_name.replace('.', '_')
        # Construcción de nombre de índice
        index_name = f'{model_name}__{field_name}'

        # Obtención de la clase del modelo
        model_model = self._m2m[index_name]

        return model_model

    def add_m2m_model(
        self,
        index: str,
        model_model: ModelClass,
    ) -> None:

        self._m2m[index] = model_model

    @overload
    def get_field_instance(
        self,
        model_name: ModelName[_M],
        field_name: Literal['id'],
    ) -> InstrumentedAttribute[int]:
        ...

    @overload
    def get_field_instance(
        self,
        model_name: ModelName[_M],
        field_name: Literal['name'],
    ) -> InstrumentedAttribute[str]:
        ...

    @overload
    def get_field_instance(
        self,
        model_name: ModelName[_M],
        field_name: Literal['create_date'],
    ) -> InstrumentedAttribute[datetime]:
        ...

    @overload
    def get_field_instance(
        self,
        model_name: ModelName[_M],
        field_name: Literal['update_date'],
    ) -> InstrumentedAttribute[datetime]:
        ...

    @overload
    def get_field_instance(
        self,
        model_name: ModelName[_M],
        field_name: Literal['create_uid'],
    ) -> InstrumentedAttribute[int]:
        ...

    @overload
    def get_field_instance(
        self,
        model_name: ModelName[_M],
        field_name: Literal['update_uid'],
    ) -> InstrumentedAttribute[int]:
        ...

    @overload
    def get_field_instance(
        self,
        model_name: ModelName[_M],
        field_name: str,
    ) -> InstrumentedAttribute[Any]:
        ...

    def get_field_instance(
        self,
        model_name: ModelName[_M],
        field_name: str,
    ) -> InstrumentedAttribute[Any]:

        # Obtención de clase del modelo
        model_model = self.get_model(model_name)
        # Obtención de instancia de campo
        field_instance: InstrumentedAttribute[Any] = getattr(model_model, field_name)

        return field_instance
