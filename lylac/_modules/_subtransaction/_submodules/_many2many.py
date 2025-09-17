from ...._core.modules import Subtransaction_Core
from .._contexts import RelationalContext
from typing import (
    Callable,
    overload,
)
from ...._module_types import (
    SubtransactionCreateMode,
    SubtransactionUpdateMode,
    Many2ManyUpdatesOnCreateCallback,
    Many2ManyUpdatesOnUpdateCallback,
    ModelName,
    RecordIDs,
    SubtransactionCommands,
    SubtransactionName,
)

class _Many2Many():

    def __init__(
        self,
        instance: Subtransaction_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._subtransaction = instance
        # Asignación de la instancia principal
        self._main = instance._main

        # Asignación de la instancia de estructura interna
        self._strc = instance._main._strc
        # Asignación de la instancia de compilador
        self._compiler = instance._main._compiler

        # Inicialización de mapa de subtransacciones
        self._initialize_subtransactions_map()

    @overload
    def _create_postcallback(
        self,
        callback: Callable[[list], None],
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _create_postcallback(
        self,
        callback: Callable[[list], None],
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _create_records(
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _create_records(
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _update_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _update_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _delete_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _delete_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _add_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _add_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _unlink_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _unlink_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _clean_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _clean_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _replace_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _replace_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _create_subtransactions_per_field(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> list[Many2ManyUpdatesOnCreateCallback]:
        ...

    @overload
    def _create_subtransactions_per_field(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> list[Many2ManyUpdatesOnUpdateCallback]:
        ...

    def create_many2many_updates_for_creation_mode(
        self,
        model_name: ModelName,
        many2many_field: str,
        subtransaction_commands: list[SubtransactionCommands],
        index: int,
    ) -> list[Many2ManyUpdatesOnCreateCallback]:

        # Obtención del modelo relacionado
        related_model_name = self._strc.get_related_model_name(model_name, many2many_field)
        # Se crea la instancia del contexto
        ctx = RelationalContext[SubtransactionCreateMode](
            model_name,
            related_model_name,
            many2many_field,
            None,
            subtransaction_commands,
            'create',
            index,
        )

        # Creación de las funciones de subtransacciones por campo
        subtransactions_per_field = self._create_subtransactions_per_field(ctx)

        return subtransactions_per_field

    def create_many2many_updates_for_update_mode(
        self,
        model_name: ModelName,
        many2many_field: str,
        subtransaction_commands: list[SubtransactionCommands],
        record_ids: RecordIDs,
    ) -> list[Many2ManyUpdatesOnUpdateCallback]:

        # Obtención del modelo relacionado
        related_model_name = self._strc.get_related_model_name(model_name, many2many_field)
        # Se crea la instancia del contexto
        ctx = RelationalContext[SubtransactionUpdateMode](
            model_name,
            related_model_name,
            many2many_field,
            record_ids,
            subtransaction_commands,
            'update',
        )

        # Creación de las funciones de subtransacciones por campo
        subtransactions_per_field = self._create_subtransactions_per_field(ctx)

        return subtransactions_per_field


    def _create_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(parent_record_ids: RecordIDs) -> None:
            # Inicialización de lista de IDs de registros creados
            total_created_ids: RecordIDs = []

            # Iteración por cada subtransacción
            for ( data, ) in ctx.subtransactions_data['create']:

                # Creación de registros
                created_ids = self._main.create(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    data,
                )

                # Se añaden las IDs
                total_created_ids += created_ids

            # Creación de los datos
            self._compiler.link_many2many(ctx.model_name, ctx.field_name, parent_record_ids, total_created_ids)

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _update_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(_: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for ( record_ids, data ) in ctx.subtransactions_data['update']:
                # Actualización de registros
                self._main.update(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    record_ids,
                    data,
                )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _delete_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(_: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for ( record_ids, ) in ctx.subtransactions_data['delete']:
                # Eliminación de registros
                self._main.delete(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    record_ids
                )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _add_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(parent_record_ids: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for ( record_ids, ) in ctx.subtransactions_data['add']:
                # Se vinculan las IDs
                self._compiler.link_many2many(ctx.model_name, ctx.field_name, parent_record_ids, record_ids)

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _unlink_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(parent_record_ids: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for ( record_ids, ) in ctx.subtransactions_data['unlink']:
                # Se desvinculan los registros referenciados
                self._compiler.unlink_many2many(ctx.model_name, ctx.field_name, parent_record_ids, record_ids)

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _clean_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(parent_records_ids: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for _ in ctx.subtransactions_data['clean']:
                # Se limpian todas las relaciones a los registros padres en el campo many2many
                self._compiler.delete_many2many(ctx.model_name, ctx.field_name, parent_records_ids)

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _replace_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(parent_record_ids: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for ( record_ids, ) in ctx.subtransactions_data['replace']:
                # Se limpian todas las relaciones a los registros padres en el campo many2many
                self._compiler.delete_many2many(ctx.model_name, ctx.field_name, parent_record_ids)
                # Se vinculan las IDs
                self._compiler.link_many2many(ctx.model_name, ctx.field_name, parent_record_ids, record_ids)

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _create_postcallback(
        self,
        subtransactions_per_type: Callable[[list], None],
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnUpdateCallback | Many2ManyUpdatesOnCreateCallback:
        """
        ### Creación de actualizaciones de tipos `many2many`
        Este método permite crear una función que permite realizar actualizaciones
        de datos en registros referenciados tras la ejecución principal de una
        transacción de creación o modificación de registros.

        Las funciones para cada tipo de transacción son distintas:

        #### Creación
        En método de transacción, una función se crea por cada ID de registro
        creado. La función creada mantiene el contexto del orden de las IDs por el
        tamaño de la lista de datos provista en la función principal de Lylac.
        
        La función recibe la lista de IDs completa pero solo procesa la ID a la que
        corresponde gracias a que se mantiene el índice de registro al que se
        asigna ésta.

        >>> def updates_on_create(created_ids: list[int]):
        >>>     ...

        #### Actualización
        En método de actualización, se crea una función para toda la transacción,
        que mantiene contexto de las IDs que han sido modificadas por el método
        principal de Lylac. La función no recibe ningún argumento y realiza las
        actualizaciones de valores referenciados que son un solo diccionario.

        >>> def updates_on_update():
        >>>     ...
        """

        # Si el modo de transacción es creación...
        if ctx.transaction_mode == 'create':
            # Se inicializa función que recibe lista de IDs de registros creados
            def wrapped_subtransactions_per_type(created_ids: RecordIDs):
                # Se extrae la ID del índice almacenado en el contexto
                created_id = [ created_ids[ctx.index] ]
                # Ejecución de la función con la ID correspondiente.
                subtransactions_per_type(created_id)

        # Si el modo de transacción es actualización...
        else:
            # Se inicializa función que no recibe ningún argumento
            def wrapped_subtransactions_per_type():
                # Se ejecuta función con los datos provistos a este método
                subtransactions_per_type(ctx.parent_record_ids)

        return wrapped_subtransactions_per_type

    def _create_subtransactions_per_field(
        self,
        ctx: RelationalContext,
    ) -> list[Many2ManyUpdatesOnCreateCallback] | list[Many2ManyUpdatesOnUpdateCallback]:

        # Inicialización de lista de transacciones por campo
        subtransactions_per_field: list[Many2ManyUpdatesOnCreateCallback] | list[Many2ManyUpdatesOnUpdateCallback] = []

        # Iteración por cada valor para asignar a la ejecución
        for subtransaction_command in ctx.subtransaction_commands:
            # Obtención del tipo de subtransacción
            subtransaction_type: SubtransactionName = subtransaction_command[0]
            # Obtención de los datos a usar
            subtransaction_data = subtransaction_command[1:]
            # Se asignan los datos
            ctx.subtransactions_data[subtransaction_type].append(subtransaction_data)

        # Iteración por cada tipo de transacción
        for subtransaction_name in ctx.subtransactions_data.keys():
            # Si existen datos en el tipo de transacción...
            if ctx.subtransactions_data[subtransaction_name]:
                # Obtención de la función que generará las subtransacciones por tipo
                callback = self._subtransactions_map[subtransaction_name]
                # Creación de función de subtransacciones por tipo
                subtransactions_per_type: Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback = callback(ctx)
                # Se añade la función de subtransacciones por tipo a la lista de transacciones por campo
                subtransactions_per_field.append(subtransactions_per_type)

        return subtransactions_per_field

    def _initialize_subtransactions_map(
        self,
    ) -> None:

        # Se crea el mapa de subtransacciones
        self._subtransactions_map = {
            'create': self._create_records,
            'update': self._update_records,
            'add': self._add_records,
            'unlink': self._unlink_records,
            'delete': self._delete_records,
            'clean': self._clean_records,
            'replace': self._replace_records,
        }
