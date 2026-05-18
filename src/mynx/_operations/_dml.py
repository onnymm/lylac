from typing import Generic
from typing import Sequence
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from .._constants import FIELD_NAME
from .._contracts.contexts import Contract_ExecutionContext
from .._contracts.contexts import Contract_RelationOperationsContext
from .._typing.generics import ModelName
from .._typing.structures import RecordData
from .._typing.type_parameters import _M

class DML(Generic[_M]):

    def create(
        self,
        rel_op_ctx: Contract_RelationOperationsContext[_M],
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        data: list[RecordData],
    ) -> list[int]:

        # Obtención del modelo de creación de datos
        model_model = execution_ctx.models_bearer.get_model(model_name)
        # Obtención de la instancia de ID de campo del modelo de creación de datos
        id_instance_field = execution_ctx.models_bearer.get_field_instance(model_name, FIELD_NAME.ID)

        # Inicialización de lista de IDs creadas
        created_ids: list[int] = []

        # Iteración por cada diccionario de registro
        for record_data in data:
            # Captación de comandos de operaciones de relación y creación de función de captación de ID
            capture_created_id_fn = rel_op_ctx.capture_relation_commands(record_data)
            # Construcción de query
            stmt_i = (
                # Crear en el modelo...
                insert(model_model)
                # Usando los valores...
                .values(**record_data)
                # Retornando IDs de registros creados
                .returning(id_instance_field)
            )

            # Obtención de la ID creada
            [ ( created_id, ) ] = execution_ctx.conn.execute(stmt_i).fetchall()

            # Ejecución de operaciones de relación
            capture_created_id_fn(created_id)

            # Se añade la ID creada a la list a retornar
            created_ids.append(created_id)

        return created_ids

    def update(
        self,
        rel_op_ctx: Contract_RelationOperationsContext[_M],
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: list[int],
        data: RecordData,
    ) -> list[int]:

        # Obtención del modelo de creación de datos
        model_model = execution_ctx.models_bearer.get_model(model_name)
        # Obtención de la instancia de ID de campo del modelo de creación de datos
        id_instance_field = execution_ctx.models_bearer.get_field_instance(model_name, FIELD_NAME.ID)

        # Captación de comandos de operaciones de relación y creación de función de captación de ID
        capture_created_id_fn = rel_op_ctx.capture_relation_commands(data)

        # Construcción de query
        stmt = (
            update(model_model)
            .where(id_instance_field.in_(record_ids))
            .values(data)
            .returning(id_instance_field)
        )

        # Obtención del resultado de la modificación
        result: Sequence[tuple[int]] = execution_ctx.conn.execute(stmt).fetchall()

        # Obtención de las IDs modificadas
        updated_ids = [record_id for ( record_id, ) in result]

        # Iteración por cada registro modificado
        for updated_id in updated_ids:
            # Captura de ID
            capture_created_id_fn(updated_id)

        return updated_ids

    def delete(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: list[int],
    ) -> list[int]:

        # Obtención del modelo de creación de datos
        model_model = execution_ctx.models_bearer.get_model(model_name)
        # Obtención de la instancia de ID de campo del modelo de creación de datos
        id_instance_field = execution_ctx.models_bearer.get_field_instance(model_name, FIELD_NAME.ID)

        # Construcción de query
        stmt = (
            delete(model_model)
            .where(id_instance_field.in_(record_ids))
            .returning(id_instance_field)
        )

        # Ejecución del query
        result: Sequence[tuple[int]] = execution_ctx.conn.execute(stmt).fetchall()

        # Obtención de las IDs de registros eliminados
        deleted_ids = [deleted_id for ( deleted_id, ) in result]

        return deleted_ids
