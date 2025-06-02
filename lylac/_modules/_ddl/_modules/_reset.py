from sqlalchemy.orm import Session
from ...._core import _BaseLylac
from ...._data import initial_models
from ._base import _BaseDDLManager

class _Reset():

    def __init__(
        self,
        instance: _BaseDDLManager,
    ) -> None:

        # Asignación de instancia propietaria
        self._ddl = instance

    def _init(self):

        # Inicialización de la base de datos
        self._ddl._main._base.metadata.create_all(self._ddl._main._engine)

        # Registro de los datos iniciales
        with Session(self._ddl._main._engine) as session:
            for ( table_name, data ) in initial_models.items():
                model = self._ddl._main._get_table_model(table_name)
                for record in data:
                    session.add(model(**record))

            session.commit()

    def _drop_all(self):

        # Eliminación de todos los datos
        self._ddl._main._base.metadata.drop_all(self._ddl._main._engine)
