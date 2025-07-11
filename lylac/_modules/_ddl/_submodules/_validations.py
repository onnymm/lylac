from typing import Any
from ...._core.modules import DDL_Core
from ...._module_types import (
    CriteriaStructure,
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
        # Asignación de instancia de algoritmos
        self._algorythms = instance._main._algorythms

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

    def unique_relation_on_one2many(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Obtención de la ID del modelo relacionado
        related_model_id = params.data['related_model_id']
        # Obtención del nombre del modelo relacionado
        related_field = params.data['related_field']
        # Creación del filtro
        search_criteria: CriteriaStructure = [
            '&',
                ('related_model_id', '=', related_model_id),
                ('related_field', '=', related_field)
        ]
        # Búsqueda de resultados
        found_ids = self._main.search(self._main._TOKEN, 'base.model.field', search_criteria)
        # Si ya existen registros...
        if found_ids:
            # Se retona True para arrojar el error
            return True

    def unique_relation_on_one2many_in_incomig_data(
        self,
        params: Validation.Create.Group.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Búsqueda de duplicados
        duplicated_records = self._algorythms.find_duplicates(
            params.data,
            lambda record: ( record['related_model_id'], record['related_field'] ),
        )
        # Si existen duplicados...
        if duplicated_records:
            # Se retornan éstos
            return duplicated_records

    def validate_related_field_existence_on_related_field(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Obtención de la ID del modelo relacionado
        related_model_id = params.data['related_model_id']
        # Obtención del nombre del modelo relacionado
        related_field = params.data['related_field']
        # Creación del filtro
        search_criteria: CriteriaStructure = [
            '&',
                ('model_id', '=', related_model_id),
                ('name', '=', related_field)
        ]
        # Búsqueda del campo
        found_id = self._main.search(self._main._TOKEN, 'base.model.field', search_criteria)
        # Si no se encontraron resultados...
        if not found_id:
            # Se retona True para arrojar el error
            return True

    def many2one_ttype_only_on_one2many_related_field(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Obtención de la ID del modelo relacionado
        related_model_id = params.data['related_model_id']
        # Obtención del nombre del modelo relacionado
        related_field = params.data['related_field']
        # Creación del filtro
        search_criteria: CriteriaStructure = [
            '&',
                ('model_id', '=', related_model_id),
                ('name', '=', related_field)
        ]
        # Búsqueda del registro
        [ field_id ] = self._main.search(self._main._TOKEN, 'base.model.field', search_criteria)
        # Obtención del tipo de dato
        ttype = self._main.get_value(self._main._TOKEN, 'base.model.field', field_id, 'ttype')
        # Si el tipo de dato del campo no es many2one...
        if ttype != 'many2one':
            # Se retona True para arrojar el error
            return True

    def bilateral_relationship_on_one2many_and_many2one(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:

        # Obtención del modelo al que pertenecerá el campo a crear
        model_id = params.data['model_id']
        # Obtención de la ID del modelo relacionado
        related_model_id = params.data['related_model_id']
        # Obtención del nombre del campo relacionado
        related_field = params.data['related_field']
        # Creación del filtro
        search_criteria: CriteriaStructure = [
            '&',
                ('model_id', '=', related_model_id),
                ('name', '=', related_field)
        ]
        # Búsqueda del registro
        [ field_id ] = self._main.search(self._main._TOKEN, 'base.model.field', search_criteria)
        # Obtención del modelo relacionado del campo relacionado
        related_field_related_model_id = self._main.get_value(self._main._TOKEN, 'base.model.field', field_id, 'related_model_id')
        # Si el modelo relacionado del campo relacionado no es el mismo...
        if related_field_related_model_id != model_id:
            # Se retona True para arrojar el error
            return True
