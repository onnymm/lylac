from typing import TYPE_CHECKING
from .._resources import ActionProperties
from .._typing.generics import EngineHub
from .._typing.generics import ModelName
from .._typing.literals import OnDeleteOption
from .._typing.literals import TTypeName
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._contexts import ActionContext

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
    ctx._ddl.create_model_table(ctx._execution_ctx.conn, table_name, model_name, has_sequence, is_archivable, has_label)

def _base_model_field__create_field_column_and_register_on_model(ctx: ActionContext):

        # Obtención del nombre del campo
        field_name = ctx.data['name']
        # Obtención del tipo de dato del campo
        field_ttype: TTypeName = ctx.data['ttype']
        # Obtención del nombre del modelo
        model_name: ModelName = ctx.data['model_id.model']
        # Obtención del nombre de la tabla del modelo
        model_table_name: str = ctx.data['model_id.name']
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

PRESET_ACTIONS: EngineHub[_M, ActionProperties[_M]] = {

    'base.model': {
        'create_model': ActionProperties(
            'base.model',
            'create_model',
            _base_model__create_model,
        ),
    },

    'base.model.field': {
        'create_field_column_and_register_on_model': ActionProperties(
            'base.model.field',
            'create_field_column_and_register_on_model',
            _base_model_field__create_field_column_and_register_on_model,
            ('name', 'ttype', 'model_id.model', 'model_id.name', 'related_model_id.name', 'nullable', 'unique', 'default_value', 'on_delete'),
        ),
    },

}
