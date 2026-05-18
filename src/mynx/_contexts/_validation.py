from typing import Any
from typing import Generic
from .._contexts.engines import BaseContext
from .._contracts import _Contract_CRUD
from .._contracts.contexts import Contract_ExecutionContext
from .._resources import ErrorDetail
from .._resources import ModelDataIndex
from .._typing.generics import ModelName
from .._typing.generics import _Record
from .._typing.structures import CriteriaStructure
from .._typing.structures import TripletStructure
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R

class ValidationContext(Generic[_M, _R], BaseContext[_M]):
    model_name: ModelName[_M]
    records: list[_R]
    _message: str

    def __init__(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        crud: _Contract_CRUD[_M],
        model_name: ModelName[_M],
        records: list[_R],
        errors: list[ErrorDetail],
        message: str,
    ) -> None:

        # Asignación de valores
        self.model_name = model_name
        self.records = records
        self._crud = crud
        self._message = message
        self._errors = errors
        self._execution_ctx = execution_ctx

        # Inicialización de índice de datos de modelo
        self._model_data_index = ModelDataIndex(execution_ctx.conn)

    def catch(
        self,
        record: _R,
        value: Any = None,
        data: list[Any] = [],
    ) -> None:

        # Construcción de mensaje a mostrar
        message_to_show = self._message.format(value= value, data= data)
        # Inicialización de detalle de error
        detail = ErrorDetail(value, record, message_to_show)
        # Se añade el registro como error
        self._errors.append(detail)

    def find_duplicated_composite_keys(
        self,
        records: list[_Record],
        field_names_composite_key: list[str],
    ) -> list[_Record]:

        # Inicialización de lista de registros duplicados
        found_records: list[_Record] = []

        # Mientras la longitud de datos sea mayor a 0...
        while len(records) > 0:
            # Obtención de un registro i
            record_i = records.pop()
            # Indicadores de duplicidad
            duplicated_in_input = False
            duplicated_in_model = False
            # Iteración por por el resto de registros
            for record_j in records:

                # Indicador de duplicidad en comparación
                duplicated_in_input_i = True
                # Iteración por cada nombre de campo que forma la llave compuesta
                for field_name in field_names_composite_key:
                    # Si los valores de ambos registros son diferentes...
                    if record_i[field_name] != record_j[field_name]:
                        # Se apaga el indicador de duplicidad 
                        duplicated_in_input_i = False
                        # Se termina el ciclo
                        break

                # Si el indicador de duplicidad en comparación no se apagó...
                if duplicated_in_input_i:
                    # Se indica que el registro es duplicado
                    duplicated_in_input = True
                    # Se rompe el ciclo para no sobreescribir el valor en falso
                    break

            # Inicialización de criterio de búsqueda
            search_criteria: CriteriaStructure = []
            # Iteración por cada nombre de campo que forma la llave compuesta
            for field_name in field_names_composite_key:
                # Construcción de condición como tripleta
                condition: TripletStructure = (field_name, '=', record_i[field_name])
                # Si la longitud del criterio de búsqueda es 0...
                if len(search_criteria) == 0:
                    # Se añade la tripleta
                    search_criteria.append(condition)
                # Si la longitud del criterio de búsqueda no es 0...
                else:
                    # Se añade la tripleta en forma de AND
                    search_criteria = ['&', *search_criteria, condition]

            # Búsqueda de cantidad de registros que cumplen con las condiciones provistas
            count = self._crud.search_count(
                self._execution_ctx,
                self.model_name,
                search_criteria,
            )

            # Si fueron encontrados resultados...
            if count:
                # Se enciende el indicador de duplicado en modelo
                duplicated_in_model = True
            # Si algún indicador de duplicidad está encendido...
            if duplicated_in_input or duplicated_in_model:
                # Se añade el registro a los registros duplicados encontrados
                found_records.append(record_i)

        return found_records
