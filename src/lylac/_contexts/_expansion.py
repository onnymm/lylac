from typing import TYPE_CHECKING
from .._contracts.contexts import Contract_ExecutionContext
from .._resources import FieldExpansionSpecs
from .._typing.generics import ModelName
from .._typing.generics import _Record
from .._typing.structures import FrameReadField
from .._typing.structures import FieldReadDeclaration
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._orchestrator import CRUD

class ExpansionContext:

    def __init__(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        crud: CRUD,
    ) -> None:

        # Asignación de valores
        self._crud = crud
        self._execution_ctx = execution_ctx

        self.related_fields: list[FieldExpansionSpecs] = []

    def intercept(
        self,
        fields: list[FieldReadDeclaration],
    ) -> list[FrameReadField]:

        # Inicialización de lista de campos a retornar
        normalized_references: list[FrameReadField] = []

        for field in fields:
            # Comprobación de estructura de tupla
            if isinstance(field, tuple):
                # Se conservan tuplas de dos elementos
                if len(field) == 2:
                    # Obtención de ambos valores
                    ( field_reference, field_expansion_or_alias ) = field
                    # Si el segundo valor es un nombre...
                    if isinstance(field_expansion_or_alias, str):
                        # Reasignación de alias
                        field_alias = field_expansion_or_alias

                        # Si el primer valor es una tupla...
                        if isinstance(field_reference, tuple):
                            # Obtención de referencia y valor de expansión
                            ( reference, expansion ) = field_reference

                        # Si el primer valor es un nombre, esto es un alias
                        else:
                            # Se descarta
                            normalized_references.append(field)
                            continue

                    # Si el segundo valor es la expansión de relación...
                    else:
                        # Obtención de la referencia de campo
                        reference: str = field_reference
                        # Obtención del valor de expansión
                        expansion = field_expansion_or_alias
                        # Generación de un alias con el mismo nombre
                        field_alias = reference
                # Se descartan computaciones de campo
                else:
                    normalized_references.append(field)
                    continue
            # Se descartan valores que no sean tuplas
            else:
                normalized_references.append(field)
                continue

            # Construcción de objeto
            spec = FieldExpansionSpecs(reference, expansion, field_alias)
            # Se guardan los datos
            self.related_fields.append(spec)
            # Se añade un reemplazo que ya no incluye referencia de expansión
            normalized_references.append((reference, field_alias))

        print(self.related_fields)

        return normalized_references

    def resolve(
        self,
        model_name: ModelName[_M],
        data: list[_Record],
    ) -> list[_Record]:

        # Iteración por cada campo a expandir
        for field_to_expand in self.related_fields:
            # Obtención de propiedades de los campos del modelo
            fields_properties = self._execution_ctx.database_metadata.get_relation_fields_properties(model_name)
            # Se convierten en mapa
            fields_properties = {
                fields_properties_i.name: fields_properties_i
                for fields_properties_i
                in fields_properties
            }
            # Obtención del modelo relacionado del campo a expandir
            related_model_name = fields_properties[field_to_expand.name].related_model_name
            # Declaración de campos a leer
            fields_to_read = (
                []
                if field_to_expand.spec == True
                else field_to_expand.spec
            )

            # Lectura de los registros relacionados
            data = self._read(
                related_model_name,
                field_to_expand.alias,
                data,
                fields_to_read,
            )

        return data

    def _read(
        self,
        model_name: ModelName[_M],
        field_alias: str,
        data: list[_Record],
        records_fields_to_read: list[FrameReadField],
    ) -> list[_Record]:

        # Inicialización de conjunto de IDs de registros
        record_ids = set[int]()

        # Iteración por cada registro
        for record in data:
            # Obtención de lista de IDs del campo
            record_record_ids: list[int] = record[field_alias]
            # Se añaden las IDs al conjunto a leer
            record_ids |= set(record_record_ids)

        # Lectura de registros
        expanded_records = self._crud.read(self._execution_ctx, model_name, list(record_ids), records_fields_to_read)

        # Se mapean los registros para despacho
        mapped_related_records = {
            expanded_record['id']: expanded_record
            for expanded_record
            in expanded_records
        }

        # Iteración por cada registro
        for record in data:
            # Inicialización de lista de registros expandidos
            expanded_related_records: list[_Record] = []
            # Obtención de lista de IDs del campo
            record_record_ids: list[int] = record[field_alias]
            # Iteración por cada ID de registro
            for record_id in record_record_ids:
                # Obtención del registro
                expanded_record = mapped_related_records[record_id]
                # Se añade éste a la nueva lista
                expanded_related_records.append(expanded_record)

            # Sobreescritura
            record[field_alias] = expanded_related_records

        return data
