from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.orm import (
    Session,
    aliased,
)
from ..._constants import MODEL_NAME
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

    def get_user_data_by_username(
        self,
        login: str,
    ) -> tuple[int, str] | None:

        # Obtención de la tabla de usuarios
        base_users = self._strc.get_model(MODEL_NAME.BASE_USERS)
        # Obtención de las instancias de columna
        base_users__id = self._index[base_users]['id']
        base_users__password = self._index[base_users]['password']
        base_users__login = self._index[base_users]['login']
        base_users__active = self._index[base_users]['active']

        # Creación del query
        stmt = (
            select(
                base_users__id,
                base_users__password,
            )
            .where(
                base_users__login == login,
                base_users__active == True,
            )
        )

        # Ejecución de la transacción
        response = self._connection.execute(stmt)
        # Obtención de los datos encontrados
        found_data = response.fetchall()

        # Si no hay datos...
        if not found_data:
            # Se retorna None
            return None

        # Destructuración de los datos
        [ ( user_id, hashed_password ) ] = found_data

        return ( user_id, hashed_password )

    def is_active_user_from_session_uuid(
        self,
        session_uuid: str,
    ) -> bool:

        # Obtención de los modelos
        base_users_session = self._strc.get_model(MODEL_NAME.BASE_USERS_SESSION)
        base_users = aliased( self._strc.get_model(MODEL_NAME.BASE_USERS) )
        # Obtención de las instancias de columnas
        base_users_session__user_id = self._index[base_users_session]['user_id']
        base_users_session__uuid = self._index[base_users_session]['name']
        base_users__id = self._index[base_users]['id']
        base_users__active = self._index[base_users]['active']

        # Creación del query
        stmt = (
            select(
                base_users__active
            )
            .select_from(base_users_session)
            .outerjoin(
                base_users,
                base_users_session__user_id == base_users__id,
            )
            .where(base_users_session__uuid == session_uuid)
        )

        # Ejecución en la base de datos
        response = self._connection.execute(stmt)
        # Destructuración del resultado
        [ ( is_active, ) ] = response.fetchall()

        return is_active

    def create(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> list[int]:

        # Se remueven los campos many2many
        self._remove_many2many_fields(model_name, data)
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

    def _remove_many2many_fields(
        self,
        model_name: str,
        data: list[RecordData],
    ) -> None:

        # Obtención de los nombres de campos many2many del modelo
        many2many_fields = self._strc.get_ttype_fields(model_name, 'many2many')

        # Iteración por cada registro a crear
        for record in data:
            # Búsqueda por cada campo many2many que pueda existir en el diccionario
            for many2many_field in many2many_fields:
                # Si se encuentra un campo many2many...
                if many2many_field in record.keys():
                    # Se remueve éste de los datos
                    del record[many2many_field]

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
