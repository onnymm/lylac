from typing import (
    Any,
    overload,
)
from sqlalchemy import (
    not_,
    or_,
    and_,
    Select,
    Update,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.elements import BinaryExpression
from ..._core import _Lylac
from ..._module_types import (
    _T,
    CriteriaStructure,
    TripletStructure,
    ComparisonOperator,
    LogicOperator,
)
from ._submodule_types import (
    ComparisonCallback,
    ConditionUnionCallback,
)

class Where():

    _comparison_operation: dict[ComparisonOperator, ComparisonCallback] = {
        '=': lambda field, value: field == value,
        '!=': lambda field, value: field != value,
        '>': lambda field, value: field > value,
        '>=': lambda field, value: field >= value,
        '<': lambda field, value: field < value,
        '<=': lambda field, value: field <= value,
        '><': lambda field, value: field.between(value[0], value[1]),
        'in': lambda field, value: field.in_(value),
        'not in': lambda field, value: field.not_in(value),
        'ilike': lambda field, value: field.contains(value),
        'not ilike': lambda field, value: not_(field.contains(value)),
        '~': lambda field, value: field.regexp_match(value),
        '~*': lambda field, value: field.regexp_match(value, 'i'),
    }

    # Operaciones lógicas
    _logic_operation: dict[LogicOperator, ConditionUnionCallback] = {
        '|': lambda condition_1, condition_2: or_(condition_1, condition_2),
        '&': lambda condition_1, condition_2: and_(condition_1, condition_2),
    }

    def __init__(
        self,
        instance: _Lylac,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

    @overload
    def add_query(
        self,
        stmt: Select[_T],
        table_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> Select[_T]:
        ...

    @overload
    def add_query(
        self,
        stmt: Update[_T],
        table_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> Update[_T]:
        ...

    def add_query(
        self,
        stmt: Select[_T] | Update[_T],
        table_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ):

        # Creación del segmento WHERE en caso de haberlo
        if len(search_criteria) > 0:

            # Creación del query where
            query = self.build_where(table_model, search_criteria)

            # Conversión del query SQL
            stmt = stmt.where(query)

        # Retorno de la sentencia SQL
        return stmt

    def build_where(
            self,
            table: type[DeclarativeBase],
            search_criteria: CriteriaStructure
        ) -> BinaryExpression:

        # Si el criterio de búsqueda sólo contiene una tripleta 
        if len(search_criteria) == 1:
            # Destructuración de la tripleta
            [ triplet ] = search_criteria
            # Creación de query de condición individual
            return self._create_individual_query(table, triplet)

        # Iteración
        for i in range( len(search_criteria) ):
            # Creación de condiciones individuales para facilitar su lectura
            istriplet_1 = self._is_triplet(search_criteria[i])
            istriplet_2 = self._is_triplet(search_criteria[i + 1])
            istriplet_3 = self._is_triplet(search_criteria[i + 2])

            # Si sólo el primer valor es un operador lógico y los siguientes dos  son tripletas
            if not istriplet_1 and istriplet_2 and istriplet_3:
                # Destructuración de los valores
                ( op, condition_1, condition_2) = search_criteria[i: i + 3]

                # Retorno de la unión de las dos condiciones
                return self._merge_queries(
                    op,
                    self._create_individual_query(table, condition_1),
                    self._create_individual_query(table, condition_2)
                )

            # Si uno de los dos siguientes valores no es tripleta se tiene que generar una
            #   condición compleja, en dos diferentes escenarios:
            else:
                # Obtención del operador lógico
                op = search_criteria[i]

                # Si el primero de los dos siguientes valores es tripleta
                if istriplet_2:
                    # Unión de condiciones
                    return self._merge_queries(
                        op,
                        # Se convierte el primer siguiente valor en query SQL
                        self._create_individual_query(table, search_criteria[i + 1]),
                        # Se ejecuta esta función recursivamente para la evaluación del resto
                        #   de los valores del criterio de búsqueda
                        self.build_where(table, search_criteria[i + 2:])
                    )

                # Si el segundo de los dos siguientes valores es tripleta
                else:
                    # Unión de dos condiciones
                    return self._merge_queries(
                        op,
                        # Se ejecuta esta función recursivamente para la evaluación del
                        #   criterio de búsqueda a partir del siguiente primer valor hasta
                        #   el penúltimo valor del criterio de búsqueda
                        self.build_where(table, search_criteria[i + 1: -1]),
                        # Se convierte el último valor del criterio de búsqueda en query SQL
                        self._create_individual_query(table, search_criteria[-1])
                    )

    def _merge_queries(
        self,
        op: LogicOperator,
        condition_1: BinaryExpression,
        condition_2: BinaryExpression
    ) -> BinaryExpression:

        # Retorno de la unión de los dos queries
        return self._logic_operation[op](condition_1, condition_2)

    def _create_individual_query(
        self,
        table: type[DeclarativeBase],
        fragment: TripletStructure
    ) -> BinaryExpression:

        # Destructuración de valores
        ( field_instance, op, value ) = fragment

        # Obtención de la instancia del campo a usar
        field_instance = self._main._models.get_table_field(table, field_instance)

        # Retorno de la evaluación
        return self._comparison_operation[op](field_instance, value)

    def _is_triplet(
        self, value: Any
    ) -> bool:
        """
        ## Evaluación de posible tripleta de condición
        Esta función evalúa si el valor provisto es una tupla o una lista de
        3 valores que puede ser convertida a un query SQL.
        """
        return (
                isinstance(value, tuple) or isinstance(value, list)
            and 
                len(value) == 3
        )
