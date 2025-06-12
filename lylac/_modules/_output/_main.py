from typing import Any
import pandas as pd
from ..._core import _Lylac
from ..._module_types import OutputOptions
from ._submodules import (
    _BaseOutput,
    _DataTypes,
    _RawORM,
)

class Output(_BaseOutput):

    def __init__(
        self,
        instance: _Lylac,
        output_format: OutputOptions | None
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Configuración de formato de salida por defecto
        self._default_output = output_format

        # Creación del submódulo de Tipos de dato
        self._m_data = _DataTypes(self)
        # Creación del submódulo de Raw ORM
        self._m_orm = _RawORM(self)

    def build_output(
        self,
        response: pd.DataFrame,
        fields: list[str],
        specified_output: OutputOptions,
        table_name: str,
        default_output: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | list[dict[str, Any]]:

        # Obtención de los atributos de los campos de los datos
        fields_atts = self._main._strc.get_fields_atts(table_name, fields)

        # Si no fue provista una lista de campos...
        if len(fields) == 0:
            # Se utilizan los campos provenientes de los atributos de campos
            fields = [ field for ( field, _, _ ) in fields_atts ]

        # Si el DataFrame de respuesta está vacío...
        if len(response) == 0:
            # Se inicializa un DataFrame con los nombres de campos y se reasigna a `data`
            data = pd.DataFrame(response, columns= fields)
        else:
            # Se reasigna el contenido de variable
            data = response
            # Destructuración e iteración de los atributos de campo
            for ( field, ttype, _ ) in fields_atts:
                # Si fue solicitado el manejo de solo IDs en campos relacionados...
                if only_ids_in_relations and ttype == 'many2one':
                    # Se manejan los tipos Many2One como enteros
                    ttype = 'integer'
                # Recuperación de tipos de dato por columna
                data = self._m_data.recover_ttype[ttype](data, field)

            # Selección de columnas
            data = data[fields]

        # Si se especificó una salida para la ejecución actual...
        if specified_output:
            if specified_output == 'dataframe':
                return data
            else:
                return data.to_dict('records')

        # Si existe un formato por defecto en la instancia...
        if self._default_output:
            if self._default_output == 'dataframe':
                return data
            else:
                return data.to_dict('records')

        # Si no se especificó un formato en ejecución o instancia...
        if default_output == 'dataframe':
            return data

        # Retorno de información en lista de diccionarios
        return data.to_dict('records')

    def _recover_ttypes(self, data: pd.DataFrame, table_name: str) -> pd.DataFrame:

        # Obtención del mapa de tipos de dato por campo
        ttypes = self._m_orm.get_fields_ttypes(table_name, data.columns.to_list())

        # Transformación de datos
        for ( field, ttype ) in ttypes.items():
            data = self._m_data.recover_ttype[ttype](data, field)

        return data
