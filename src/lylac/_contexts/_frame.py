from typing import Any
from typing import Generator
from typing import Generic
from typing import Optional
from sqlalchemy import Subquery
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy.engine import Connection
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import BinaryExpression
from .._constants import ERROR_LABEL
from .._constants import FIELD_NAME
from .._constants import FIELD_SUFFIX
from .._constants import RELATION_PATH_SEPARATOR
from .._constants import ROOT_PATH
from .._contracts.contexts import Contract_FrameContext
from .._contracts.engines import Contract_ComputationEngine
from .._resources import DatabaseMetadata
from .._resources import FieldProperties
from .._resources import FieldTarget
from .._resources import ModelProperties
from .._resources import ModelsBearer
from .._resources import OuterJoin
from .._typing.aliases import ModelClass
from .._typing.generics import ModelName
from .._typing.structures import FieldReadDeclaration
from .._typing.type_parameters import _M
from ._compute import ComputeContext
from ._where import WhereContext

class FrameContext(Generic[_M], Contract_FrameContext[_M]):

    def __init__(
        self,
        model_name: ModelName[_M],
        conn: Connection,
        database_metadata: DatabaseMetadata[_M],
        computation_engine: Contract_ComputationEngine[_M],
    ) -> None:

        # Inicialización de instancia de portador de modelos
        self._models_bearer = ModelsBearer[_M]()
        self._computation_engine = computation_engine

        # Obtención de instancia de conexión
        self._conn = conn
        # Obtención de instancia de metadatos de la base de datos
        self._database_metadata = database_metadata

        # Obtención del nombre del modelo
        self.model_name = model_name

        # Obtención de la clase del modelo
        self.origin_model = self.get_aliased_model_model(model_name)

        # Inicialización de lista de OUTERJOINs
        self._final_stmt_outerjoins = []

        # Inicialización de diccionario de grafos
        self._graph: dict[str, ModelProperties[_M]] = {}
        # Inicialización de grafo raíz
        self._graph[ROOT_PATH] = ModelProperties[_M](self.model_name, self.origin_model)

    @property
    def outerjoins(
        self,
    ) -> tuple[OuterJoin]:

        # Obtención de las instancias de OUTERJOINs como tupla
        outerjoins = tuple(self._final_stmt_outerjoins)

        return outerjoins

    def create_filter_context(
        self,
    ) -> WhereContext[_M]:

        # Inicialización de contexto de filtro
        where_ctx = WhereContext[_M](self)

        return where_ctx

    def portal(
        self,
        model_name: ModelName[_M],
    ) -> Contract_FrameContext[_M]:

        # Creación de un contexto de portal de frame
        frame_ctx = FrameContext[_M](model_name, self._conn, self._database_metadata, self._computation_engine)

        return frame_ctx

    def create_field_target(
        self,
        field_read_declaration: FieldReadDeclaration,
        only_id_for_m2o: bool = False,
    ) -> FieldTarget[_M]:

        # Si la declaración de campo es una estructura de campo computado en ejecución...
        if isinstance(field_read_declaration, tuple) and len(field_read_declaration) == 3:
            # Obtención del nombre, tipo de dato y función de cómputo
            ( field_label, field_ttype, computation_callback ) = field_read_declaration

            # Inicialización de objeto de objetivo de campo
            field_target = FieldTarget(
                complete_name= None,
                label= field_label,
                ttype= field_ttype,
                computation_callback= computation_callback
            )

            return field_target

        # Si el campo es una cadena de texto...
        if isinstance(field_read_declaration, str):
            # Obtención del nombre del campo
            complete_name = field_read_declaration
            # Obtención del alias de campo
            field_label = field_read_declaration

        # Si el campo es una tupla de nombre real y alias...
        elif isinstance(field_read_declaration, tuple) and len(field_read_declaration) == 2:
            # Obtención del nombre y alias del campo
            ( complete_name, field_label ) = field_read_declaration

        else:
            # Se arroja error de campo malformado
            raise AssertionError(ERROR_LABEL.MALFORMED_FIELD_DECLARATION)

        # Obtención de las propiedades del campo
        field_properties = self._database_metadata.field_properties(self.model_name, complete_name)
        # Obtención del tipo de dato del campo
        field_ttype = field_properties.ttype

        # Si se especificó el parámetro de solo ID para many2one...
        if only_id_for_m2o:
            # Si el campo es many2one:
            if field_ttype == 'many2one':
                # Se declara que se obtenga la ID del campo
                complete_name = f'{complete_name}{RELATION_PATH_SEPARATOR}{FIELD_NAME.ID}'

        # Inicialización de objeto de objetivo de campo
        field_target = FieldTarget(
            complete_name= complete_name,
            label= field_label,
            ttype= field_ttype,
        )

        return field_target

    def get_field_instances_from_target(
        self,
        field_target: FieldTarget,
    ) -> list[InstrumentedAttribute]:

        # Si el objetivo de campo tiene una función de cómputo...
        if field_target.computation_callback is not None:
            # Obtención de la función de cómputo
            computation_callback = field_target.computation_callback
            # Inicialización de contexto de cómputo
            computation_ctx = ComputeContext(self, self._computation_engine)
            # Obtención de la instancia de campo computado
            field_instance = (
                computation_callback(computation_ctx)
                .label(field_target.label)
            )
            # # Construcción de formato esperado
            field_instances = [field_instance,]

        # Si el objetivo de campo no tiene una función de cómputo...
        else:
            # Obtención de lista de instancias de campo
            field_instances = self.get_field_instances(field_target.complete_name, field_target.label)

        return field_instances

    def get_field_instances(
        self,
        field_complete_name: str,
        field_label: Optional[str] = None,
    ) -> list[InstrumentedAttribute]:

        # Si la etiqueta del campo no existe...
        if field_label is None:
            # Se asigna el nombre completo del campo como etiqueta
            field_label = field_complete_name

        # Inicialización de lista de instancias de campos
        field_instances: list[InstrumentedAttribute] = []

        # Si el campo es una referencia...
        if self.is_reference_field(field_complete_name):

            # Obtención de la referencia de ruta de campo
            field_reference = field_complete_name
            # Construcción de grafo para llegar al modelo del campo
            self._create_field_graph(field_reference)

            # Obtención de las propiedades del modelo
            model_properties = self._get_model_properties_from_graph(field_reference)
            # Obtención de la clase del modelo
            model_model = model_properties.model
            # Obtención del nombre del modelo
            model_name = model_properties.name

            # Obtención del nombre del campo desde la ruta
            ( field_reference, field_name ) = self.get_path_and_name(field_reference)

            # Se crea un contexto relativo de frame
            ctx = self.spawn_relative(field_reference)

        # Si el campo no es una referencia...
        else:
            # Obtención del nombre del campo desde el nombre completo
            field_name = field_complete_name

            # Obtención de la clase del modelo desde el contexto de frame
            model_model = self.origin_model
            # Obtención del nombre del modelo desde el contexto de frame
            model_name = self.model_name

            # Se usa esta instancia como contexto de frame
            ctx = self

        # Obtención de las propiedades del campo
        field_properties = self._database_metadata.field_properties(model_name, field_name)

        # Evaluación de si el campo debe computarse
        must_compute = (
            field_properties.is_computed
            or field_properties.name == FIELD_NAME.DISPLAY_NAME
        )

        # Si el campo debe computarse...
        if must_compute:
            # Inicialización de contexto de cómputo
            compute_ctx = ComputeContext(ctx, self._computation_engine)

            # Obtención de la instancia de campo
            field_instance = (
                compute_ctx[field_name]
                .label(field_label)
            )

            # Si la instancia se pudo obtener...
            if field_instance is not None:
                # Se añade ésta
                field_instances.append(field_instance)

        # Si el tipo de dato del campo es many2one...
        elif field_properties.ttype == 'many2one':

            # Asignación de referencia de campo
            field_reference = field_complete_name

            # Construcción y obtención de las propiedades del modelo
            model_properties = self.build_graph_from_field_path(field_reference)
            # Obtención del nombre del modelo
            model_name = model_properties.name
            # Obtención de la clase del modelo
            model_model = model_properties.model

            # Creación de contexto relativo de frame desde la referencia de campo
            ctx = self.spawn_relative(field_reference)

            # Inicialización de contexto de cómputo
            compute_ctx = ComputeContext(ctx, self._computation_engine)

            # Construcción de etiquetas de instancias de campos
            id_field_label = f'{field_label}{FIELD_SUFFIX.ID}'
            name_field_label = f'{field_label}{FIELD_SUFFIX.NAME}'

            # Obtención de la instancia de ID desde el campo Many2One
            id_field_instance = (
                compute_ctx[FIELD_NAME.ID]
                .label(id_field_label)
            )
            # Obtención de la instancia de nombre a mostrar desde el campo Many2One
            name_field_instance = (
                compute_ctx[FIELD_NAME.DISPLAY_NAME]
                .label(name_field_label)
            )

            # Se añaden las instancias de campos a la lista a retornar
            field_instances.append(id_field_instance)
            field_instances.append(name_field_instance)

        # Si el tipo de dato del campo es one2many...
        elif field_properties.ttype == 'one2many':

            # Obtención del nombre del campo one2many
            field_name = field_properties.name
            # Obtención del nombre del campo Many2One del modelo relacionado
            related_field_name = field_properties.related_field
            # Obtención de la clase del modelo hijo desde el contexto de frame
            child_model = ctx.origin_model

            # Obtención de instancia de campo de ID del modelo hijo
            child_model_id_field_instance = self.get_physical_field_instance(child_model, FIELD_NAME.ID)
            # Obtención del nombre del modelo relacionado
            related_model_name = field_properties.related_model_name
            # Obtención de la clase del modelo relacionado
            related_model_model = self.get_aliased_model_model(related_model_name)

            # Obtención de la instancia de campo de ID del modelo relacionado
            related_model_id_field_instance = self.get_physical_field_instance(related_model_model, FIELD_NAME.ID)
            # Obtención de la instancia del campo Many2One del modelo relacionado
            related_model_m2o_field_instance = self.get_physical_field_instance(related_model_model, related_field_name)

            # Obtención de instancia de lista de IDs desde el modelo relacionado
            id_array_field_instance = (
                # Se hace una agregación por arreglo
                func.array_agg(
                    # Uso de ordenamiento para garantizar el orden ascendente de IDs
                    aggregate_order_by(
                        related_model_id_field_instance,
                        related_model_id_field_instance.asc(),
                    )
                )
                .label(field_complete_name)
            )

            # Construcción de subquery
            stmt = (
                # Selección de campos
                select(
                    # ID de modelo de origen
                    child_model_id_field_instance,
                    # Lista de IDs del modelo relacionado
                    id_array_field_instance
                )
                # Declaración explícita de origen de selección
                .select_from(child_model)
                # Se añade OUTERJOIN
                .outerjoin(
                    # Objetivo hacia el modelo relacionado
                    related_model_model,
                    # Donde la ID de modelo hijo sea igual a la ID del modelo relacionado
                    child_model_id_field_instance == related_model_m2o_field_instance
                )
                # Se agrupan los resultados por ID de modelo hijo
                .group_by(child_model_id_field_instance)
                # Ordenamiento por ID de modelo hijo
                .order_by(child_model_id_field_instance)
                # Conversión a subquery
                .subquery()
            )

            # Obtención de instancia de campo One2Many desde subquery
            o2m_subquery_field_instance = (
                self.get_physical_field_instance(stmt, field_complete_name)
                .label(field_label)
            )
            # Obtención de instancia de campo de ID de modelo de origen desde subquery
            subquery_id_field_instance = self.get_physical_field_instance(stmt, FIELD_NAME.ID)

            # Se añade el OUTERJOIN
            self.add_outerjoin(
                # Objetivo hacia subquery construida
                stmt,
                # Donde ID de modelo de origen sea igual a ID de query
                child_model_id_field_instance == subquery_id_field_instance
            )

            # Se añade la instancia de campo One2Many a la lista a retornar
            field_instances.append(o2m_subquery_field_instance)

        # Si el tipo de dato del campo es many2many...
        elif field_properties.ttype == 'many2many':

            # Obtención del nombre del campo
            field_name = field_properties.name
            # Obtención del nombre del modelo
            model_name = ctx.model_name
            # Obtención del modelo de relación
            m2m_model_model = self._models_bearer.get_m2m_model(model_name, field_name)

            # Obtención del campo de ID del modelo de origen
            id_field_instance = ctx.get_physical_field_instance_from_current(FIELD_NAME.ID)

            # Obtención de la instancia de campo de ID de registro padre
            reference_origin_field_instance = self.get_physical_field_instance(m2m_model_model, FIELD_NAME.X)
            # Obtención de la instancia de campo de ID de registro referenciado
            y_field_instance = self.get_physical_field_instance(m2m_model_model, FIELD_NAME.Y)

            # Agregación de campo de registro referenciado
            related_field_instance = (
                func.array_agg(
                    aggregate_order_by(
                        y_field_instance,
                        y_field_instance.asc()
                    )
                )
                .label(field_name)
            )

            # Construcción de subquery
            stmt = (
                # Selección de campos
                select(
                    # ID de registro que referencía
                    reference_origin_field_instance,
                    # ID de registro referenciado
                    related_field_instance,
                )
                # Declaración explícita de origen de selección
                .select_from(m2m_model_model)
                # Se agrupan los resultados por ID de registro que referencía
                .group_by(reference_origin_field_instance)
                # Conversión a subquery
                .subquery()
            )

            # Obtención de instancia de campo X desde el subquery
            subquery_id_field_instance = self.get_physical_field_instance(stmt, FIELD_NAME.X)
            # Obtención de instancia de campo Y desde el subquery
            m2m_subquery_field_instance = self.get_physical_field_instance(stmt, field_name).label(field_label)

            # Se agrega el OUTERJOIN
            self.add_outerjoin(
                stmt,
                id_field_instance == subquery_id_field_instance,
            )

            # Se añade la instancia de campo Many2Many a la lista a retornar
            field_instances.append(m2m_subquery_field_instance)

        # Si el campo es físico...
        else:
            # Obtención de instancia de campo físico desde la tabla
            field_instance = (
                self.get_physical_field_instance(model_model, field_properties.name)
                .label(field_label)
            )

            # Se añade la instancia de campo a la lista a retornar
            field_instances.append(field_instance)

        return field_instances

    def get_field_properties(
        self,
        model_name: ModelName[_M],
        field_name: str,
    ) -> FieldProperties[_M]:

        # Obtención de las propiedades de campo
        field_properties = self._database_metadata.field_properties(model_name, field_name)

        return field_properties

    def spawn_relative(
        self,
        path: str,
    ) -> Contract_FrameContext[_M]:

        # Creación de instancia de frame relativo
        relative_frame_ctx = RelativeFrameContext(self, path)

        return relative_frame_ctx

    def get_physical_field_instance_from_current(
        self,
        field_name: str,
    ) -> InstrumentedAttribute:

        # Obtención de instancia de campo desde campo físico en la tabla origen del contexto
        field_instance = self.get_physical_field_instance(self.origin_model, field_name)

        return field_instance

    def is_reference_field(
        self,
        field_reference_or_name: str,
    ) -> bool:

        # Se comprueba si existe un separador de relación en el nombre completo
        result = RELATION_PATH_SEPARATOR in field_reference_or_name

        return result

    def get_path_and_name(
        self,
        field_reference: str,
    ) -> tuple[str, str]:

        # Obtención de la ruta de campos con el nombre
        fields_path_with_field_name = (
            field_reference
            .split(RELATION_PATH_SEPARATOR)
        )

        # Obtención de la referencia de campo
        field_reference = RELATION_PATH_SEPARATOR.join(fields_path_with_field_name[:-1])
        # Obtención del nombrel de campo
        field_name = fields_path_with_field_name[-1]

        return ( field_reference, field_name )

    def build_graph_from_field_path(
        self,
        field_reference: str,
    ) -> ModelProperties[_M]:

        # Obtención de lista de ruta de campos
        fields_path = field_reference.split(RELATION_PATH_SEPARATOR)

        # Asignación del nombre de modelo padre desde el nombre de modelo del contexto del frame
        parent_model_name = self.model_name
        # Asignación de la clase de modelo padre desde la clase del modelo de origen del contexto
        parent_model_model = self.origin_model

        # Creación de cada ruta existente para los modelos encadenados
        for ( layer_i, m2o_field_name ) in enumerate(fields_path):
            # Construcción de ruta parcial de campos en base a la iteración
            fields_partial_path = fields_path[:layer_i + 1]
            # Creación de referencia partial para obtención de modelo y creación de outerjoin
            fields_partial_reference = RELATION_PATH_SEPARATOR.join(fields_partial_path)

            # Si la referencia parcial de campos no está en el grafo...
            if not fields_partial_reference in self._graph:
                # Obtención del campo físico Many2One desde el modelo padre
                m2o_field_instance = self.get_physical_field_instance(parent_model_model, m2o_field_name)
                # Obtención de las propiedades del campo
                field_properties = self._database_metadata.field_properties(parent_model_name, m2o_field_name)

                # Obtención del nombre del modelo relacionado
                related_model_name = field_properties.related_model_name
                # Obtención de un alias de la clase del modelo referenciado
                related_model_model = self.get_aliased_model_model(related_model_name)
                # Obtención de la instancia de ID del campo del modelo relacionado
                related_model_id_field_instance = self.get_physical_field_instance(related_model_model, FIELD_NAME.ID)

                # Se añade el OUTERJOIN
                self.add_outerjoin(
                    # Objetivo hacia modelo relacionado
                    related_model_model,
                    # Donde el campo Many2One del modelo padre sea igual al campo de ID del modelo relacionado
                    m2o_field_instance == related_model_id_field_instance
                )

                # Inicialización de instancia de propiedades del modelo
                model_properties = ModelProperties[_M](
                    related_model_name,
                    related_model_model,
                )

                # Se registran las propiedades del modelo en el grafo
                self._graph[fields_partial_reference] = model_properties

                # Reasignación de nombre y clase de modelo padre desde el modelo relacionado para siguiente iteración
                parent_model_name = related_model_name
                parent_model_model = related_model_model

            else:
                # Obtención de propiedades del modelo de la referencia parcial desde los grafos
                model_properties = self._graph[fields_partial_reference]
                # Obtención de nombre del modelo
                parent_model_name = model_properties.name
                # Obtención de clase del modelo
                parent_model_model = model_properties.model

        return model_properties

    def get_aliased_model_model(
        self,
        model_name: ModelName[_M],
    ) -> ModelClass:

        # Obtención de la clase del modelo
        model_model = self._models_bearer.get_model(model_name)
        # Obtención de alias de la clase del modelo
        aliased_model_model = aliased(model_model)

        return aliased_model_model

    def get_physical_field_instance(
        self,
        source: ModelClass | Subquery,
        field_name: str,
    ) -> InstrumentedAttribute:

        # Si el origen es un subquery...
        if isinstance(source, Subquery):
            # Obtención de la instancia de campo desde obtención de atributo
            field_instance: InstrumentedAttribute = getattr(source.c, field_name)

        # Si el origen es una clase...
        else:
            # Obtención de la instancia de campo desde obtención de atributo
            field_instance: InstrumentedAttribute = getattr(source, field_name)

        return field_instance

    def get_database_model_names(
        self,
    ) -> Generator[ModelName[_M], Any, None]:

        # Se retornan los nombres de modelo
        for model_name_i in self._database_metadata.model_names:
            yield model_name_i

    def add_outerjoin(
        self,
        model: ModelClass,
        on: BinaryExpression
    ) -> None:

        # Inicialización de la instancia de OUTERJOIN
        outerjoin = OuterJoin(model, on)
        # Se añade éste a la lista del contexto
        self._final_stmt_outerjoins.append(outerjoin)

    def _create_field_graph(
        self,
        field_reference: str,
    ) -> None:

        # Obtención de ruta y nombre de campo
        ( fields_path, _ ) = self.get_path_and_name(field_reference)

        # Si el modelo del campo aún no existe en los grafos...
        if fields_path not in self._graph:
            # Construcción de la ruta
            self.build_graph_from_field_path(fields_path)

    def _get_model_properties_from_graph(
        self,
        field_reference: str,
    ) -> ModelProperties[_M]:

        # Obtención de ruta de grafo y nombre del campo
        ( fields_path, _ ) = self.get_path_and_name(field_reference)
        # Obtención del alias del modelo desde el grafo
        model_properties = self._graph[fields_path]

        return model_properties

class RelativeFrameContext(Generic[_M], Contract_FrameContext[_M]):

    def __init__(
        self,
        main_ctx: FrameContext[_M],
        relative_origin: str,
    ) -> None:

        # Obtención de las propiedades del modelo de inicio relativo
        model_properties = main_ctx.build_graph_from_field_path(relative_origin)

        # Obtención de instancia de metadatos de la base de datos
        self._database_metadata = main_ctx._database_metadata

        # Obtención del nombre del modelo
        self.model_name = model_properties.name
        # Obtención de la clase del modelo
        self.origin_model = model_properties.model

        # Asignación del contexto principal
        self._main_ctx = main_ctx
        # Asignación de la ruta de inicio relativa
        self._relative_main = relative_origin

        self._final_stmt_outerjoins = self._main_ctx._final_stmt_outerjoins

    @property
    def outerjoins(
        self,
    ) -> tuple[OuterJoin]:

        # Obtención de las instancias de OUTERJOINs en tupla desde el contexto principal
        outerjoins = self._main_ctx.outerjoins

        return outerjoins

    def get_field_instances_from_target(
        self,
        field_target: FieldTarget,
    ) -> list[InstrumentedAttribute]:

        # Construcción del nombre con la ruta de inicio relativa
        complete_name = f'{self._relative_main}{RELATION_PATH_SEPARATOR}{field_target.complete_name}'
        # Obtención de las instancias de campo
        field_instances = self._main_ctx.get_field_instances(complete_name, field_target.label)

        return field_instances

    def create_filter_context(
        self,
    ) -> WhereContext[_M]:

        # Inicialización de contexto de filtro
        where_ctx = WhereContext[_M](self)

        return where_ctx

    def portal(
        self,
        model_name: ModelName[_M],
    ) -> Contract_FrameContext[_M]:

        # Creación de un contexto de portal de frame
        frame_ctx = self._main_ctx.portal(model_name)

        return frame_ctx

    def get_field_instances(
        self,
        field_complete_name: str,
        field_label: Optional[str] = None,
    ) -> list[InstrumentedAttribute]:

        # Construcción del nombre con la ruta de inicio relativa
        complete_name = f'{self._relative_main}{RELATION_PATH_SEPARATOR}{field_complete_name}'
        # Obtención de las instancias de campo
        field_instances = self._main_ctx.get_field_instances(complete_name, field_label)

        return field_instances

    def get_physical_field_instance_from_current(
        self,
        field_name: str,
    ) -> InstrumentedAttribute:

        # Obtención de la instancia de campo usando el modelo de origen de este contexto
        field_instance = self._main_ctx.get_physical_field_instance(self.origin_model, field_name)

        return field_instance

    def get_database_model_names(
        self,
    ) -> Generator[ModelName[_M], Any, None]:

        # Se retornan los nombres de modelo
        for model_name_i in self._database_metadata.model_names:
            yield model_name_i

    def get_field_properties(
        self,
        model_name: ModelName[_M],
        field_name: str,
    ) -> FieldProperties[_M]:

        # Obtención de las propiedades de campo
        field_properties = self._database_metadata.field_properties(model_name, field_name)

        return field_properties

    def get_physical_field_instance(
        self,
        source: ModelClass | Subquery,
        field_name: str,
    ) -> InstrumentedAttribute:

        # Obtención de la instancia de campo físico desde la tabla
        field_instance = self._main_ctx.get_physical_field_instance(source, field_name)

        return field_instance

    def is_reference_field(
        self,
        field_reference_or_name: str,
    ) -> bool:

        # Se comprueba si existe un separador de relación en el nombre completo
        result = RELATION_PATH_SEPARATOR in field_reference_or_name

        return result

    def get_path_and_name(
        self,
        field_reference: str,
    ) -> tuple[str, str]:

        # Obtención de tupla de datos
        path_and_name = self._main_ctx.get_path_and_name(field_reference)

        return path_and_name

    def spawn_relative(
        self,
        path: str,
    ) -> Contract_FrameContext[_M]:
        
        # Construcción de ruta completa
        complete_path = f'{self._relative_main}{RELATION_PATH_SEPARATOR}{path}'
        # Inicialización de contexto relativo de frame
        frame_ctx = RelativeFrameContext[_M](self._main_ctx, complete_path)

        return frame_ctx

    def add_outerjoin(
        self,
        model: ModelClass,
        on: BinaryExpression
    ) -> None:

        # Se añade el OUTERJOIN en el contexto principal
        self._main_ctx.add_outerjoin(model, on)
