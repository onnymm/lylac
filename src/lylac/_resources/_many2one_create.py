from typing import Generic
from typing import TYPE_CHECKING
from .._typing.generics import ModelName
from .._typing.structures import RecordData
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._contexts import ExecutionContext
    from .._orchestrator import CRUD

class Many2OneCreate(Generic[_M]):

    def __init__(
        self,
        crud: 'CRUD[_M]',
    ) -> None:

        self._crud = crud

    def resolve(
        self,
        execution_ctx: 'ExecutionContext[_M]',
        model_name: ModelName[_M],
        data: list[RecordData],
    ) -> list[RecordData]:

        if self._crud.PERMISSIONS_BYPASS:
            return data

        # Obtención de los nombres de los campos
        field_properties = execution_ctx.database_metadata.get_fields_properties_by_ttypes(model_name, ['many2one'])

        # Iteración por cada registro a crear
        for record in data:
            # Iteración por cada propiedad de campo many2one
            for field_property in field_properties:
                # Si el nombre del campo está en el registro a crear...
                if field_property.name in record:
                    # Si el valor es un diccionario de registro a crear...
                    if isinstance(record[field_property.name], dict):
                        # Obtención del modelo relacionado a usar
                        related_model_name = field_property.related_model_name
                        # Obtención de los datos del registro a crear
                        related_record_data = record[field_property.name]

                        # Creación de registro y obtención de ID
                        [ created_record_id ] = self._crud.create(
                            execution_ctx,
                            related_model_name,
                            related_record_data,
                        )

                        # Se asigna la ID creada al valor del campo
                        record[field_property.name] = created_record_id

        return data