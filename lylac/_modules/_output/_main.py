from typing import Any
import pandas as pd
import numpy as np
from ..._core import _BaseLylac
from ..._module_types import (
    SerializableDict,
    OutputOptions,
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

    def build_output(
        self,
        response: pd.DataFrame | list[dict[str, Any]],
        fields: list[str],
        specified_output: OutputOptions,
        default_output: OutputOptions | None = None,
    ) -> pd.DataFrame | list[dict[str, Any]]:
        
        # Obtención de los nombres de columna excluyendo el nombre de la tabla
        fields = [ str(i).split(".")[1] for i in fields ]

        # Si se especificó una salida para la ejecución actual...
        if specified_output:
            if specified_output == 'dataframe':
                return pd.DataFrame(response, columns= fields)
            else:
                return self._to_serializable_dict(response)

        # Si existe un formato por defecto en la instancia...
        if self._default_output:
            if self._default_output == 'dataframe':
                return pd.DataFrame(response, columns= fields)
            else:
                return self._to_serializable_dict(response)

        # Si no se especificó un formato en ejecución o instancia...
        if default_output == 'dataframe':
            return pd.DataFrame(response, columns= fields)

        # Retorno de información en lista de diccionarios
        return self._to_serializable_dict(response)

    def _to_serializable_dict(
        self,
        data: pd.DataFrame
    ) -> SerializableDict:
        """
        ## Conversión a diccionario serializable
        Este método interno convierte un DataFrame en una lista de diccionarios
        que puede ser convertida a JSON.
        """

        return (
            data
            .pipe(
                lambda df: (
                    df
                    # Reemplazo de todos los potenciales nulos no serializables
                    .replace({np.nan: None})
                    # Transformación de tipos no nativos en cadenas de texto
                    .astype(
                        {
                            col: 'string' for col in (
                                df
                                # Obtención de los tipos de dato del DataFrame
                                .dtypes
                                # Transformación de tipos de dato de serie
                                .astype('string')
                                # Filtro por tipos de dato no serializables
                                .pipe(
                                    lambda s: s[s.isin(['object', 'datetime64[ns]'])]
                                )
                                # Obtención de los nombres de columnas desde el índice
                                .index
                            )
                        }
                    )
                )
            )
            # Conversión a lista de diccionarios
            .to_dict('records')
        )
