from typing import Callable, Literal
from ..._core import (
    _BaseAutomations,
    _Lylac,
)
from ..._data import preset_automations
from ..._module_types import (
    AutomationDataModel,
    CriteriaStructure,
    DataPerRecord,
    DataPerTransaction,
    RecordData,
    AutomationTemplate,
    ModificationTransaction,
    Transaction,
)
from ._module_types import (
    AutomationsHub,
    ProgrammedAutomation,
)
from ._submodules import (
    _Automations,
)

class Automations(_BaseAutomations):

    # Inicialización de estructura central de automatizaciones
    _hub: AutomationsHub = {}

    def __init__(
        self,
        instance: _Lylac,
    ) -> None:

        # Asignación de la instancia principal
        self._main = instance

        # Referencia del módulo de estructura interna
        self._strc = instance._strc

        # Inicialización del submódulo de automatizaciones
        self._m_automations = _Automations(self)

        # Creación de desencadenantes de automatización vacíos por cada tabla existente en la base de datos
        for model_name in self._strc.models.keys():
            self.register_model(model_name)

    def register_automation(
        self,
        model_name: str,
        transaction: Transaction,
        callback: AutomationTemplate,
        fields: list[str] = ['id',],
        criteria: CriteriaStructure = [],
        execution: Literal['record', 'all'] = 'record'
    ) -> None:

        # Creación de la automatización programada
        prog_autom: ProgrammedAutomation = {
            'criteria': criteria,
            'callback': callback,
            'fields': fields,
            'execution': execution,
        }

        # Se añade la automatización programada en la transacción correspondiente de su tabla
        self._hub[model_name][transaction].append(prog_autom)

    def run_after_transaction(
        self,
        model_name: str,
        transaction: ModificationTransaction,
        record_ids: list[int],
    ) -> None:

        # Se inicializa la lista de automatizaciones a ejecutar
        callbacks_to_run: list[Callable[[], None]] = []

        # Iteración por cada automatización programada
        for prog_autom in self._hub[model_name][transaction]:

            # Obtención del criterio de evaluación de la automatización programada
            automation_criteria = prog_autom['criteria']

            # Se crea un criterio de búsqueda segmentando solo por las IDs de registros a evaluar
            criteria = self._create_validation(record_ids, automation_criteria)

            # Se filtran las IDs por el criterio de búsqueda
            found_ids = self._main.search(model_name, criteria)

            # Si existen IDs para ejecutar la automatización
            if len(found_ids):

                # Inicialización de la función que ejecuta la automatización únicamente con las IDs encontradas
                automation_to_execute = self._build_runable_modification_automation(
                    model_name,
                    found_ids,
                    prog_autom,
                    transaction,
                )

                # Se añade la función preparada
                callbacks_to_run.append(automation_to_execute)

        # Ejecución de las automatizaciones
        for callback in callbacks_to_run:
            callback()

    def generate_before_transaction(
        self,
        model_name: str,
        record_ids: list[int],
    ):

        # Se inicializa la lista de automatizaciones a ejecutar
        callbacks_to_run: list[Callable[[list[int]], None]] = []

        # Iteración por cada automatización programada
        for prog_autom in self._hub[model_name]['delete']:

            # Obtención del criterio de evaluación de la automatización programada
            automation_criteria = prog_autom['criteria']

            # Obtención del criterio de búsqueda segmentado solo por las IDs de registros a evaluar
            criteria = self._create_validation(record_ids, automation_criteria)

            # Se filtran las IDs por el criterio de búsqueda
            found_ids = self._main.search(model_name, criteria)

            # Si existen IDs para ejecutar la automatización
            if len(found_ids):

                # Inicialización de la función que ejecuta la automatización únicamente con las IDs encontradas
                automation_to_execute = self._build_runable_deletion_automation(
                    model_name,
                    found_ids,
                    prog_autom,
                )

                # Se añade la función preparada
                callbacks_to_run.append(automation_to_execute)

        # Inicialización de función ejecutable
        def run_automations_after_deletion(deleted_ids: list[int]) -> None:
            for callback in callbacks_to_run:
                callback(deleted_ids)

        # Retorno de función de función ejecutable
        return run_automations_after_deletion

    def create_preset_automations(
        self,
    ) -> None:

        # Registro de las automatizaciones precargadas
        for automation in [ AutomationDataModel(**data) for data in preset_automations ]:

            # Obtención del módulo que contiene la automatización
            submodule = getattr(self._main, automation.submodule)
            # Obtención de la instancia de automatizaciones del submódulo
            autom_extension = getattr(submodule, '_m_automations')
            # Obtención de la función a registrar como automatización
            callback: Callable[[DataPerRecord | DataPerTransaction], None] = getattr(autom_extension, automation.callback)

            # Registro de la automatización
            self.register_automation(
                automation.model,
                automation.transaction,
                callback,
                automation.fields,
                automation.criteria,
                automation.execution
            )

    def _build_runable_modification_automation(
        self,
        model_name: str,
        found_ids: list[int],
        prog_autom: ProgrammedAutomation,
        transaction: ModificationTransaction,
    ):

        # Inicialización de datos de registros mapeados
        mapped_data: dict[int, RecordData] = {}

        # Se obtienen los datos de los registros
        records_data = self._main.read(model_name, found_ids, prog_autom['fields'], output_format= 'dict', only_ids_in_relations= True)

        # Mapeo de datos de registros
        for record_data in records_data:
            mapped_data[record_data['id']] = record_data

        # Inicialización de la función para ejecución de las automatizaciones
        def automation_to_execute():

            # Si el tipo de ejecución es por registro
            if prog_autom['execution'] == 'record':
                # Ejecución de automatización por registro
                for record_id in found_ids:
                    record_data = mapped_data[record_id]
                    prog_autom['callback'](DataPerRecord(id= record_id, record_data= record_data, transaction= transaction))
                    print(f'La automatización [{prog_autom['callback'].__name__}] se ha ejecutado con el registro {record_id}')
            # Ejecución por toda la lista de registros provistos
            else:
                prog_autom['callback'](DataPerTransaction(found_ids, records_data, transaction))

        # Retorno de la función para ejecutar las automatizaciones
        return automation_to_execute

    def _funnel_individua_records(
        self,
        records_data: list[RecordData],
    ) -> list[DataPerRecord]:

        # Creación de los objetos
        return [ DataPerRecord(id= record_data['id'], record_data= record_data) for record_data in records_data ]

    def _build_runable_deletion_automation(
        self,
        model_name: str,
        found_ids: list[int],
        prog_autom: ProgrammedAutomation,
    ):

        # Inicialización de datos de registros mapeados
        mapped_data: dict[int, RecordData] = {}

        # Se obtienen los datos de los registros
        records_data = self._main.read(model_name, found_ids, prog_autom['fields'], output_format= 'dict', only_ids_in_relations= True)

        # Mapeo de datos de registros
        for record_data in records_data:
            mapped_data[record_data['id']] = record_data

        def automation_to_execute(deleted_ids: list[int]):

            # Se inicializa una lista con las IDs que solo aplican
            applyable_ids = list( set(found_ids) & set(deleted_ids) )

            if prog_autom['execution'] == 'record':
                for record_id in applyable_ids:
                    record_data = mapped_data[record_id]

                    prog_autom['callback'](DataPerRecord(id= record_id, record_data= record_data, transaction= 'delete'))
            else:
                prog_autom['callback'](DataPerTransaction(applyable_ids, records_data, 'delete'))

        return automation_to_execute

    def register_model(
        self,
        table: str,
    ) -> None:

        self._hub[table] = {
            'create': [],
            'update': [],
            'delete': [],
        }

    def _create_validation(
        self,
        record_ids: list[int],
        aut_criteria: CriteriaStructure
    ) -> CriteriaStructure:

        if len(aut_criteria):
            return self._main.and_(
                [('id', 'in', record_ids)],
                aut_criteria
            )
        else:
            return [('id', 'in', record_ids)]
