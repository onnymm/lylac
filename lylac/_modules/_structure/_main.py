from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._core import (
    _Lylac,
    _BaseStructure,
)
from ..._module_types import TType
from ._submodules import (
    _Automations,
    _RawORM,
)

class Structure(_BaseStructure):

    def __init__(
        self,
        instance: _Lylac
    ) -> None:

        # Asignación de instancia principal
        self._main = instance

        # Inicialización del módulo de ORM crudo
        self._m_raworm = _RawORM(self)
        # Inicialización del módulo de automatizaciones
        self._m_automations = _Automations(self)

        # Inicialización de la estructura de tablas y atributos de campos
        self._initialize_models_atts()

    def get_model(
        self,
        model_name: str,
    ) -> type[DeclarativeBase]:

        return self.models[model_name]['model']

    def _initialize_models_atts(
        self,
    ) -> None:

        # Obtención del set de mapeadores de la tabla
        mappers = list(self._main._base.registry.mappers)
        # Creación del diccionario de tablas
        self.models = { getattr(mapper.class_, '__tablename__').replace('_', '.'): self._initialize_model_properties(mapper.class_) for mapper in mappers }

    def register_field(
        self,
        model_name: str,
        field_name: str,
        ttype: TType,
        relation: str | None,
    ) -> None:

        # Asignación de valores
        self.models[model_name]['fields'][field_name] = {
            'ttype': ttype,
            'relation': relation,
        }

    def unregister_field(
        self,
        model_name: str,
        field_name: str,
    ) -> None:

        # Eliminación del registro
        del self.models[model_name]['fields'][field_name]

    def register_table(
        self,
        table_model: type[DeclarativeBase]
    ) -> None:

        # Obtención del nombre de la tabla
        table_name = table_model.__tablename__.replace('_', '.')
        # Se registra el modelo de la tabla en el diccionario de modelos
        self.models[table_name] = self._initialize_model_properties(table_model)
        # Registro de las propiedades de los campos de la tabla
        self.register_table_fields_atts(table_name)

    def register_table_fields_atts(
        self,
        model_name,
    ) -> None:

        # Obtención de los atributos de los campos de la tabla
        fields_atts = self._m_raworm.get_model_fields(model_name)

        # Registro de los campos
        for atts in fields_atts:
            # Destructuración de los valores en la tupla
            ( field_name, ttype, field_relation ) = atts
            # Registro por cada campo
            self.register_field(model_name, field_name, ttype, field_relation)

    def unregister_table(
        self,
        table_name: str
    ) -> None:

        # Obtención del modelo de la tabla
        table_model = self.models[table_name]['model']
        # Se borra el modelo
        del table_model
        # Se borra la llave y valor del diccionario de modelos
        del self.models[table_name]

    def initialize_fields_atts(
        self,
    ) -> None:

        # Registro de los atributos de campos de modelos existentes registrados
        for model_name in self.models.keys():
            self.register_table_fields_atts(model_name)

    def _initialize_model_properties(
        self,
        table_model: type[DeclarativeBase],
    ):

        return {
            'model': table_model,
            'fields': {}
        }
