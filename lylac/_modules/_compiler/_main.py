from sqlalchemy import delete
from sqlalchemy.orm import Session
from ..._core import _Lylac, BaseCompiler
from ..._module_types import (
    ModelTemplate,
    RecordData,
)

class Compiler(BaseCompiler):

    def __init__(
        self,
        instance: _Lylac
    ):

        # Asignación de la instancia principal
        self._main = instance
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc
        # Asignación de la instancia de índice
        self._index = instance._index
        # Asignación de la instancia de conexión
        self._connection = instance._connection
        # Asignación del motor de conexión
        self._engine = instance._engine

    def create(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> list[int]:

        # Obtención de la instancia de la tabla
        model_model = self._strc.get_model(model_name)
        # Instanciación de objetos para crear en la base de datos
        records: list[ModelTemplate] = [ model_model(**record) for record in data ]

        # Ejecución de la transacción
        with Session(self._engine) as session:
            session.add_all(records)
            session.commit()

            # Actualización de los objetos registrados
            for record in records:
                session.refresh(record)

        # Obtención de las IDs creadas
        inserted_records = [ record.id for record in records ]

        return inserted_records

    def create_many2many(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> None:

        # Obtención del modelo
        model_model = self._strc.get_model(model_name)
        # Inicialización de los datos
        instanced_data = [ model_model(**record) for record in data ]

        # Creación de registros en la base de datos
        with Session(self._engine) as session:
            session.add_all(instanced_data)
            session.commit()

    def delete_many2many(
        self,
        model_name: str,
        field_name: str,
        record_ids: list[int],
    ) -> None:

        # Obtención de modelo de tabla de relación
        model_model = self._strc.get_relation_model(model_name, field_name)
        # Obtención de instancia de campo de ID de modelo propietario
        id_field_instance = self._index[model_model]['x']

        # Creación del query
        stmt = (
            delete(model_model)
            .where( id_field_instance.in_(record_ids) )
        )

        # Ejecución de la transacción en la base de datos
        self._connection.execute(stmt, commit= True)
