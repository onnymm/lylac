from ..._constants import (
    MODEL_NAME,
    FIELD_NAME,
)
from ..._core.main import _Lylac_Core
from ..._module_types import (
    ComputedFieldCallback,
    ModelName,
    TType,
)
from ..._core.modules import Compute_Core
from ._submodules import _Automations

class Compute(Compute_Core):

    hub = dict[ModelName, dict[str, ComputedFieldCallback]]

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Inicialización de submódulo de automatizaciones
        self._m_automations = _Automations(self)

        # Inicialización del módulo
        self._initialize()

    def _initialize(
        self,
    ) -> None:

        # Obtención de los nombres de los modelos
        models = self._main._strc.get_model_names()
        # Inicialización del núcleo de campos computados
        self.hub = { model: {} for model in models }

    def register_computed_field(
        self,
        model_name: ModelName,
        ttype: TType,
        field_name: str,
        field_label: str,
        compute_field_callback: ComputedFieldCallback,
    ) -> None:

        # Búsqueda del registro del modelo
        [ record ] = self._main.search_read(
            self._main._ROOT_USER,
            MODEL_NAME.BASE_MODEL,
            [('model', '=', model_name)],
            output_format= 'dict',
        )
        # Obtención de la ID del modelo
        model_id = record[FIELD_NAME.ID]

        # Búsqueda de algún campo computado existente
        found_ids = self._main.search(
            self._main._ROOT_USER,
            MODEL_NAME.BASE_MODEL_FIELD,
            [
                '&',
                    ('name', '=', field_name),
                    '&',
                        ('model_id', '=', model_id),
                        '&',
                            ('ttype', '=', ttype),
                            ('is_computed', '=', True),
            ]
        )

        # Si no se encontraron coincidencias...
        if not found_ids:
            # Se crea el registro en la base de datos
            [ created_field_id ] = self._main.create(
                self._main._ROOT_USER,
                MODEL_NAME.BASE_MODEL_FIELD,
                {
                    'name': field_name,
                    'label': field_label,
                    'ttype': ttype,
                    'model_id': model_id,
                    'is_computed': True,
                },
            )

            # Obtención de posibles valores de selección
            selection_values = (
                self._main.search_read(
                    self._main._ROOT_USER,
                    'base.model.field.selection',
                    [('field_id', '=', created_field_id)],
                    ['name'],
                    output_format= 'dataframe',
                )
                ['name']
                .to_list()
            )

        # Registro de la función
        self._register_field_computation(model_name, field_name, compute_field_callback)
        # Registro de campo en la estructura
        self._main._strc.register_field(model_name, field_name, ttype, None, None, selection_values, True)

    def _register_field_computation(
        self,
        model_name: ModelName,
        field_name: str,
        computation_callback: ComputedFieldCallback,
    ) -> None:

        # Registro de la función en el núcleo
        self.hub[model_name][field_name] = computation_callback

    def register_model(
        self,
        model_name: ModelName,
    ) -> None:

        # Registro del modelo como un diccionario vacío
        self.hub[model_name] = {}

    def unregister_model(
        self,
        model_name: ModelName,
    ) -> None:

        # Se elimina el diccionario del modelo
        del self.hub[model_name]
