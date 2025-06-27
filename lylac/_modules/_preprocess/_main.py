from ..._core import _Lylac
from ..._module_types import RecordData

class Preprocess():

    def __init__(
        self,
        instance: _Lylac
    ):

        # Asignación de la instancia principal
        self._main = instance
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc

    def process_data_on_create(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> list[RecordData]:

        if 'create_uid' in self._strc.get_model_field_names(model_name):
            for record in data:
                # Escritura de usuario de creación y modificación
                record['create_uid'] = 1
                record['write_uid'] = 1

    def process_data_on_update(
        self,
        model_name: str,
        record: RecordData,
    ) -> RecordData:

        if 'write_uid' in self._strc.get_model_field_names(model_name):
            # Escritura de usuario de modificación
            record['write_uid'] = 1
