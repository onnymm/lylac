from typing import (
    Any,
    Optional,
)
from ..._core import _Lylac
from ._module_types import (
    TTypesMapping,
    OperationData,
)
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
        # Asignación de instancia de estructura
        self._strc = instance._strc

    def build(
        self,
        model_name: str,
        fields: list[str] = [],
    ) -> tuple[Select[Any], TTypesMapping]:

        # Si no fue provista una lista de campos se toma la lista completa para iterar
        if len(fields) == 0:
            fields = self._strc.models[model_name]['fields'].keys()
        else:
            if 'id' in fields:
                fields.remove('id')
            fields.insert(0, 'id')

        # Inicialización de los datos de operación
        operation_data = OperationData()

        # Obtención del modelo de la tabla
        model_model = self._strc.models[model_name]['model']

        for field in fields:
            self._add_field(
                field,
                model_name,
                operation_data,
                model_model,
            )

        # Creación de query
        stmt = (
            select(*operation_data.field_instances)
        )

        # Se añaden los JOINs
        for ( related_model_model, on ) in operation_data.outerjoins:
            stmt = stmt.outerjoin(related_model_model, on)

        # Retorno de datos relevantes
        return ( stmt, operation_data.ttypes_mapping )

    def _add_field(
        self,
        field_name: str,
        model_name: str,
        operation_data: OperationData,
        model_model: Optional[type[DeclarativeBase]] = None,
    ) -> None:

        # Obtención de cadena de campos separados por punto
        fields_chain = field_name.split('.')

        # Si existe una cadena de campos...
        if len(fields_chain) > 1:

            # Obtención del nombre del campo inicial
            inicial_field_name = fields_chain[0]
            # Obtención de nombre del modelo relacionado
            related_model_name = self._strc.models[model_name]['fields'][inicial_field_name]['related_model']

            # Se envía el campo a obtención de relacionados
            self._add_related_field(
                fields_chain,
                model_model,
                related_model_name,
                operation_data,
                field_name,
            )

        # Si no existe una cadena de campos...
        else:
            # Se envía el campo a obtención individual
            self._proccess_field(
                field_name,
                model_name,
                operation_data,
                model_model,
            )

    def _add_related_field(
        self,
        refs: list[str],
        model_model: type[DeclarativeBase],
        related_model_name: str,
        operation_data: OperationData,
        label: Optional[str] = None
    ) -> None:

        # Obtención del nombre del campo actual
        current_field_name = refs[0]
        # Obtención del modelo relacionado
        related_model_model = aliased( self._strc.models[related_model_name]['model'] )

        # Obtención de la instancia del campo actual
        id_current_field_instance = self._index[model_model][current_field_name]

        # Se añade el outerjoin
        self._add_join(
            id_current_field_instance,
            related_model_model,
            operation_data,
        )

        # Obtención del nombre del campo siguiente
        next_field_name = refs[1]
        # Obtención del nombre del modelo relacionado del campo siguiente
        next_field_related_model_name = self._strc.models[related_model_name]['fields'][next_field_name]['related_model']

        # Si hay más campos por acceder...
        if len(refs) > 2:
            # Se accede a ellos de forma recursiva
            self._add_related_field(
                refs[1:],
                related_model_model,
                next_field_related_model_name,
                operation_data,
                label,
            )

        # Si el campo actual es el último a acceder
        else:
            # Se envía el campo a procesamiento individual
            self._proccess_field(
                next_field_name,
                related_model_name,
                operation_data,
                related_model_model,
                label,
            )

    def _proccess_field(
        self,
        field_name: str,
        model_name: str,
        operation_data: OperationData,
        model_model: Optional[type[DeclarativeBase]] = None,
        label: Optional[str] = None,
    ) -> None:

        # Obtención del tipo de dato del campo
        field_ttype = self._strc.models[model_name]['fields'][field_name]['ttype']

        if field_ttype == 'one2many':
            return

        # Obtención o reasignación de variable al modelo
        if model_model is not None:
            computed_model_model = model_model
        else:
            computed_model_model = aliased(self._strc.models[model_name]['model'])

        # Si el campo es many2one...
        if field_ttype == 'many2one':
            self._add_many2one_field(
                field_name,
                model_name,
                computed_model_model,
                operation_data,
                label,
            )
        # Si el campo es de otro tipo de dato...
        else:
            self._add_common_field(
                field_name,
                model_name,
                computed_model_model,
                operation_data,
                label,
            )

    def _add_many2one_field(
        self,
        field_name: str,
        model_name: str,
        model_model: type[DeclarativeBase],
        operation_data: OperationData,
        label: Optional[str] = None,
    ) -> None:

        # Obtención del nombre del modelo relacionado
        related_model_name = self._strc.models[model_name]['fields'][field_name]['related_model']
        # Obtención del modelo relacionado
        related_model_model = aliased( self._strc.models[related_model_name]['model'] )

        # Si una etiqueta de campo fue especificada
        if label is not None:
            # Se asigna ésta como nombre computado del campo
            field_computed_name = label
        # Si no fue especificada una etiqueta
        else:
            # Se asigna el nombre del campo como nombre computado de éste
            field_computed_name = field_name

        # Se añade el campo propio
        id_current_field_instance = self._add_common_field(
            field_name,
            model_name,
            model_model,
            operation_data,
            label,
        )

        # Se añade el campo relacionado
        self._add_common_field(
            'name',
            related_model_name,
            related_model_model,
            operation_data,
            f'{field_computed_name}/name',
            False,
        )

        # Se añade el JOIN
        self._add_join(
            id_current_field_instance,
            related_model_model,
            operation_data,
        )

    def _add_common_field(
        self,
        field_name: str,
        model_name: str,
        model_model: type[DeclarativeBase],
        operation_data: OperationData,
        label: Optional[str] = None,
        add_ttype: bool = True,
    ) -> InstrumentedAttribute[Any]:

        # Obtención del tipo de dato del campo
        field_ttype = self._strc.models[model_name]['fields'][field_name]['ttype']

        # Obtención de la instancia del campo
        field_instance = self._index[model_model][field_name]

        # Si fue especificada etiqueta de campo...
        if label is not None:
            # Se añade la etiqueta al campo
            field_instance = field_instance.label(label)
            # Se asigna ésta como nombre computado del campo
            field_computed_name = label
        # Si no fue especificada etiqueta de campo...
        else:
            # Se asigna el nombre del campo nombre computado de éste
            field_computed_name = field_name

        # Se añaden los datos obtenidos
        operation_data.field_instances.append(field_instance)
        # Se añade el tipo de dato si no se especificó lo contrario
        if add_ttype:
            operation_data.ttypes_mapping.append( (field_computed_name, field_ttype) )

        # Se retorna la instancia del campo para posibles usos
        return field_instance

    def _add_join(
        self,
        id_current_field_instance: InstrumentedAttribute,
        related_model_model: type[DeclarativeBase],
        operation_data: OperationData,
    ) -> None:

        # Obtención de instancia del campo de ID del modelo relacionado
        id_related_field = self._index[related_model_model]['id']
        # Creación de unión ON
        on = id_current_field_instance == id_related_field
        # Se añade el JOIN
        operation_data.outerjoins.append( (related_model_model, on) )
