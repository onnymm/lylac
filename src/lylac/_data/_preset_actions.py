from typing import TYPE_CHECKING
from .._constants import FACTORY_FIELDS
from .._constants import PRESET
from .._resources import ActionProperties
from .._typing.generics import EngineHub
from .._typing.generics import ModelName
from .._typing.literals import OnDeleteOption
from .._typing.literals import TTypeName
from .._typing.structures import CriteriaStructure
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._contexts import ActionContext

def _base_model__create_table_on_database(ctx: ActionContext):

    # Obtención del nombre de modelo
    table_name = ctx.data['name']
    # Obtención del modelo del modelo
    model_name = ctx.data['model']
    # Obtención de valor de si el modelo tiene secuencia
    has_sequence = ctx.data['has_sequence']
    # Obtención de valor de si el modelo permite archivar
    is_archivable = ctx.data['is_archivable']
    # Obtención de valor de si el modelo contiene leyenda
    has_label = ctx.data['has_label']

    # Creación de la clase del modelo
    ctx._ddl.create_model_table(ctx._execution_ctx.conn, table_name, model_name, has_sequence, is_archivable, has_label)

def _base_model__create_model(ctx: ActionContext):

    # Obtención del nombre de modelo
    table_name = ctx.data['name']
    # Obtención del modelo del modelo
    model_name = ctx.data['model']
    # Obtención de valor de si el modelo tiene secuencia
    has_sequence = ctx.data['has_sequence']
    # Obtención de valor de si el modelo permite archivar
    is_archivable = ctx.data['is_archivable']
    # Obtención de valor de si el modelo contiene leyenda
    has_label = ctx.data['has_label']

    # Creación de la clase del modelo
    ctx._execution_ctx.models_bearer.create_model_class(
        table_name,
        model_name,
        has_sequence,
        is_archivable,
        has_label,
    )

def _base_model__drop_table(ctx: ActionContext):

    # Obtención del nombre del modelo
    model_name = ctx.data['model']
    # Se elimina el modelo de los metadatos de Base
    ctx._ddl.delete_model_table(
        ctx._execution_ctx,
        model_name,
    )
    # Se elimina el modelo de los metadatos de Base
    ctx._ddl.delete_model_model(model_name)

def _base_model__delete_model(ctx: ActionContext):

    # Obttención del nombre del modelo
    model_name = ctx.data['model']
    # Se elimina el modelo de los metadatos de Base
    ctx._ddl.delete_model_model(model_name)

def _base_model_field__create_column(ctx: ActionContext):

    # Obtención del nombre del campo
    field_name = ctx.data['name']
    # Obtención del tipo de dato del campo
    field_ttype: TTypeName = ctx.data['ttype']
    # Obtención del nombre de la tabla del modelo
    model_table_name: str = ctx.data['model_id.name']
    # Obtención de valor predeterminado
    default_value: str = ctx.data['default_value']
    # Obtención del nombre de la tabla del modelo relacionado
    related_model_table_name: str = ctx.data['related_model_id.name']
    # Obtención de valor de en eliminación
    on_delete: OnDeleteOption = ctx.data['on_delete']

    # Se crea la columna en la tabla de la base de datos
    ctx._ddl.add_column_to_table(
        model_table_name,
        field_name,
        field_ttype,
        default_value,
        related_model_table_name,
        on_delete,
        ctx._execution_ctx.conn,
    )

def _base_model_field__register_on_model(ctx: ActionContext):

    # Obtención del nombre del campo
    field_name = ctx.data['name']
    # Obtención del tipo de dato del campo
    field_ttype: TTypeName = ctx.data['ttype']
    # Obtención del nombre del modelo
    model_name: ModelName = ctx.data['model_id.model']
    # Obtención de valor de nuleable
    nullable: bool = ctx.data['nullable']
    # Obtención de valor de único
    unique: bool = ctx.data['unique']
    # Obtención de valor predeterminado
    default_value: str = ctx.data['default_value']
    # Obtención del nombre de la tabla del modelo relacionado
    related_model_table_name: str = ctx.data['related_model_id.name']
    # Obtención de valor de en eliminación
    on_delete: OnDeleteOption = ctx.data['on_delete']

    # Se crea la instancia de campo en el modelo
    ctx._ddl.create_field_column(
        field_name,
        field_ttype,
        model_name,
        nullable,
        unique,
        default_value,
        related_model_table_name,
        on_delete,
    )

def _drop_column(ctx: ActionContext):

    # Obtención del nombre del campo
    field_name = ctx.data['name']
    # Obtención del nombre de la tabla del modelo
    table_name = ctx.data['model_id.name']

    # Eliminación de la columna del campo en la tabla
    ctx._ddl.drop_column(
        ctx._execution_ctx.conn,
        table_name,
        field_name,
    )

def _base_model__restore(ctx: ActionContext):

    # Creación del modelo SQLAlchemy
    ctx.action(
        'base.model',
        PRESET.AUTOMATION.BASE_MODEL__CREATE_MODEL,
        ctx.data['id'],
    )

    # Creación de criterio de búsqueda para encontrar todos los campos pertenientes al modelo
    criteria: CriteriaStructure = [
        '&',
            '&',
                ('model_id', '=', ctx.data['id']),
                ('name', 'not in', FACTORY_FIELDS),
            ('ttype', 'not in', ['one2many', 'many2many']),
    ]

    # Obtención de registros de campos a crear en los modelos de SQLAlchemy
    field_ids = ctx.search(
        'base.model.field',
        criteria,
    )

    # Iteración por cada ID de campo
    for field_id in field_ids:
        # Registro de la instancia del campo en el modelo
        ctx.action(
            'base.model.field',
            PRESET.AUTOMATION.BASE_MODEL_FIELD__REGISTER_ON_MODEL,
            field_id,
        )

PRESET_ACTIONS: EngineHub[_M, ActionProperties[_M]] = {

    'base.model': {

        PRESET.AUTOMATION.BASE_MODEL__CREATE_TABLE_ON_DATABASE: ActionProperties(
            'base.model',
            _base_model__create_table_on_database,
        ),

        PRESET.AUTOMATION.BASE_MODEL__CREATE_MODEL: ActionProperties(
            'base.model',
            _base_model__create_model,
            ('name', 'model', 'has_sequence', 'is_archivable', 'has_label'),
        ),

        PRESET.AUTOMATION.BASE_MODEL__DROP_TABLE: ActionProperties(
            'base.model',
            _base_model__drop_table,
            ('name',),
        ),

        PRESET.AUTOMATION.BASE_MODEL__DELETE_MODEL: ActionProperties(
            'base.model',
            _base_model__delete_model,
            ('model',),
        ),

        PRESET.AUTOMATION.BASE_MODEL__RESTORE: ActionProperties(
            'base.model',
            _base_model__restore,
            ('id',),
        ),

    },

    'base.model.field': {

        PRESET.AUTOMATION.BASE_MODEL_FIELD__CREATE_COLUMN: ActionProperties(
            'base.model.field',
            _base_model_field__create_column,
            ('name', 'ttype', 'model_id.name', 'related_model_id.name', 'default_value', 'on_delete'),
        ),

        PRESET.AUTOMATION.BASE_MODEL_FIELD__REGISTER_ON_MODEL: ActionProperties(
            'base.model.field',
            _base_model_field__register_on_model,
            ('name', 'ttype', 'model_id.model', 'related_model_id.name', 'nullable', 'unique', 'default_value', 'on_delete'),
        ),

        PRESET.AUTOMATION.BASE_MODEL_FIELD__DROP_COLUMN: ActionProperties(
            'base.model.field',
            _drop_column,
            ('name', 'model_id.name'),
        ),

    },

}
