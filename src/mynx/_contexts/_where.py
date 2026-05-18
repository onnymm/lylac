from typing import Callable
from typing import Generic
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy import and_
from sqlalchemy import not_
from sqlalchemy import or_
from .._constants import ERROR_LABEL
from .._contracts.contexts import Contract_FrameContext
from .._contracts.contexts import Contract_WhereContext
from .._typing.structures import CriteriaStructure
from .._typing.structures import TripletStructure
from .._typing.structures import ComparisonOperator
from .._typing.structures import LogicOperator
from .._typing.structures import RecordValue
from .._typing.type_parameters import _M

class WhereContext(Generic[_M], Contract_WhereContext[_M]):
    _comparison_expression: dict[ComparisonOperator, Callable[[InstrumentedAttribute, RecordValue], BinaryExpression]] = {
        '=': lambda field_instance, value: field_instance == value,
        '!=': lambda field, value: field != value,
        '>': lambda field, value: field > value,
        '>=': lambda field, value: field >= value,
        '<': lambda field, value: field < value,
        '<=': lambda field, value: field <= value,
        'in': lambda field, value: field.in_(value),
        'not in': lambda field, value: field.not_in(value),
        'ilike': lambda field, value: field.contains(value),
        'not ilike': lambda field, value: not_(field.contains(value)),
        '~': lambda field, value: field.regexp_match(value),
        '~*': lambda field, value: field.regexp_match(value, 'i'),
    }
    _logic_expression: dict[LogicOperator, Callable[[BinaryExpression, BinaryExpression], BinaryExpression]] = {
        '&': lambda a, b: and_(a, b),
        '|': lambda a, b: or_(a, b),
    }

    def __init__(
        self,
        frame_ctx: Contract_FrameContext[_M],
    ) -> None:

        # Asignación de instancia de contexto de frame
        self._frame_ctx = frame_ctx

    def build_conditions(
        self,
        search_criteria: CriteriaStructure,
    ) -> BinaryExpression | BooleanClauseList:

        # Si el criterio de búsqueda solo tiene un elemento...
        if len(search_criteria) == 1:
            # Obtención de la tripleta contenida
            [ triplet ] = search_criteria
            # Se asume que es una condición y se resuelve ésta
            expression = self.create_binary_expression(triplet)

        # Si la longitud del criterio de búsqueda es un número par...
        elif (len(search_criteria) % 2) == 0:
            # Se lanza error de criterio de búsqueda mal construido
            raise AssertionError(ERROR_LABEL.MALFORMED_SEARCH_CRITERIA)

        # Se asume que la cantidad de elementos es válida
        else:
            # Se tienen que convertir todas las tuplas a expresiones binarias antes de hacer uniones lógicas
            for ( index, op_or_triplet ) in enumerate(search_criteria):
                if isinstance(op_or_triplet, tuple):
                    # Se resuelve la tripleta
                    expression = self.create_binary_expression(op_or_triplet)
                    # Asignación de la expresión en el índice correspondiente
                    search_criteria[index] = expression

            # Mientras el tamaño del criterio de búsqueda sea diferente de 1
            while len(search_criteria) != 1:

                # Inicialización de valor de unión encontrada
                union_found = False

                # Se recorre el criterio de búsqueda para unir expresiones
                for index in range( len(search_criteria) - 2 ):

                    # Obtención de elementos para su evaluación
                    item_a = search_criteria[index]
                    item_b = search_criteria[index + 1]
                    item_c = search_criteria[index + 2]

                    # Elemento A es un operador lógico
                    a_is_op = item_a in ['&', '|']
                    # Elemento B es una expresión
                    b_is_condition = isinstance(item_b, BinaryExpression) or isinstance(item_b, BooleanClauseList)
                    # Elemento C es una expresión
                    c_is_condition = isinstance(item_c, BinaryExpression) or isinstance(item_c, BooleanClauseList)

                    # Si A es un operador lógico y a la vez B y C son expresiones...
                    if a_is_op and b_is_condition and c_is_condition:

                        # Reasignación de variables para conservar semántica
                        op = item_a
                        condition_x = item_b
                        condition_y = item_c

                        # Obtención de la expresión binaria
                        expression = self._logic_expression[op](condition_x, condition_y)

                        # Cálculo del índice más alto para cortar el criterio de búsqueda
                        highest_available_index = min(index + 3, len(search_criteria))

                        # Obtención de rebanadas inicial y final de criterio de búsqueda
                        initial_slice = search_criteria[:index]
                        final_slice = search_criteria[highest_available_index:]
                        search_criteria = [*initial_slice, expression, *final_slice]

                        # Se especifica que hubo unión encontrada
                        union_found = True

                        # Se vuelve a iniciar el ciclo de búsqueda
                        break

                # Si se llega a este punto no se puede continuar con el procesamiento del
                # criterio de búsqueda porque no hay más uniones por procesar y tampoco se
                # colapsó a un solo elemento
                if not union_found:
                    raise AssertionError(ERROR_LABEL.MALFORMED_SEARCH_CRITERIA)

            # Obtención de expresión a usar em query
            [ expression ] = search_criteria

        return expression

    def create_binary_expression(
        self,
        triplet: TripletStructure,
    ) -> BinaryExpression:

        # Obtención de los elementos desde la tripleta
        ( field_name, op, value ) = triplet
        # Inicialización de un objetivo de campo
        field_target = self._frame_ctx.create_field_target(field_name, True)
        # Obtención de la instancia de campo
        [ field_instance ] = self._frame_ctx.get_field_instances_from_target(field_target)

        # Construcción de expresión binaria
        expression = self._comparison_expression[op](field_instance, value)

        return expression
