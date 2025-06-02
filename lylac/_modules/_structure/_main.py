from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._core import (
    _BaseLylac,
    _BaseStructure,
)

class Structure(_BaseStructure):

    def __init__(
        self,
        instance: _BaseLylac
    ) -> None:

        # Obtención del set de mapeadores de la tabla
        mappers = list(instance._base.registry.mappers)
        # Creación del diccionario de tablas
        self.models = { getattr(mapper.class_, '__tablename__').replace('_', '.'): mapper.class_ for mapper in mappers }

    def register_table(
        self,
        table_model: type[DeclarativeBase]
    ) -> None:

        # Obtención del nombre de la tabla
        table_name = table_model.__tablename__.replace('_', '.')
        # Se registra el modelo de la tabla en el diccionario de modelos
        self.models[table_name] = table_model

    def unregister_table(
        self,
        table_name: str
    ) -> None:

        # Obtención del modelo de la tabla
        table_model = self.models[table_name]
        # Se borra el modelo
        del table_model
        # Se borra la llave y valor del diccionario de modelos
        del self.models[table_name]
