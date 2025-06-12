from typing import (
    Any,
    Tuple,
)
from ..._core import _Lylac
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.selectable import Select

class Select_():

    def __init__(
        self,
        instance: _Lylac,
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Asignación de objeto de obtención de campos
        self._index = instance._index

    def build(
        self,
        model_name: str,
        fields: list[str] = []
    ) -> Select[Any]:

        # Obtención de los atributos de campo
        fields_atts = self._main._strc.get_fields_atts(model_name, fields)
        # Inicialización de lista de modelos relacionados
        related_models: list[Tuple[type[DeclarativeBase], InstrumentedAttribute[int]]] = []
        # Inicialización de los campos seleccionados
        selected_fields: list[InstrumentedAttribute[Any]] = []

        # Destructuración e iteración por los atributos de campos
        for ( field_name, ttype, related_model ) in fields_atts:
            # Obtención de la instancia de campo de la tabla
            field_instance = self._index[model_name][field_name]
            # Se añade la instancia a la lista de campos seleccionados
            selected_fields.append(field_instance)

            # Si el campo en cuestión está relacionado a un modelo externo...
            if ttype == 'many2one':
                # Creación de un alias del modelo relacionado
                alias = aliased( self._main._models.get_table_model(related_model) )
                # Obtención de la instancia de nombre en el modelo relacionado del campo
                related_field_instance = self._index[alias]['name'].label(f'{field_name}/name')
                # Se añade el modelo relacionado y su campo a la lista de modelos relacionados
                related_models.append( (alias, field_instance) )
                # Se añade el campo de nombre en el modelo relacionado a la lista de campo relacionados
                selected_fields.append(related_field_instance)

        # Creación del query
        stmt = select(*selected_fields)

        # Destructuración e iteración por modelos relacionados
        for (alias, field_instance) in related_models:
            # Creación de OUTER JOIN
            stmt = stmt.outerjoin(alias, field_instance == self._index[alias]['id'])

        return stmt
