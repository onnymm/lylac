from typing import Generic
from typing import Optional
from typing import TYPE_CHECKING
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import InstrumentedAttribute
from .._constants import FIELD_NAME
from .._contexts import FrameContext
from .._contexts import WhereContext
from .._resources import InputProcessing
from .._resources import OutputParser
from .._typing.generics import ItemOrList
from .._typing.generics import ModelName
from .._typing.generics import _Record
from .._typing.structures import CriteriaStructure
from .._typing.structures import FrameReadField
from .._typing.type_parameters import _M
from .._utils import to_list

if TYPE_CHECKING:
    from .._contexts import ExecutionContext

class DQL(Generic[_M]):
    _sorting_direction = {
        True: asc,
        False: desc,
    }

    def __init__(
        self,
    ) -> None:

        self._input_processing = InputProcessing()
        self._output_parser = OutputParser()

    def search(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[int]:

        # Inicialización de contexto de frame
        frame_ctx = self._create_frame_context(execution_ctx, model_name)
        # Inicialización de contexto de filtro
        where_ctx = self._create_filter_context(frame_ctx)

        # Inicialización de objetivos de campo
        id_field_target = frame_ctx.create_field_target(FIELD_NAME.ID)

        # Obtención de instancia(s) de campo
        [ id_field_instance ] = frame_ctx.get_field_instances_from_target(id_field_target)

        # Obtención de modelo de origen desde el contexto de frame
        origin_model = frame_ctx.origin_model

        # Inicialización de query
        stmt = (
            select(id_field_instance)
            .select_from(origin_model)
        )

        # Si se proporcionó un criterio de búsqueda
        if search_criteria:

            # Construcción de las condiciones de búsqueda en SQL
            conditions = where_ctx.build_conditions(search_criteria)
            # Asignación del criterio de búsqueda
            stmt = stmt.where(conditions)

        # Obtención de los outerjoins
        for outerjoin in frame_ctx.outerjoins:
            # Obtención de modelo a relacionar
            target_model = outerjoin.model
            # Obtención de clausula de unión
            on = outerjoin.on

            # Se añade el LEFT JOIN al query
            stmt = stmt.outerjoin(target_model, on)

        # Si un valor de desfase fue provisto...
        if offset:
            # Se añade éste al query
            stmt = stmt.offset(offset)

        # Si un valor de límite fue provisto...
        if limit:
            # Se añade éste al query
            stmt = stmt.limit(limit)

        # Ejecución de query
        records_data: list[tuple[int]] = (
            execution_ctx.conn
            .execute(stmt)
            .fetchall()
        )

        # Obtención de los datos formateados
        record_ids = self._output_parser.ids_from_database(records_data)

        return record_ids

    def read(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: list[int],
        fields: list[FrameReadField] = [],
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None,
    ) -> list[_Record]:

        # Inicialización de contexto de frame
        frame_ctx = self._create_frame_context(execution_ctx, model_name)

        # Normalización de campos
        normalized_fields = self._normalize_fields(execution_ctx, model_name, fields)

        # Inicialización de objetivos de campo
        field_targets_to_read = [frame_ctx.create_field_target(field) for field in normalized_fields]

        # Inicialización de instancias de campos a leer
        field_instances_to_read: list[InstrumentedAttribute] = []

        # Iteración por cada objetivo de campo
        for field_target in field_targets_to_read:
            # Obtención de instancia(s) de campo
            field_instances = frame_ctx.get_field_instances_from_target(field_target)
            # Se añaden a la lista
            field_instances_to_read += field_instances

        # Obtención de la instancia de ID
        id_field_instance: InstrumentedAttribute[int] = field_instances_to_read[0]

        # Inicialización de query
        stmt = (
            select(*field_instances_to_read)
            .select_from(frame_ctx.origin_model)
            .where(id_field_instance.in_(record_ids))
        )

        # Obtención de los outerjoins
        for outerjoin in frame_ctx.outerjoins:
            # Obtención de modelo a relacionar
            target_model = outerjoin.model
            # Obtención de clausula de unión
            on = outerjoin.on

            # Se añade el LEFT JOIN al query
            stmt = stmt.outerjoin(target_model, on)

        # Obtención de campos de ordenamiento
        sorting_field_instances = self._build_sorting_field_instances(frame_ctx, sortby, ascending)

        # Se añaden las direcciones de ordenamiento
        stmt = stmt.order_by(*sorting_field_instances)

        # Ejecución de query
        records_data = (
            execution_ctx.conn.execute(stmt)
            .fetchall()
        )

        # Formateo de los datos de salida
        output_data = self._output_parser.records_from_database(records_data, field_targets_to_read)

        return output_data

    def search_read(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        fields: list[FrameReadField] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None,
    ) -> list[_Record]:

        # Inicialización de contexto de frame
        frame_ctx = self._create_frame_context(execution_ctx, model_name)
        # Inicialización de contexto de filtro
        where_ctx = self._create_filter_context(frame_ctx)

        # Normalización de campos
        normalized_fields = self._normalize_fields(execution_ctx, model_name, fields)

        # Inicialización de objetivos de campo
        field_targets_to_read = [frame_ctx.create_field_target(field) for field in normalized_fields]

        # Inicialización de instancias de campos a leer
        field_instances_to_read: list[InstrumentedAttribute] = []

        # Iteración por cada objetivo de campo
        for field_target in field_targets_to_read:
            # Obtención de instancia(s) de campo
            field_instances = frame_ctx.get_field_instances_from_target(field_target)

            # Se añaden a la lista
            field_instances_to_read += field_instances

        # Inicialización de query
        stmt = (
            select(*field_instances_to_read)
            .select_from(frame_ctx.origin_model)
        )

        # Si se proporcionó un criterio de búsqueda
        if search_criteria:

            # Construcción de las condiciones de búsqueda en SQL
            conditions = where_ctx.build_conditions(search_criteria)
            # Asignación del criterio de búsqueda
            stmt = stmt.where(conditions)

        # Obtención de los outerjoins
        for outerjoin in frame_ctx.outerjoins:
            # Obtención de modelo a relacionar
            target_model = outerjoin.model
            # Obtención de clausula de unión
            on = outerjoin.on

            # Se añade el LEFT JOIN al query
            stmt = stmt.outerjoin(target_model, on)

        # Si un valor de desfase fue provisto...
        if offset:
            # Se añade éste al query
            stmt = stmt.offset(offset)

        # Si un valor de límite fue provisto...
        if limit:
            # Se añade éste al query
            stmt = stmt.limit(limit)

        # Obtención de campos de ordenamiento
        sorting_field_instances = self._build_sorting_field_instances(frame_ctx, sortby, ascending)

        # Se añaden las direcciones de ordenamiento
        stmt = stmt.order_by(*sorting_field_instances)

        # Ejecución de query
        records_data = (
            execution_ctx.conn
            .execute(stmt)
            .fetchall()
        )

        # Formateo de los datos de salida
        output_data = self._output_parser.records_from_database(records_data, field_targets_to_read)

        return output_data

    def search_count(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
    ) -> int:

        # Inicialización de contexto de frame
        frame_ctx = self._create_frame_context(execution_ctx, model_name)
        # Inicialización de contexto de filtro
        where_ctx = self._create_filter_context(frame_ctx)

        # Obtención de la instancia de ID
        id_field_instance = frame_ctx.get_physical_field_instance_from_current(FIELD_NAME.ID)

        # Construcción del query de conteo
        stmt = (
            select(
                func.count(id_field_instance)
            )
            .select_from(frame_ctx.origin_model)
        )

        # Si se proporcionó un criterio de búsqueda
        if search_criteria:

            # Construcción de las condiciones de búsqueda en SQL
            conditions = where_ctx.build_conditions(search_criteria)
            # Asignación del criterio de búsqueda
            stmt = stmt.where(conditions)

        # Obtención de los outerjoins
        for outerjoin in frame_ctx.outerjoins:
            # Obtención de modelo a relacionar
            target_model = outerjoin.model
            # Obtención de clausula de unión
            on = outerjoin.on

            # Se añade el LEFT JOIN al query
            stmt = stmt.outerjoin(target_model, on)

        # Ejecución de query
        count = (
            execution_ctx.conn
            .execute(stmt)
            .scalar()
        )

        return count

    def _build_sorting_field_instances(
        self,
        frame_ctx: FrameContext[_M],
        sortby: Optional[ItemOrList[str]],
        ascending: Optional[ItemOrList[bool]],
    ) -> list[InstrumentedAttribute]:

        # Inicialización de lista de ordenamientos
        sorting_fields: list[InstrumentedAttribute] = []

        # Si un valor de ordenamiento fue provisto...
        if sortby is not None:
            # Se asegura un valor de lista
            sortby = to_list(sortby)
            # Si un valor de dirección de ordenamiento fue provisto...
            if ascending is not None:
                # Se asegura un valor de lista
                ascending = to_list(ascending)
            else:
                # Se asegura una lista con la misma longitud de ordenamiento
                ascending = [True for _ in range( len(sortby) )]


            # Iteración por cada campo y dirección de ordenamiento
            for ( sorting_field, sorting_direction ) in zip(sortby, ascending):
                # Obtención de función de dirección de ordenamiento
                direction_fn = self._sorting_direction[sorting_direction]
                # Obtención de la instancia de campo
                [ sorting_field_instance ] = frame_ctx.get_field_instances(sorting_field)
                # Se añade la instancia de campo de ordenamiento
                sorting_fields.append(direction_fn(sorting_field_instance))

        # Si un valor de ordenamiento no fue provisto...
        else:
            # Obtención de instancia de ID
            [ sorting_field_instance ] = frame_ctx.get_field_instances(FIELD_NAME.ID)
            # Se añade la instancia a la lista a retornar
            sorting_fields.append(sorting_field_instance)

        return sorting_fields

    def _create_filter_context(
        self,
        frame_ctx: FrameContext[_M],
    ) -> WhereContext[_M]:

        # Inicialización de contexto de filtro
        where_ctx = WhereContext[_M](frame_ctx)

        return where_ctx

    def _normalize_fields(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        fields: list[FrameReadField] = [],
    ) -> list[FrameReadField]:

        # Si no fue provista una lista de campos...
        if not fields:
            # Obtención de lista de campos desde los metadatos del modelo
            fields = execution_ctx.database_metadata.get_field_names_from_model(model_name)
            # Normalización de campos
            normalized_fields = self._input_processing.reorder_fields(fields)
        # Si fue provista una lista de campos
        else:
            # Se procesan los campos para colocar el campo de ID al principio
            normalized_fields = self._input_processing.id_first_on_fields(fields)

        return normalized_fields

    def _create_frame_context(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
    ) -> FrameContext[_M]:

        execution_ctx.models_bearer

        # Inicialización de contexto de frame
        frame_ctx = FrameContext[_M](
            model_name,
            execution_ctx.conn,
            execution_ctx.database_metadata,
            execution_ctx.compute,
            execution_ctx.models_bearer,
        )

        return frame_ctx
