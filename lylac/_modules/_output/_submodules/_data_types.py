import pandas as pd
import numpy as np
from typing import Callable
from pandas._typing import AstypeArg
from ...._module_types import TType
from ._base import _BaseOutput

class _DataTypes():

    recover_ttype: dict[TType, Callable[[pd.DataFrame, str], pd.DataFrame]]

    def __init__(
        self,
        instance: _BaseOutput,
    ) -> None:

        # Asignación de la instancia propietaria
        self._output = instance
        # Referencia de la instancia principal
        self._main = instance._main

        # Inicialización del mapa de funciones de recuperación de tipo de dato
        self._build_recover_ttype()

    def _build_recover_ttype(
        self,
    ) -> None:

        # TODO Falta mapear tipos file y many2one
        self.recover_ttype: dict[TType, Callable[[pd.DataFrame, str], pd.DataFrame]] = {
            'integer': lambda df, field: self._recover_numeric(df, field, 'int'),
            'char': lambda df, field: self._bypass_value(df, field),
            'float': lambda df, field: self._recover_numeric(df, field, 'float'),
            'boolean': lambda df, field: self._recover_boolean(df, field),
            'date': lambda df, field: self._recover_time_alike(df, field),
            'datetime': lambda df, field: self._recover_time_alike(df, field),
            'time': lambda df, field: self._recover_time_alike(df, field),
            'file': lambda df, field: self._bypass_value(df, field),
            'text': lambda df, field: self._bypass_value(df, field),
            'selection': lambda df, field: self._bypass_value(df, field),
            'many2one': lambda df, field: self.transform_many2one(df, field),
        }

    def transform_many2one(
        self,
        data: pd.DataFrame,
        field: str
    ) -> pd.DataFrame:
        return (
            data
            .pipe(
                lambda df: self._recover_numeric(df, field, 'int')
            )
            .assign(
                **{
                    field: lambda df: df[[field, f'{field}/name']].apply(self._create_many2one_value, axis=1)
                }
            )
        )

    def _create_many2one_value(
        self,
        s: pd.Series,
    ) -> list:

        [ id_column, name_column ] = s.index.to_list()
        if s[id_column] is not None:
            return [
                s[id_column],
                s[name_column],
            ]
        else:
            return None

    def _bypass_value(self, data: pd.DataFrame, _: str) -> pd.DataFrame:
        return data

    def _recover_time_alike(self, data: pd.DataFrame, field: str) -> pd.DataFrame:
        return (
            data
            .replace({field: {np.nan: 'None'}})
            .astype({field: 'string'})
            .replace({field: {'None': None}})
        )

    def _recover_boolean(self, data: pd.DataFrame, field: str) -> pd.DataFrame:
        return data.replace({field: {np.nan: None}})

    def _recover_numeric(self, data: pd.DataFrame, field: str, type_arg: AstypeArg) -> pd.DataFrame:
        max_value = data[field].max()
        if max_value is np.nan:
            return data.replace({field: {np.nan: None}})
        else:
            return (
                data
                .replace({field: {np.nan: max_value + 1}})
                .astype({field: type_arg})
                .replace({field: {max_value + 1: None}})
            )
