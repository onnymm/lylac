import io
import json
from typing import Generic
from typing import TypedDict
from typing import TYPE_CHECKING
from .._constants import ENCODE_REF
from .._constants import ERROR_LABEL
from .._constants import MODEL_NAME
from .._typing.generics import ModelName
from .._typing.structures import FieldComputation
from .._typing.structures import RecordData
from .._typing.structures import RelationCommands
from .._typing.type_parameters import _M
from ..settings import DIRECTORY
from errors import ModuleAlreadyLoaded

if TYPE_CHECKING:
    from .._contexts import TransactionContext
    from .._main import Lylac

class _ModelData(TypedDict, Generic[_M]):
    name: str
    model_name: ModelName[_M]

class _Step(TypedDict, Generic[_M]):
    model_name: ModelName[_M]
    sequence: int
    record_data_ids: RelationCommands

class _ModuleData(TypedDict):
    name: str
    model_data: list[_ModelData]
    data: list[RecordData]

MODEL_ID__RES_NAME__FIELD_COMPUTATION: FieldComputation = (
    'model_id',
    'char',
    lambda ctx: ctx.case(
        (
            ctx['model_id.id'] != None,
            ctx.concat(ENCODE_REF.START, 'base_model.', ctx['model_id.name'], ENCODE_REF.END)
        )
    )
)

RELATED_MODEL_ID__RES_NAME__FIELD_COMPUTATION: FieldComputation = (
    'related_model_id',
    'char',
    lambda ctx: ctx.case(
        (
            ctx['related_model_id.id'] != None,
            ctx.concat(ENCODE_REF.START, 'base_model.', ctx['related_model_id.name'], ENCODE_REF.END)
        )
    )
)

class Modules(Generic[_M]):

    def __init__(
        self,
        main: 'Lylac[_M]',
    ) -> None:

        # Asignación de la instancia principal
        self._main = main

    def export(
        self,
        name: str,
        model_names: list[ModelName[_M]],
    ) -> None:

        # Inicialización de función de exportación
        def transaction(ctx: TransactionContext[_M]) -> None:

            # Inicialización de datos de modelos
            models_data: list[_ModelData] = []
            # Inicialización de registros de pasos
            step_ids: list[_Step] = []
            # Inicialización de registros referenciados
            record_data_ids: dict[ModelName, list[RecordData]] = {
                MODEL_NAME.BASE_MODEL: [],
                MODEL_NAME.BASE_MODEL_FIELD: [],
                MODEL_NAME.BASE_MODEL_FIELD_SELECTION: [],
                MODEL_NAME.BASE_USER_ACCESS: [],
                MODEL_NAME.BASE_USER_GROUPS: [],
                MODEL_NAME.BASE_RULES: [],
            }
            # Inicialización de diccionario de secuencias
            sequence: dict[ModelName, int] = {
                MODEL_NAME.BASE_MODEL: 1,
                MODEL_NAME.BASE_MODEL_FIELD: 1,
                MODEL_NAME.BASE_MODEL_FIELD_SELECTION: 1,
                MODEL_NAME.BASE_USER_ACCESS: 1,
                MODEL_NAME.BASE_USER_GROUPS: 1,
                MODEL_NAME.BASE_RULES: 1,
            }
            # Inicialización de datos de proceso
            process: RecordData = {
                'name': name,
                'step_ids': {
                    'create': step_ids,
                },
            }
            # Se añaden las referencias de registros referenciados
            step_ids.append({
                'model_name': MODEL_NAME.BASE_MODEL,
                'sequence': 1,
                'record_data_ids': {
                    'create': record_data_ids[MODEL_NAME.BASE_MODEL],
                },
            })
            step_ids.append({
                'model_name': MODEL_NAME.BASE_MODEL_FIELD,
                'sequence': 2,
                'record_data_ids': {
                    'create': record_data_ids[MODEL_NAME.BASE_MODEL_FIELD],
                },
            })
            step_ids.append({
                'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
                'sequence': 3,
                'record_data_ids': {
                    'create': record_data_ids[MODEL_NAME.BASE_MODEL_FIELD_SELECTION],
                },
            })
            step_ids.append({
                'model_name': MODEL_NAME.BASE_USER_GROUPS,
                'sequence': 4,
                'record_data_ids': {
                    'create': record_data_ids[MODEL_NAME.BASE_USER_GROUPS],
                },
            })
            step_ids.append({
                'model_name': MODEL_NAME.BASE_USER_ACCESS,
                'sequence': 5,
                'record_data_ids': {
                    'create': record_data_ids[MODEL_NAME.BASE_USER_ACCESS],
                },
            })
            step_ids.append({
                'model_name': MODEL_NAME.BASE_RULES,
                'sequence': 6,
                'record_data_ids': {
                    'create': record_data_ids[MODEL_NAME.BASE_RULES],
                },
            })

            # Iteración por cada uno de los modelos solicitados
            for model_name in model_names:
                # Obtención de los datos del modelo
                [ base_model__metadata ] = ctx.search_read(
                    MODEL_NAME.BASE_MODEL,
                    [('model', '=', model_name)],
                    [
                        'name',
                        'model',
                        'label',
                        'description',
                        'has_sequence',
                        'is_archivable',
                        'has_label',
                        'transient',
                        'field_ids',
                    ],
                )
                # Se elimina el valor de ID
                del base_model__metadata['id']
                # Obtención de las IDs de campos
                field_ids: list[int] = base_model__metadata.pop('field_ids')
                # Obtención del nombre de tabla del modelo
                model_table_name = base_model__metadata['name']
                # Construcción del nombre del recurso
                base_model__res_name = f'base_model.{model_table_name}'

                # Construcción del registro de datos de modelo
                base_model__model_data: _ModelData = {
                    'name': base_model__res_name,
                    'model_name': MODEL_NAME.BASE_MODEL,
                }
                # Se añade el registro a los datos de modelo
                models_data.append(base_model__model_data)

                # Se añaden los datos del registro a crear
                record_data_ids[MODEL_NAME.BASE_MODEL].append({
                    'name': base_model__res_name,
                    'sequence': sequence[MODEL_NAME.BASE_MODEL],
                    'data': base_model__metadata,
                })

                # Obtención de los datos de los campos
                base_model_field__metadata = ctx.search_read(
                    MODEL_NAME.BASE_MODEL_FIELD,
                    [
                        '&',
                            ('id', 'in', field_ids),
                            ('name', 'not in', ['id', 'name', 'create_date', 'update_date', 'create_uid', 'update_uid', 'display_name', 'label', 'active', 'sequence'])
                    ],
                    [
                        'name',
                        'label',
                        MODEL_ID__RES_NAME__FIELD_COMPUTATION,
                        'ttype',
                        'nullable',
                        'on_delete',
                        'is_required',
                        'readonly',
                        'default_value',
                        'unique',
                        'help_info',
                        RELATED_MODEL_ID__RES_NAME__FIELD_COMPUTATION,
                        'related_field',
                        'is_computed',
                    ],
                )

                # Iteración por cada uno de los registros encontrados
                for field_metadata_i in base_model_field__metadata:
                    # Se remueve el valor de ID de los metadatos del registro
                    del field_metadata_i['id']
                    # Obtención del nombre del campo
                    field_i_name = field_metadata_i['name']

                    # Construcción del nombre de recurso
                    base_model_field__res_name = f'base_model_field.{model_table_name}__{field_i_name}'
                    # Construcción del registro de datos de modelo
                    base_model_field__model_data: _ModelData = {
                        'name': base_model_field__res_name,
                        'model_name': MODEL_NAME.BASE_MODEL_FIELD,
                    }
                    # Se añade éste a los datos de modelo
                    models_data.append(base_model_field__model_data)

                    # Se añaden los datos del registro a crear
                    record_data_ids[MODEL_NAME.BASE_MODEL_FIELD].append({
                        'name': base_model_field__res_name,
                        'sequence': sequence[MODEL_NAME.BASE_MODEL_FIELD],
                        'data': field_metadata_i,
                    })

                    # Incremento en secuencia
                    sequence[MODEL_NAME.BASE_MODEL_FIELD] += 1

                # Búsqueda de campos de tipo selección
                selection_ttype_field_ids = ctx.search_read(
                    MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
                    [('field_id.id', 'in', field_ids)],
                    [
                        'name',
                        'label',
                        (
                            'field_id',
                            'char',
                            lambda ctx: ctx.case(
                                (
                                    ctx['field_id.id'] != None,
                                    ctx.concat(ENCODE_REF.START, 'base_model_field.', ctx['field_id.model_id.name'], '__', ctx['field_id.name'], ENCODE_REF.END)
                                )
                            )
                        ),
                        ('field_id.name', 'field_name'),
                    ]
                )

                # Iteración por cada valor de selección de campo encontrado
                for selection_field_id in selection_ttype_field_ids:
                    # Se remueve el valor de ID de los metadatos del valor de selección
                    del selection_field_id['id']
                    # Obtención del nombre del campo
                    field_name = selection_field_id.pop('field_name')
                    # Obtención del nombre del valor de selección
                    selection_name = selection_field_id['name']
                    # Construcción del nombre de recurso
                    base_model_field_selection__res_name = f'base_model_field_selection.{model_name}__{field_name}__{selection_name}'
                    # Construcción del registro de datos de modelo
                    base_model_field_selection__model_data: _ModelData = {
                        'name': base_model_field_selection__res_name,
                        'model_name': MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
                    }
                    # Se añade éste a los datos de modelo
                    models_data.append(base_model_field_selection__model_data)

                    # Se añaden los datos del registro a crear
                    record_data_ids[MODEL_NAME.BASE_MODEL_FIELD_SELECTION].append({
                        'name': base_model_field_selection__res_name,
                        'sequence': sequence[MODEL_NAME.BASE_MODEL_FIELD_SELECTION],
                        'data': selection_field_id,
                    })

                    # Incremento en secuencia
                    sequence[MODEL_NAME.BASE_MODEL_FIELD_SELECTION] += 1

                # Incremento en secuencia
                sequence[MODEL_NAME.BASE_MODEL] += 1

                # Búsqueda de reglas de registro del modelo
                base_rules__metadata = ctx.search_read(
                    MODEL_NAME.BASE_RULES,
                    [('model_id.model', '=', model_name)],
                    fields= [
                        'name',
                        'active',
                        'domain',
                        'global_',
                        'label',
                        'perm_create',
                        'perm_read',
                        'perm_update',
                        'perm_delete',
                        MODEL_ID__RES_NAME__FIELD_COMPUTATION,
                        (
                            'res_name',
                            'char',
                            lambda ctx: ctx.case(
                                (
                                    ctx['model_id.id'] != None,
                                    ctx.concat('base_rules.', ctx['model_id.name'], '__', ctx['name'])
                                )
                            )
                        ),
                    ],
                )

                # Iteración por cada registro de reglas de registro encontradas
                for base_rule_i in base_rules__metadata:
                    # Remoción del valor de ID
                    del base_rule_i['id']
                    # Obtención del nombre de recurso
                    base_rule__res_name = base_rule_i.pop('res_name')

                    # Construcción del registro de datos de modelo
                    base_rule__model_data: _ModelData = {
                        'name': base_rule__res_name,
                        'model_name': MODEL_NAME.BASE_RULES,
                    }
                    # Se añade éste a los datos de modelo
                    models_data.append(base_rule__model_data)

                    # Se añaden los datos del registro a crear
                    record_data_ids[MODEL_NAME.BASE_RULES].append({
                        'name': base_rule__res_name,
                        'sequence': sequence[MODEL_NAME.BASE_RULES],
                        'data': base_rule_i,
                    })

                    # Incremento en secuencia
                    sequence[MODEL_NAME.BASE_RULES] += 1

            # Búsqueda de los permisos de permiso
            base_user_access__metadata = ctx.search_read(
                MODEL_NAME.BASE_USER_ACCESS,
                [('model_id.model', 'in', model_names)],
                [
                    'name',
                    'perm_create',
                    'perm_read',
                    'perm_update',
                    'perm_delete',
                    ('group_id.id', 'group_id_id'),
                    ('group_id.name', 'group_name'),
                    (
                        'group_id',
                        'char',
                        lambda ctx: ctx.case(
                            (
                                ctx['group_id.id'] != None,
                                ctx.concat(ENCODE_REF.START, 'base_user_groups.', ctx['group_id.name'], ENCODE_REF.END)
                            )
                        )
                    ),
                    MODEL_ID__RES_NAME__FIELD_COMPUTATION,
                ]
            )

            # Inicialización de lista de grupos a leer
            group_ids: list[int] = []

            # Iteración por cada registro de permiso de acceso
            for access_metadata_i in base_user_access__metadata:
                # Remoción del valor de ID
                del access_metadata_i['id']
                # Obtención de la ID de grupo
                group_id = access_metadata_i.pop('group_id_id')
                # Se añade ésta a las IDs de grupos a leer
                group_ids.append(group_id)
                # Obtención del nombre del grupo
                group_name = access_metadata_i.pop('group_name')
                # Obtención del nombre del permiso de acceso
                access_name = access_metadata_i['name']
                # Construcción del nombre de recurso
                base_user_access__res_name = f'base_user_access.{group_name}__{access_name}'
                # Construcción del registro de datos de modelo
                base_user_access__model_data: _ModelData = {
                    'name': base_user_access__res_name,
                    'model_name': MODEL_NAME.BASE_USER_ACCESS,
                }
                # Se añade éste a los datos de modelo
                models_data.append(base_user_access__model_data)

                # Se añaden los datos del registro a crear
                record_data_ids[MODEL_NAME.BASE_USER_ACCESS].append({
                    'name': base_user_access__res_name,
                    'sequence': sequence[MODEL_NAME.BASE_USER_ACCESS],
                    'data': access_metadata_i,
                })

                # Incremento en secuencia
                sequence[MODEL_NAME.BASE_USER_ACCESS] += 1

            # Búsqueda de los grupos mencionados por los accesos
            base_user_groups__metadata = ctx.search_read(
                MODEL_NAME.BASE_USER_GROUPS,
                ['&', ('id', 'in', group_ids), ('name', '!=', 'basic_permissions')],
                ['name', 'label'],
            )

            # Iteración por cada registro de grupo
            for group_metadata_i in base_user_groups__metadata:
                # Remoción del valor de ID
                del group_metadata_i['id']
                # Obtención del nombre del grupo
                group_name = group_metadata_i['name']
                # Construcción del nombre del recurso
                base_user_groups__res_name = f'base_user_groups.{group_name}'
                # Construcción del registro de datos de modelo
                base_user_groups__model_data: _ModelData = {
                    'name': base_user_groups__res_name,
                    'model_name': MODEL_NAME.BASE_USER_GROUPS,
                }
                # Se añade éste a los datos de modelo
                models_data.append(base_user_groups__model_data)

                # Se añaden los datos del registro a crear
                record_data_ids[MODEL_NAME.BASE_USER_GROUPS].append({
                    'name': base_user_groups__res_name,
                    'sequence': sequence[MODEL_NAME.BASE_USER_GROUPS],
                    'data': group_metadata_i,
                })

                # Incremento en secuencia
                sequence[MODEL_NAME.BASE_USER_GROUPS] += 1

            # Construcción del objeto de datos de módulo a exportar
            module_data = {
                'name': name,
                'model_data': models_data,
                'data': process
            }

            # Se guardan los datos en archivo JSON
            with open(f'./{DIRECTORY.MODULES}/{name}.json', 'w', encoding= 'utf-8') as file:
                json.dump(
                    module_data,
                    file,
                    indent= 4,
                    ensure_ascii= False,
                )

        # Ejecución de la transacción
        self._main._execute_as_root(transaction)

    def load(
        self,
        file: io.FileIO,
    ) -> None:

        # Carga de los datos del módulo
        module_data: _ModuleData = json.load(file)
        name = module_data['name']
        model_data = module_data['model_data']
        data = module_data['data']

        # Inicialización de la función de transacción
        def transaction(ctx: TransactionContext[_M]):

            # Búsqueda de paquetes cargados
            count = ctx.search_count(
                MODEL_NAME.BASE_MODEL_DATA_PROCESS,
                [('name', '=', name)]
            )

            # Si ya existen procesos instalados...
            if count:
                # Se lanza error de módulo ya cargado
                raise ModuleAlreadyLoaded(ERROR_LABEL.MODULE_ALREADY_LOADED)

            # Creación de los datos de modelo
            ctx.create(
                MODEL_NAME.BASE_MODEL_DATA,
                model_data,
            )

            # Creación de los datos de instalación
            ctx.create(
                MODEL_NAME.BASE_MODEL_DATA_PROCESS,
                data,
            )

        # Ejecución de la transacción
        self._main._execute_as_root(transaction)
