from sqlalchemy import select
from sqlalchemy.engine import Connection
from sqlalchemy.orm import aliased
from typing import Any
from typing import Generator
from typing import Generic
from .._constants import RELATION_PATH_SEPARATOR
from .._core import Metadata
from .._core import Transaction
from .._typing.literals import TTypeName
from .._typing.generics import ModelName
from .._typing.structures import RawFieldProperties
from .._typing.type_parameters import _M
from ._field_properties import FieldProperties

class DatabaseMetadata(Generic[_M]):
    _hub: dict[ModelName[_M], dict[str, FieldProperties]]

    def __init__(
        self,
    ) -> None:

        # Inicialización de instancia de transacciones
        self._transaction = Transaction()
        # Se establece el valor de inicializado en falso
        self._initialized = False

    @property
    def initialized(
        self,
    ) -> bool:

        return self._initialized

    def get_field_names_from_model(
        self,
        model_name: ModelName[_M],
    ) -> list[str]:

        # Inicialización de lista de nombres de campos a retornar
        field_names: list[str] = []

        # Obtención de propiedades de campos en valores de diccionario
        field_properties = self._hub[model_name].values()

        # Iteración por cada instancia de propiedades de modelo
        for field_property in field_properties:
            # Se añade el nombre del modelo a la lista
            field_names.append(field_property.name)

        return field_names

    def get_fields_properties_by_ttypes(
        self,
        model_name: ModelName[_M],
        ttypes: list[TTypeName],
    ) -> list[FieldProperties]:

        # Inicialización de lista de nombres de campos a retornar
        relation_fields_properties: list[FieldProperties] = []

        # Obtención de propiedades de campos en valores de diccionario
        field_properties = self._hub[model_name].values()
        # Iteración por cada instancia de propiedades de modelo
        for field_property in field_properties:
            # Si el tipo de dato del campo está en los tipos proporcionados
            if field_property.ttype in ttypes:
                # Se añade éste a la lista a retornar
                relation_fields_properties.append(field_property)

        return relation_fields_properties

    def field_properties(
        self,
        model_name: ModelName[_M],
        field_name: str,
    ) -> FieldProperties[_M]:

        # Si el nombre es referencia
        if RELATION_PATH_SEPARATOR in field_name:

            # Obtención de la ruta de campos y el nombre real del campo
            ( fields_path, field_name ) = self._split_path_and_name(field_name)
            # Asignación de referencia de modelo padre
            parent_model_name = model_name

            # Iteración por cada campo de la ruta
            for field_i in fields_path:
                # Obtención de las propiedades del campo i de la ruta
                properties_i = self._hub[parent_model_name][field_i]
                # Reasignación de referencia de modelo padre
                parent_model_name = properties_i.related_model_name

            # Una vez terminada la iteración se obtienen las propiedades del campo buscado
            properties = self._hub[parent_model_name][field_name]

        # Si el nombre no es una referencia...
        else:
            # Obtención de las propiedades del campo
            properties = self._hub[model_name][field_name]

        return properties

    def update(
        self,
        conn: Connection,
    ) -> None:

        # Ejecución de la función de construcción de mapa de metadatos
        self.build(conn)

    def build(
        self,
        conn: Connection,
    ) -> None:

        # Inicialización del centro de datos
        self._hub = {}

        # Obtención del modelo de campos de modelos
        base_model_field = Metadata.BaseModelField
        # Obtención de un alias del modelo de modelos
        base_model = aliased(Metadata.BaseModel)
        # Obtención de un alias del modelo de modelos para modelos relacionados
        related_model = aliased(Metadata.BaseModel)

        # Query para obtención de nombre de modelo desde la tabla de modelos
        stmt = select(Metadata.BaseModel.model)
        # Obtención de los datos
        data: list[tuple[ModelName[_M]]] = self._transaction.search_read(stmt, conn)

        # Iteración por cada modelo encontrado
        for ( model_name, ) in data:

            # Inicialización del espacio de propiedades para el modelo
            self._hub[model_name] = {}

            # Construcción de query para obtención de metados de campos
            stmt = (
                # Seleccionar...
                select(
                    # Nombre del campo
                    base_model_field.name,
                    # Tipo de dato del campo
                    base_model_field.ttype,
                    # El campo es computado
                    base_model_field.is_computed,
                    # Nombre de modelo del modelo relacionado
                    related_model.model,
                    # Campo relacionado
                    base_model_field.related_field,
                )
                # Donde se cumplan las condiciones...
                .where(
                    # Nombre de modelo del modelo es igual al nombre de modelo provisto
                    base_model.model == model_name,
                )
                # LEFT JOIN desde campos de modelos hacia modelos
                .outerjoin(base_model, base_model_field.model_id == base_model.id)
                # LEFT JOIN desde campos de modelos hacia modelos relacionados
                .outerjoin(related_model, base_model_field.related_model_id == related_model.id)
            )

            # Obtención de los metadatos de los campos
            fields_metadata: list[RawFieldProperties[_M]] = self._transaction.search_read(stmt, conn)

            # Iteración por los metadatos de los campos
            for ( field_name, field_ttype, is_computed, related_model_name, related_field ) in fields_metadata:
                # Se guardan las propiedades
                self._hub[model_name][field_name] = FieldProperties(
                    field_name,
                    field_ttype,
                    is_computed,
                    related_model_name,
                    related_field,
                )

        # Se establece el valor de inicializado en verdadero
        self._initialized = True

    def _split_path_and_name(
        self,
        path_and_name: str,
    ) -> tuple[list[str], str]:

        # Obtención de cada fragmento de la ruta de campos
        complete_path = path_and_name.split(RELATION_PATH_SEPARATOR)

        # Construcción de ruta de campos sin el campo destino
        fields_path = complete_path[:-1]
        # Extracción del nombre de campo cuyas propiedades serán buscadas
        field_name = complete_path[-1]

        return (fields_path, field_name)

    @property
    def model_names(
        self,
    ) -> Generator[ModelName[_M], Any, None]:

        # Se retornan los nombres de modelo
        for model_name_i in self._hub.keys():
            yield model_name_i
