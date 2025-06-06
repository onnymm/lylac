from typing import Any
import pandas as pd
from ..._core import _BaseLylac
from ..._module_types import OutputOptions
from ._modules import (
    _DataTypes,
    _RawORM,
)

class Output(_BaseLylac):

    def __init__(
        self,
        instance: _BaseLylac,
        output_format: OutputOptions | None
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Configuración de formato de salida por defecto
        self._default_output = output_format

        # Creación del submódulo de Tipos de dato
        self._data = _DataTypes(self)
        # Creación del submódulo de Raw ORM
        self._orm = _RawORM(self)

    def build_output(
        self,
        response: pd.DataFrame | list[dict[str, Any]],
        fields: list[str],
        specified_output: OutputOptions,
        table_name: str,
        default_output: OutputOptions | None = None,
    ) -> pd.DataFrame | list[dict[str, Any]]:

        # Inicialización de los nombres de columnas
        columns = [str(field).split('.')[1] for field in fields]

        # Preparación de los datos
        data: pd.DataFrame = (
            # Reasignación de nombres de columna
            pd.DataFrame(response, columns= columns)
            # Recuperación de tipos de dato
            .pipe( lambda df: self._recover_ttypes(df, table_name) )
        )

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
        ttypes = self._orm.get_fields_ttypes(table_name, data.columns.to_list())

        # Transformación de datos
        for ( field, ttype ) in ttypes.items():
            data = self._data.recover_ttype[ttype](data, field)

        return data
