from typing import Any
from typing import Callable
from typing import Generic
from typing import Literal
from typing import TypedDict
from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.orm import aliased
from .._constants import FIELD_NAME
from .._constants import RELATION_ACTIONS
from .._constants import RELATION_ACTION_NAME
from .._contracts import _Contract_CRUD
from .._contracts.contexts import Contract_RelationOperationsContext
from .._contracts.contexts import Contract_ExecutionContext
from .._core import Metadata
from .._resources import ModelsBearer
from .._typing.callables import CaptureCreatedRecordID
from .._typing.callables import CaptureRecordID
from .._typing.callables import CRUD_Operation
from .._typing.generics import ItemOrList
from .._typing.generics import ModelName
from .._typing.interfaces import Many2ManyRelation
from .._typing.literals import RelationActionName
from .._typing.literals import TTypeName
from .._typing.structures import RecordData
from .._typing.structures import RelationCommands
from .._typing.structures import RecordIDs
from .._typing.type_parameters import _M
from .._utils import to_list

class _FieldMetadata(TypedDict, Generic[_M]):
    name: str
    related_field: str
    ttype: TTypeName
    model: ModelName[_M]
    related_model: ModelName[_M]

class _BaseRelation_CRUD(Generic[_M]):
    _model_name: ModelName[_M]
    _commands_map: dict[RelationActionName, Callable[[Contract_ExecutionContext[_M], Any], CaptureRecordID[_M]]]

    def capture_commands_for_field(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        relation_commands: RelationCommands,
        capture_id_functions: list[CaptureRecordID],
    ) -> None:

        # Iteración por cada nombre de acción de relación
        for action_name in RELATION_ACTIONS:
            # Si existe el comando...
            if action_name in relation_commands:
                # Obtención del comando
                data = relation_commands[action_name]
                # Se crea la función de captura de ID
                capture_id = self._commands_map[action_name](execution_ctx, data)
                # Se añade la función a la lista de funciones de captura de ID
                capture_id_functions.append(capture_id)

    def _build_update(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        update_data: ItemOrList[tuple[RecordIDs, RecordData]],
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        update_data = to_list(update_data)

        def update_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Inicialización de función de operación de relación
            def crud_operation(crud: _Contract_CRUD[_M]) -> None:
                # Iteración por cada tupla de datos
                for ( record_ids, records_data ) in update_data:
                    # Modificación
                    crud.update(
                        execution_ctx,
                        self._model_name,
                        record_ids,
                        records_data
                    )

            return crud_operation

        return update_records

    def _build_delete(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        record_ids = to_list(record_ids)

        def delete_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Inicialización de función de operación de relación
            crud_operation: CRUD_Operation[_M] = lambda crud: crud.delete(
                execution_ctx,
                self._model_name,
                record_ids,
            )

            return crud_operation

        return delete_records

    def _build_create(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        records_data: ItemOrList[RecordData],
    ) -> CaptureRecordID[_M]:
        ...
    def _build_add(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:
        ...
    def _build_unlink(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:
        ...
    def _build_replace(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:
        ...
    def _build_clear(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        _: Literal[True] = True,
    ) -> CaptureRecordID[_M]:
        ...

    def _initialize_build_commands_map(
        self,
    ) -> None:

        self._commands_map = {
            RELATION_ACTION_NAME.CREATE: self._build_create,
            RELATION_ACTION_NAME.ADD: self._build_add,
            RELATION_ACTION_NAME.UPDATE: self._build_update,
            RELATION_ACTION_NAME.UNLINK: self._build_unlink,
            RELATION_ACTION_NAME.CLEAR: self._build_clear,
            RELATION_ACTION_NAME.REPLACE: self._build_replace,
            RELATION_ACTION_NAME.DELETE: self._build_delete,
        }

class _Many2One_CRUD(Generic[_M], _BaseRelation_CRUD[_M]):

    def __init__(
        self,
        related_model_name: ModelName[_M],
        m2o_field_name: str,
    ) -> None:

        # Asignación de valores
        self._model_name = related_model_name
        self._m2o_field_name = m2o_field_name

        # Inicialización de mapa de constructor de comandos de acciones de relación
        self._initialize_build_commands_map()

    def _build_create(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        records_data: ItemOrList[RecordData],
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        records_data = to_list(records_data)

        def create_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Iteración por cada registro
            for record_data in records_data:
                # Se añade la ID en el campo correspondiente
                record_data[self._m2o_field_name] = created_or_updated_id

            # Creación de función de operación CRUD
            crud_operation: CRUD_Operation[_M] = lambda crud: crud.create(
                execution_ctx,
                self._model_name,
                records_data,
            )

            return crud_operation

        return create_records

    def _build_add(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        record_ids = to_list(record_ids)

        def add_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Inicialización de función de operación de relación
            def crud_operation(crud: _Contract_CRUD[_M]):
                # Iteración por cada ID de registro
                for record_id in record_ids:
                    # Modificación del campo
                    crud.update(
                        execution_ctx,
                        self._model_name,
                        record_id,
                        {self._m2o_field_name: created_or_updated_id}
                    )

            return crud_operation

        return add_records

    def _build_unlink(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        record_ids = to_list(record_ids)

        def unlink_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Inicialización de función de operación de relación
            crud_operation: CRUD_Operation[_M] = lambda crud: crud.update(
                execution_ctx,
                self._model_name,
                record_ids,
                {self._m2o_field_name: None},
            )

            return crud_operation

        return unlink_records

    def _build_replace(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        record_ids = to_list(record_ids)

        def replace_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Inicialización de función de operación de relación
            def crud_operation(crud: _Contract_CRUD[_M]) -> None:
                # Búsqueda de IDs a reemplazar
                old_record_ids = crud.search(
                    execution_ctx,
                    self._model_name,
                    [(self._m2o_field_name, '=', created_or_updated_id)]
                )
                # Se establecen los registros existentes a None
                crud.update(
                    execution_ctx,
                    self._model_name,
                    old_record_ids,
                    {self._m2o_field_name: None}
                )
                # Se establecen los nuevos registros
                crud.update(
                    execution_ctx,
                    self._model_name,
                    record_ids,
                    {self._m2o_field_name: created_or_updated_id}
                )

            return crud_operation

        return replace_records

    def _build_clear(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        _: Literal[True] = True,
    ) -> CaptureRecordID[_M]:

        def clear_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Inicialización de función de operación de relación
            def crud_operation(crud: _Contract_CRUD[_M]) -> None:
                # Búsqueda de IDs a limpiar
                records_to_clear = crud.search(
                    execution_ctx,
                    self._model_name,
                    [(self._m2o_field_name, '=', created_or_updated_id)]
                )
                # Se establecen los registros a None
                crud.update(
                    execution_ctx,
                    self._model_name,
                    records_to_clear,
                    {self._m2o_field_name: None}
                )

            return crud_operation

        return clear_records

class _Many2Many_CRUD(Generic[_M], _BaseRelation_CRUD[_M]):

    def __init__(
        self,
        model_name: ModelName[_M],
        relation_model_model: type[Many2ManyRelation],
    ) -> None:

        # Asignación de valores
        self._model_name = model_name
        self._relation_model_model = relation_model_model

        # Inicialización de mapa de constructor de comandos de acciones de relación
        self._initialize_build_commands_map()

    def _build_create(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        records_data: ItemOrList[RecordData],
    ) -> CaptureRecordID[_M]:

        def create_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Creación de función de operación CRUD
            crud_operation: CRUD_Operation[_M] = lambda crud: crud.create(
                execution_ctx,
                self._model_name,
                records_data,
            )
            # Creación de función envuelta para captura de IDs creadas
            def wrapped_create_records(crud: _Contract_CRUD[_M]):
                # Ejecución de la operación y captura de IDs de registros creados
                created_ids = crud_operation(crud)
                # Creación de las relaciones en el modelo de relación
                self._create_relations(created_or_updated_id, created_ids, execution_ctx)

            return wrapped_create_records

        return create_records

    def _build_add(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        record_ids = to_list(record_ids)

        def add_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Creación de función de operación CRUD
            crud_operation: CRUD_Operation[_M] = lambda _: self._create_relations(
                created_or_updated_id,
                record_ids,
                execution_ctx,
            )

            return crud_operation

        return add_records

    def _build_unlink(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        record_ids = to_list(record_ids)

        def unlink_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Creación de función de operación CRUD
            crud_operation: CRUD_Operation[_M] = lambda _: self._delete_relations(
                created_or_updated_id,
                record_ids,
                execution_ctx,
            )

            return crud_operation

        return unlink_records

    def _build_replace(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        record_ids: RecordIDs,
    ) -> CaptureRecordID[_M]:

        # Se asegura el formato en lista
        record_ids = to_list(record_ids)

        def replace_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Inicialización de función de operación de relación
            def crud_operation(_: _Contract_CRUD[_M]) -> None:
                # Eliminación de relaciones existentes
                self._clear_relations(created_or_updated_id, execution_ctx)
                # Creación de relaciones
                self._create_relations(
                created_or_updated_id,
                    record_ids,
                    execution_ctx,
                )

            return crud_operation

        return replace_records

    def _build_clear(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        _: Literal[True] = True,
    ) -> CaptureRecordID[_M]:

        def clear_records(created_or_updated_id: int) -> CRUD_Operation[_M]:
            # Creación de función de operación CRUD
            crud_operation: CRUD_Operation[_M] = lambda _: self._clear_relations(
                created_or_updated_id,
                execution_ctx,
            )

            return crud_operation

        return clear_records

    def _create_relations(
        self,
        x: int,
        y: list[int],
        execution_ctx: Contract_ExecutionContext[_M],
    ) -> None:

        # Creación de diccionario de datos
        data = [
            {
                FIELD_NAME.X: x,
                FIELD_NAME.Y: y_i,
            }
            for y_i in y
        ]

        # Creación del query
        stmt = (
            insert(self._relation_model_model)
            .values(data)
        )

        # Ejecución del query
        execution_ctx.conn.execute(stmt)

    def _delete_relations(
        self,
        x: int,
        y: list[int],
        execution_ctx: Contract_ExecutionContext[_M],
    ) -> None:

        # Creación del query
        stmt = (
            delete(self._relation_model_model)
            .where(
                and_(
                    self._relation_model_model.x == x,
                    self._relation_model_model.y.in_(y)
                )
            )
        )

        # Ejecución del query
        execution_ctx.conn.execute(stmt)

    def _clear_relations(
        self,
        x: int,
        execution_ctx: Contract_ExecutionContext[_M],
    ) -> None:

        # Creación de query
        stmt = (
            delete(self._relation_model_model)
            .where(
                self._relation_model_model.x == x
            )
        )

        # Ejecución del query
        execution_ctx.conn.execute(stmt)

class RelationOperationsContext(Generic[_M], Contract_RelationOperationsContext[_M]):

    def __init__(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        models_bearer: ModelsBearer[_M],
    ) -> None:

        # Asignación de la instancia de contexto de ejecución
        self._execution_ctx = execution_ctx
        # Asignación de la instancia de portador de modelos
        self._models_bearer = models_bearer

        # Inicialización de lista total de operaciones CRUD
        self._total_relation_operations: list[CRUD_Operation[_M]] = []

        # Obtención de modelo de campos de modelos
        field = Metadata.BaseModelField
        # Obtención de modelo propietario
        model = aliased(Metadata.BaseModel)
        # Obtención de modelo relacionado
        related_model = aliased(Metadata.BaseModel)

        # Construcción de query para obtención de tipos de datos de campos
        stmt = (
            select(
                field.name,
                field.related_field,
                field.ttype,
                model.model,
                related_model.model.label('related_model'),
            )
            .where(
                model.model == model_name,
                field.ttype.in_(['one2many', 'many2many'])
            )
            .outerjoin(
                model,
                field.model_id == model.id,
            )
            .outerjoin(
                related_model,
                field.related_model_id == related_model.id
            )
        )

        # Ejecución del query
        result = (
            execution_ctx.conn
            .execute(stmt)
            .fetchall()
        )

        # Obtención de los metadatos de los campos
        fields_metadata: list[_FieldMetadata[_M]] = [row._asdict() for row in result]
        # Obtención de los metadatos de los campos one2many
        o2m_fields_metadata = {
            row['name']: row
            for row in fields_metadata
            if row['ttype'] == 'one2many'
        }
        # Obtención de los metadatos de los campos many2many
        m2m_fields_metadata = {
            row['name']: row
            for row in fields_metadata
            if row['ttype'] == 'many2many'
        }

        # Inicialización de mapa de operaciones CRUD en campos one2many
        self._m2o_crud_per_field: dict[str, _Many2One_CRUD[_M]] = {}
        # Inicialización de mapa de operaciones CRUD en campos many2many
        self._m2m_crud_per_field: dict[str, _Many2Many_CRUD[_M]] = {}

        # Iteración por los campos one2many de los metadatos del modelo
        for ( o2m_field_name, o2m_properties ) in o2m_fields_metadata.items():
            # Obtención del nombre del modelo relacionado
            related_model_name = o2m_properties['related_model']
            # Obtención de nombre del campo many2one
            m2o_field_name: str = o2m_properties['related_field']

            # Creación de una instancia de captador de IDs para el campo
            m2o_crud = _Many2One_CRUD[_M](related_model_name, m2o_field_name)
            # Mapeo de la instancia con respecto al nombre del campo one2many
            self._m2o_crud_per_field[o2m_field_name] = m2o_crud

        # Iteración por los campos many2many de los metadatos del modelo
        for ( m2m_field_name, m2m_properties ) in m2m_fields_metadata.items():
            # Obtención del nombre del modelo propiertario
            owner_model_name = m2m_properties['model']
            # Obtención del nombre del modelo relacionado
            related_model_name = m2m_properties['related_model']

            # Obtención del nombre del modelo de relación
            relation_model_model = self._models_bearer.get_m2m_model(owner_model_name, m2m_field_name)

            # Creación de una instancia de captador de IDs para el campo
            m2m_crud = _Many2Many_CRUD[_M](related_model_name, relation_model_model)
            # Mapeo de la instancia con respecto al nombre del campo many2many
            self._m2m_crud_per_field[m2m_field_name] = m2m_crud

    def run_relation_operations(
        self,
        crud: _Contract_CRUD[_M],
    ) -> None:

        # Iteración por cada función a ejecutar
        for relation_operation in self._total_relation_operations:
            # Ejecución de función
            relation_operation(crud)

    def capture_relation_commands(
        self,
        record_data: RecordData,
    ) -> CaptureCreatedRecordID:

        # Inicialización de lista de funciones de captura de ID creada
        capture_id_functions: list[CaptureRecordID] = []
        # Creación de copia de datos para iterar y no romper el ciclo cuando se eliminen llaves
        record_data_for_iteration = record_data.copy()

        # Iteración por cada campo y valor de datos de diccionario de registro a crear
        for field_name in record_data_for_iteration.keys():

            # Si el nombre del campo se encuentra en el diccionario de operaciones de relación para campos one2many...
            if field_name in self._m2o_crud_per_field:
                # Obtención de los comandos de operaciones de relación
                relation_commands: RelationCommands = record_data.pop(field_name)
                # Obtención de la instancia de operaciones CRUD para el campo
                m2o_crud = self._m2o_crud_per_field[field_name]
                # Captura de comandos
                m2o_crud.capture_commands_for_field(self._execution_ctx, relation_commands, capture_id_functions)

            # Si el nombre del campo se encuentra en el diccionario de operaciones de relación para campos many2many...
            if field_name in self._m2m_crud_per_field:

                # Obtención de los comandos de operaciones de relación
                relation_commands: RelationCommands = record_data.pop(field_name)
                # Obtención de la instancia de operaciones CRUD para el campo
                m2m_crud = self._m2m_crud_per_field[field_name]
                # Captura de comandos
                m2m_crud.capture_commands_for_field(self._execution_ctx, relation_commands, capture_id_functions)

        # Inicialización de función para capturar ID de registro creado
        def capture_created_id(created_id: int) -> None:

            # Captura de ID por función generada
            for capture_id_fn in capture_id_functions:
                # Generación de operación CRUD
                crud_operation = capture_id_fn(created_id)
                # Se añade ésta a la lista total
                self._total_relation_operations.append(crud_operation)

        return capture_created_id
