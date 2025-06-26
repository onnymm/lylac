from typing import Tuple
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._core import (
    _Lylac,
    BaseStructure,
)
from ..._data import fields_atts
from ..._module_types import TType, ModelMap
from ._submodules import (
    _Automations,
    _RawORM,
)

class Structure(BaseStructure):

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
        self._initialize()

    def get_model(
        self,
        model_name: str,
    ) -> type[DeclarativeBase]:

        return self.models[model_name]['model']

    def get_table_name(
        self,
        model_model: type[DeclarativeBase] | str,
    ) -> str:

        # Obtención del modelo en caso de haberse proporcionado una valor en texto
        if isinstance(model_model, str):
            model_model = self.get_model(model_model)
        # Obtención del nombre de la tabla
        table_name = model_model.__tablename__

        return table_name

    def get_registered_model_names(
        self,
    ) -> list[str]:

        # Obtención de los nombres de modelos registrados en la estructura
        registered_model_names = list( self.models.keys() )

        return registered_model_names

    def get_model_field_names(
        self,
        model_name: str,
    ) -> list[str]:

        # Obtención de los nombres de campos existentes del modelo especificado
        field_names = list( self.models[model_name]['fields'].keys() )

        return field_names

    def get_field_ttype(
        self,
        model_name: str,
        field_name: str,
    ) -> TType:

        # Obtención del tipo de dato del campo
        ttype = self.models[model_name]['fields'][field_name]['ttype']

        return ttype

    def get_related_model_name(
        self,
        model_name: str,
        field_name: str,
    ) -> str:

        # Obtención del modelo relacionado
        related_model_name = self.models[model_name]['fields'][field_name]['related_model']

        return related_model_name

    def get_related_field_name(
        self,
        model_name: str,
        field_name: str,
    ) -> str:

        # Obtención del campo de ID relacionado
        related_field_name = self.models[model_name]['fields'][field_name]['related_field']

        return related_field_name

    def register_field(
        self,
        model_name: str,
        field_name: str,
        ttype: TType,
        related_model: str | None,
        related_field: str | None
    ) -> None:

        # Asignación de valores
        self.models[model_name]['fields'][field_name] = {
            'ttype': ttype,
            'related_model': related_model,
            'related_field': related_field,
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
        model_model: type[DeclarativeBase]
    ) -> None:

        # Obtención del nombre de la tabla
        table_name = self.get_table_name(model_model)
        # Obtención del nombre del modelo
        model_name = table_name.replace('_', '.')
        # Se registra el modelo de la tabla en el diccionario de modelos
        self.models[model_name] = self._initialize_model_properties(model_model)
        # Registro de las propiedades de los campos de la tabla
        self.register_table_fields_atts(model_name)

    def register_table_fields_atts(
        self,
        model_name,
    ) -> None:

        # Obtención de los atributos de los campos de la tabla
        fields_atts = self._m_raworm.get_model_fields(model_name)

        # Registro de los campos
        for atts in fields_atts:
            # Destructuración de los valores en la tupla
            ( field_name, ttype, related_model, related_field ) = atts
            # Registro por cada campo
            self.register_field(model_name, field_name, ttype, related_model, related_field)

    def unregister_table(
        self,
        model_name: str
    ) -> None:

        # Obtención del modelo de la tabla
        table_model = self.get_model(model_name)
        # Se borra el modelo
        del table_model
        # Se borra la llave y valor del diccionario de modelos
        del self.models[model_name]

    def initialize_fields_atts(
        self,
    ) -> None:

        # Registro de los atributos de campos de modelos existentes registrados
        for model_name in self.models.keys():
            self.register_table_fields_atts(model_name)

    def _initialize(
        self,
    ) -> None:

        # Obtención del set de mapeadores de la tabla
        mappers = list(self._main._base.registry.mappers)
        # Inicialización de mapeo de modelos
        self.models = {}

        # Iteración por mapeador de SQLAlchemy
        for mapper in mappers:
            # Obtención de los datos desde los datos prestablecidos
            model_map = self._initialize_model_properties(mapper.class_, True)
            # Obtención del nombre de la tabla
            table_name: str = getattr(mapper.class_, '__tablename__')
            # Creación del nombre del modelo
            model_name = table_name.replace('_', '.')
            # Se añaden las propiedades al mapeo de módulos
            self.models[model_name] = model_map

    def _initialize_model_properties(
        self,
        table_model: type[DeclarativeBase],
        from_data: bool = False,
    ):

        # Obtención del nombre del modelo
        model_name = table_model.__tablename__.replace('_', '.')

        # Si el parámetro de obtener desde los datos predeterminados es verdedero...
        if from_data:
            # Se obtienen los datos correspondientes
            fields_data = fields_atts[model_name]
        # Si el parámetro de obtener desde los datos predeterminados es falso...
        else:
            # Se inicializa un diccionario vacío para el mapa de campos
            fields_data = {}

        return {
            'model': table_model,
            'fields': fields_data
        }
