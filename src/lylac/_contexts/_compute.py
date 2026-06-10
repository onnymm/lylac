from datetime import datetime
from typing import Any
from typing import Generic
from typing import Literal
from typing import Iterable
from typing import Optional
from typing import overload
from typing import TYPE_CHECKING
from sqlalchemy import types
from sqlalchemy import and_
from sqlalchemy import asc
from sqlalchemy import case
from sqlalchemy import cast
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.functions import _FunctionGenerator
from sqlalchemy.sql.type_api import TypeEngine
from .._constants import FIELD_NAME
from .._constants import FIELD_SUFFIX
from .._constants import RELATION_PATH_SEPARATOR
from .._typing.callables import AggFunc
from .._typing.callables import ComputeFieldFn
from .._typing.structures import CriteriaStructure
from .._typing.type_parameters import _M
from .._typing.literals import AggFuncName
from .._typing.literals import TTypeName

if TYPE_CHECKING:
    from .._contexts import FrameContext
    from .._engines import ComputeEngine

class ComputeContext(Generic[_M]):
    _zero_value = {
        'integer': 0,
        'duration': '00:00',
        'float': 0.0,
    }
    """
    Valores en cero especiales para algunos tipos de dato.
    """
    _agg_fn: dict[AggFuncName, AggFunc] = {
        'sum': func.sum,
        'max': func.max,
        'min': func.min,
        'mean': getattr(func, 'avg'),
        'count': func.count,
        'array': func.array_agg,
    }
    """
    Diccionario de funciones de agregación.
    """
    _casteable: dict[TTypeName, type[TypeEngine]] = {
        'integer': types.Integer,
        'char': types.String,
        'float': types.Float,
        'boolean': types.Boolean,
        'date': types.Date,
        'datetime': types.DateTime,
        'time': types.Time,
        'duration': types.Interval,
    }
    """
    Diccionario de casteos disponibles.
    """

    @overload
    def __getitem__(
        self,
        field_name: Literal['id'],
    ) -> InstrumentedAttribute[int]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['name'],
    ) -> InstrumentedAttribute[str]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['create_date'],
    ) -> InstrumentedAttribute[datetime]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['update_date'],
    ) -> InstrumentedAttribute[datetime]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['create_uid'],
    ) -> InstrumentedAttribute[int]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['update_uid'],
    ) -> InstrumentedAttribute[int]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['display_name'],
    ) -> InstrumentedAttribute[str]:
        ...

    def __init__(
        self,
        frame_ctx: FrameContext[_M],
        engine: ComputeEngine[_M],
    ) -> None:

        # Asignación de contexto de frame
        self._frame_ctx = frame_ctx
        # Asignación de motor de cómputo de campos
        self._computation = engine
        # Inicialización de centro de funciones de campos computados
        self._hub = engine.hub

        # Asignación de nombre y modelo de modelo
        self.model_name = frame_ctx.model_name
        self.origin_model = frame_ctx.origin_model

    def __getitem__(
        self,
        field_name: str,
    ) -> InstrumentedAttribute:

        # Obtención de la instancia de campo
        field_instance = self._get_field_instance(field_name)

        return field_instance

    def cast(
        self,
        field_name_or_instance: str | InstrumentedAttribute,
        ttype: TTypeName,
    ) -> InstrumentedAttribute:

        # Si la declaración de campo es una cadena de texto...
        if isinstance(field_name_or_instance, str):
            # Obtención de la instancia de campo
            field_instance = self._get_field_instance(field_name_or_instance)
        # Si la declaración de campo es una instancia de campo...
        else:
            # Reasignación de la instancia de campo
            field_instance = field_name_or_instance
        # Obtención de tipo de dato a convertir
        type_to_cast = self._casteable[ttype]
        # Obtención de la instancia de campo parseada
        casted_field_instance = cast(field_instance, type_to_cast)

        return casted_field_instance

    def concat(
        self,
        *args: tuple[Any],
    ) -> InstrumentedAttribute[str]:

        # Construcción de la instancia de campo usando la función de concatenación de SQLAlchemy
        field_instance = func.concat(*args)

        return field_instance

    def case(
        self,
        *args: tuple[BinaryExpression, Any],
        default: Any = None,
    ) -> InstrumentedAttribute:

        # Creación de valor condicional en instancia de campo
        field_instance = case(
            *args,
            else_= default,
        )

        return field_instance

    def agg(
        self,
        o2m_field_name: str,
        field_to_aggregate_name: str | ComputeFieldFn[_M],
        fn_name: AggFuncName,
        search_criteria: CriteriaStructure = [],
        default_zero_value: Optional[str | int | float] = None,
    ) -> InstrumentedAttribute:

        # Obtención de la función de agregación
        agg_fn = self._agg_fn[fn_name]

        # Si el campo a usar es una referencia...
        if self._frame_ctx.is_reference_field(o2m_field_name):
            # Obtención de la ruta de campos y el nombre del campo
            ( field_path, field_name ) = self._frame_ctx.get_path_and_name(o2m_field_name)
            # Creación de contexto relativo de frame
            current_frame_ctx = self._frame_ctx.spawn_relative(field_path)

        # Si el campo a usar no es una referencia...
        else:
            # Se usa el contexto propio de frame como contexto relativo
            current_frame_ctx = self._frame_ctx
            # Se reasigna el nombre completo a nombre de campo
            field_name = o2m_field_name

        # Obtención de las propiedades del campo
        field_properties = current_frame_ctx.get_field_properties(current_frame_ctx.model_name, field_name)

        # Si el tipo de dato del campo es One2Many...
        if field_properties.ttype == 'one2many':

            # Obtención del nombre del modelo relacionado
            related_model_name = field_properties.related_model_name
            # Obtención del nombre del campo relacionado
            related_field_name = field_properties.related_field

            # Creación de portal de contexto de frame
            portal_frame_ctx = current_frame_ctx.portal(related_model_name)

            # Construcción de etiqueta común
            label = f'{o2m_field_name}{RELATION_PATH_SEPARATOR}{id(field_to_aggregate_name)}'

            # Etiqueta para campo many2one relacionado
            m2o_related_field_name_label = f'{label}{FIELD_SUFFIX.REF_ID}'
            # Etiqueta para campo a agregar
            field_to_aggregate_label = f'{label}{FIELD_SUFFIX.AGG}'

            # Obtención de la instancia de campo relacionado
            related_field_instance = (
                portal_frame_ctx.get_physical_field_instance_from_current(related_field_name)
                .label(m2o_related_field_name_label)
            )

            # Si la referencia del campo a agregar es un texto...
            if isinstance(field_to_aggregate_name, str):
                # Obtención de la instancia de campo a agregar
                [ field_to_aggregate_instance ] = portal_frame_ctx.get_field_instances(field_to_aggregate_name)

            # Si la referencia del campo a agregar es una función de cómputo...
            else:
                # Creación de un contexto de cómputo con el portal frame
                portal_compute_ctx = ComputeContext(portal_frame_ctx, self._computation)
                # Obtención de la instancia de campo a agregar
                field_to_aggregate_instance = field_to_aggregate_name(portal_compute_ctx)

            # Declaración de cómputo
            aggregated_field = (
                # agg_fn(field_to_aggregate_instance)
                agg_fn(
                    aggregate_order_by(
                        field_to_aggregate_instance,
                        field_to_aggregate_instance.asc()
                    )
                )
                .label(field_to_aggregate_label)
            )

            # Creación del subquery
            subquery = (
                select(
                    related_field_instance,
                    aggregated_field
                )
                .select_from(portal_frame_ctx.origin_model)
            )

            # Si un criterio de búsqueda fue provisto...
            if search_criteria:
                # Inicialización de contexto de filtro
                where_ctx = portal_frame_ctx.create_filter_context()
                # Obtención de instancia de condiciones
                conditions_instance = where_ctx.build_conditions(search_criteria)
                # Se añade cláusula WHERE al subquery
                subquery = subquery.where(conditions_instance)

            # Iteración por OUTERJOINs
            for outerjoin in portal_frame_ctx.outerjoins:
                # Se añaden los OUTERJOINs al subquery
                subquery = subquery.outerjoin(outerjoin.model, outerjoin.on)

            # Ajustes finales
            subquery = (
                subquery
                # Agrupamiento por campo relacionado
                .group_by(related_field_instance)
                # Conversión a subquery
                .subquery()
            )

            # Obtención de instancia de referencia de ID
            ref_id_field_instance = current_frame_ctx.get_physical_field_instance(subquery, m2o_related_field_name_label)
            # Obtención de instancia de campo agregado
            agg_field_instance = current_frame_ctx.get_physical_field_instance(subquery, field_to_aggregate_label)

            # Si el nombre de la función agregada es conteo o suma...
            if fn_name in ['count', 'sum']:
                # Si el campo a agregar es un nombre...
                if isinstance(field_to_aggregate_name, str):
                    # Obtención de las propiedades del campo agregado
                    agg_field_properties = self._frame_ctx.get_field_properties(portal_frame_ctx.model_name, field_to_aggregate_name)
                    # Obtención del tipo de dato del campo agregado
                    agg_field_ttype = agg_field_properties.ttype
                    # Obtención de valor cero del campo en base a su tipo de dato
                    zero_value = self._zero_value[agg_field_ttype]

                    # Uso de switch case para convertir valores nulos a valor cero
                    computed_aggregation = case(
                        (agg_field_instance == None, zero_value),
                        else_= agg_field_instance,
                    )
                # Si el campo a agregar no es un nombre...
                else:
                    # Uso de switch case para convertir valores nulos a valor cero
                    computed_aggregation = case(
                        (agg_field_instance == None, default_zero_value),
                        else_= agg_field_instance,
                    )

            # Si el nombre de la función agregada no es conteo o suma...
            else:
                # Se usa la instancia agregada como cómputo final
                computed_aggregation = agg_field_instance

            # Obtención de instancia de ID del modelo de origen del contexto
            origin_id_field_instance = current_frame_ctx.get_physical_field_instance_from_current(FIELD_NAME.ID)

            # Se añade el OUTERJOIN del subquery al contexto en uso
            current_frame_ctx.add_outerjoin(
                subquery,
                origin_id_field_instance == ref_id_field_instance
            )

            return computed_aggregation

    def weekday(
        self,
        field: str | InstrumentedAttribute,
    ) -> InstrumentedAttribute:

        # Si la referencia de campo es un nombre...
        if isinstance(field, str):
            # Se obtiene éste
            field_instance = self._get_field_instance(field)
        # Si la referencia de campo es una instancia...
        else:
            # Se usa ésta
            field_instance = field

        # Obtención del día de la semana
        weekday_value = func.lower(
            func.trim(
                func.to_char(
                    field_instance,
                    'Day'
                )
            )
        )

        return weekday_value

    def asc(
        self,
        field_instance: InstrumentedAttribute,
    ) -> InstrumentedAttribute:

        # Generación de la declaración
        ordered_field_instance = asc(field_instance)

        return ordered_field_instance

    def desc(
        self,
        field_instance: InstrumentedAttribute,
    ) -> InstrumentedAttribute:

        # Generación de la declaración
        ordered_field_instance = desc(field_instance)

        return ordered_field_instance

    def and_(
        self,
        *field_instances: Iterable[InstrumentedAttribute],
    ) -> BinaryExpression:

        # Obtención de la expresión binaria
        binary_expression = and_(*field_instances)

        return binary_expression

    def or_(
        self,
        *field_instances: Iterable[InstrumentedAttribute],
    ) -> BinaryExpression:

        # Obtención de la expresión binaria
        binary_expression = or_(*field_instances)

        return binary_expression

    @property
    def func(
        self,
    ) -> _FunctionGenerator:

        return func

    def _get_field_instance(
        self,
        field_name: str,
    ) -> InstrumentedAttribute | None:

        # Obtención de las propiedades del campo
        field_properties = self._frame_ctx.get_field_properties(self.model_name, field_name)

        # Si el campo es computado...
        if field_properties.is_computed:

            # Si el campo tiene disponible una función de cómputo...
            if field_name in self._hub[self._frame_ctx.model_name]:
                # Obtención de la función
                compute_callback = self._hub[self._frame_ctx.model_name][field_name]
                # Obtención de la instancia de campo
                field_instance = compute_callback(self)

            # Si el campo no tiene función disponible pero es nombre a mostrar...
            elif field_name == FIELD_NAME.DISPLAY_NAME:
                # Obtención de instancia de campo predeterminado de nombre a mostrar
                field_instance = self._default_display_name()

            # No se hace nada y se retorna None
            else:
                field_instance = None

        # Si el campo no es computado...
        else:
            # Obtención de la instancia de campo
            [ field_instance ] = self._frame_ctx.get_field_instances(field_name)

        return field_instance

    def _default_display_name(
        self,
    ) -> InstrumentedAttribute:

        # Obtención de la instancia de ID de campo
        id_field_instance = self._get_field_instance(FIELD_NAME.ID)
        # Obtención de la instancia de nombre de campo
        name_field_instance = self._get_field_instance(FIELD_NAME.NAME)

        # Cómputo de valor de registro sin nombre
        no_name_field_instance = func.concat(id_field_instance, ',', self.model_name)

        # Evaluación de si el registro tiene nombre o no para asignarle nombre visible
        default_display_name_field_instance = self.case(
            ( name_field_instance == None, no_name_field_instance),
            default= name_field_instance
        )

        return default_display_name_field_instance
