from typing import Any
from ...._core.modules import DDL_Core
from ...._module_types import (
    ModelRecordData,
    Validation,
)

class _Validations():
    _ddl: DDL_Core

    def __init__(
        self,
        instance: DDL_Core,
    ) -> None:

        # Asignación de instancia propietaria
        self._ddl = instance
        # Asignación de instancia principal
        self._main = instance._main

    def reject_related_model_on_single_ttype(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Si el tipo de dato del campo no es relacionado...
        if params.data['ttype'] not in ['many2one', 'one2many', 'many2many']:
            # Si existe un modelo relacionado...
            if params.data.get('related_model_id') is not None:
                # Se retorna True para arrojar el error
                return True

    def reject_related_field_on_single_ttype(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Si el tipo de dato del campo no es relacionado...
        if params.data['ttype'] not in ['many2one', 'one2many', 'many2many']:
            # Si existe un modelo relacionado...
            if params.data.get('related_field') is not None:
                # Se retorna True para arrojar el error
                return True

    def mandatory_related_model_on_many2one_ttype(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Si el tipo de dato del campo no es relacionado...
        if params.data['ttype'] == 'many2one':
            # Si existe un modelo relacionado...
            if params.data.get('related_model_id') is None:
                # Se retorna True para arrojar el error
                return True

    def reject_related_field_on_many2one_ttype(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Si el tipo de dato del campo no es relacionado...
        if params.data['ttype'] == 'many2one':
            # Si existe un modelo relacionado...
            if params.data.get('related_field') is not None:
                # Se retorna True para arrojar el error
                return True

    def mandatory_related_model_on_one2many_ttype(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Si el tipo de dato del campo no es relacionado...
        if params.data['ttype'] == 'one2many':
            # Si existe un modelo relacionado...
            if params.data.get('related_model_id') is None:
                # Se retorna True para arrojar el error
                return True

    def mandatory_related_field_on_one2many_ttype(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Si el tipo de dato del campo no es relacionado...
        if params.data['ttype'] == 'one2many':
            # Si existe un modelo relacionado...
            if params.data.get('related_field') is None:
                # Se retorna True para arrojar el error
                return True

    def mandatory_related_model_on_many2many_ttype(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Si el tipo de dato del campo no es relacionado...
        if params.data['ttype'] == 'many2many':
            # Si existe un modelo relacionado...
            if params.data.get('related_model_id') is None:
                # Se retorna True para arrojar el error
                return True

    def reject_related_field_on_many2many_ttype(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Si el tipo de dato del campo no es relacionado...
        if params.data['ttype'] == 'many2many':
            # Si existe un modelo relacionado...
            if params.data.get('related_field') is not None:
                # Se retorna True para arrojar el error
                return True
