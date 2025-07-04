from ...._core import BaseAutomations
from .._module_types import ProgrammedAutomation
from ...._module_types import (
    CreateOrUpdateTransaction,
    RecordData,
    DataPerRecord,
    DataPerTransaction,
)
from .._module_types import (
    CompiledDeletionAutomation,
    CompiledModificationAutomation,
)

class _Builder():

    def __init__(
        self,
        instance: BaseAutomations,
    ):

        # Asignación de la instancia propietaria
        self._automations = instance
        # Asignación de la instancia principal
        self._main = instance._main

    def build_runable_modification_automation(
        self,
        model_name: str,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
        transaction: CreateOrUpdateTransaction,
    ) -> CompiledModificationAutomation:

        # Obtención de mapa de información de los registros
        mapped_data = self._get_records_data_for_automation(
            model_name,
            found_ids,
            autom_data,
        )

        # Inicialización de la función para ejecución de las automatizaciones
        def automation_to_execute():

            # Obtención de la función de automatización a ejecutar
            automation_callback = autom_data['callback']

            # Si el tipo de ejecución es por registro
            if autom_data['execution'] == 'record':
                # Ejecución de automatización por registro
                for record_id in found_ids:
                    # Obtención del registro a usar para entrada de argumentos a la automatización
                    input_record = mapped_data[record_id]
                    # Creación del objeto a ingresar a la automatización
                    data = DataPerRecord(
                        id= record_id,
                        record_data= input_record,
                        transaction= transaction
                    )
                    # Ejecución de la automatización
                    automation_callback(data)
                    # Notificación de ejecución de la automatización
                    print(f'La automatización [{automation_callback.__name__}] se ha ejecutado con el registro {record_id}')

            # Ejecución por toda la lista de registros provistos
            else:
                # Creación del objeto a ingresar a la automatización
                data = DataPerTransaction(
                    ids= found_ids,
                    records_data= mapped_data.values(),
                    transaction= transaction
                )
                # Ejecución de la automatización
                automation_callback(data)

        # Retorno de la función para ejecutar las automatizaciones
        return automation_to_execute

    def build_runable_deletion_automation(
        self,
        model_name: str,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
    ) -> CompiledDeletionAutomation:

        # Obtención de mapa de información de los registros
        mapped_data = self._get_records_data_for_automation(
            model_name,
            found_ids,
            autom_data,
        )

        def automation_to_execute(deleted_ids: list[int]):

            # Se inicializa una lista con las IDs que solo aplican
            applyable_ids = list( set(found_ids) & set(deleted_ids) )

            if autom_data['execution'] == 'record':
                for record_id in applyable_ids:
                    record_data = mapped_data[record_id]

                    autom_data['callback'](DataPerRecord(id= record_id, record_data= record_data, transaction= 'delete'))
            else:
                autom_data['callback'](DataPerTransaction(applyable_ids, mapped_data.values(), 'delete'))

        return automation_to_execute

    def _get_records_data_for_automation(
        self,
        model_name: str,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
    ) -> dict[int, RecordData]:

        # Inicialización de datos de registros mapeados
        mapped_data: dict[int, RecordData] = {}
        # Se obtienen los datos de los registros
        records_data = self._main.read(
            model_name,
            found_ids,
            autom_data['fields'],
            output_format= 'dict',
            only_ids_in_relations= True,
        )

        # Mapeo de datos de registros
        for record_data in records_data:
            # Se indexan los datos de cada registro por medio de su ID
            mapped_data[ record_data['id'] ] = record_data

        return mapped_data

