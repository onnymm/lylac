from typing import Generic
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy import func
from .._constants import FIELD_NAME
from .._constants import MODEL_NAME
from .._contexts import ExpansionContext
from .._contexts import RelationOperationsContext
from .._operations import DQL
from .._operations import DML
from .._resources import InputProcessing
from .._resources import ModelsBearer
from .._typing.generics import ItemOrList
from .._typing.generics import ModelName
from .._typing.generics import _Record
from .._typing.literals import CRUDPermission
from .._typing.literals import CRUDPermissionColumnName
from .._typing.structures import CriteriaStructure
from .._typing.structures import RecordData
from .._typing.structures import FieldReadDeclaration
from .._typing.type_parameters import _M
from .._utils import to_list
from .._utils import parse_record_rule
from ..errors import PermissionDeniedError
from ..errors import RecordRulesPermissionError

if TYPE_CHECKING:
    from .._contexts import ExecutionContext

class CRUD(Generic[_M]):
    PERMISSIONS_BYPASS: bool = True
    _adapter: dict[CRUDPermission, CRUDPermissionColumnName] = {
        'create': 'perm_create',
        'read': 'perm_read',
        'update': 'perm_update',
        'delete': 'perm_delete',
    }

    def _check_access(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        permission: CRUDPermission = None,
    ) -> None:

        # Si el bypass de revisión de permisos está activado...
        if self.PERMISSIONS_BYPASS:
            # Se termina la ejecución
            return

        # Obtención del modelo de usuarios
        base_users = self._models_bearer.get_model(MODEL_NAME.BASE_USERS)
        # Obtención del modelo de roles de usuario
        base_users_role = self._models_bearer.get_model(MODEL_NAME.BASE_USERS_ROLE)
        # Obtención del modelo de grupos de acceso
        base_user_groups = self._models_bearer.get_model(MODEL_NAME.BASE_USER_GROUPS)
        # Obtención del modelo de permisos de acceso
        base_user_access = self._models_bearer.get_model(MODEL_NAME.BASE_USER_ACCESS)
        # Obtención del modelo de modelos
        base_model = self._models_bearer.get_model(MODEL_NAME.BASE_MODEL)

        # Obtención de intermedio entre usuarios y roles
        m2m_base_users__role_ids = self._models_bearer.get_m2m_model(MODEL_NAME.BASE_USERS, 'role_ids')
        # Obtención de intermedio entre roles y grupos
        m2m_base_users_role__group_ids = self._models_bearer.get_m2m_model(MODEL_NAME.BASE_USERS_ROLE, 'group_ids')

        # Columna a buscar
        permission_column = self._adapter[permission]

        # Obtención de instancias de ID
        base_users__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USERS, FIELD_NAME.ID)
        base_users_role__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USERS_ROLE, FIELD_NAME.ID)
        base_user_groups__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USER_GROUPS, FIELD_NAME.ID)
        base_model__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_MODEL, FIELD_NAME.ID)

        # Obtención de instancia de ID de grupo
        base_user_access__group_id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USER_ACCESS, 'group_id')
        # Obtención de instancia de modelo vinculado
        base_user_access__model_id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USER_ACCESS, 'model_id')
        # Obtención de instancia de nombre de modelo
        base_model__model = self._models_bearer.get_field_instance(MODEL_NAME.BASE_MODEL, 'model')

        # Obtención de instancia de permiso
        permission_instance = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USER_ACCESS, permission_column)

        # Construcción de query
        stmt = (
            # Conteo de resultados
            select( func.count('*') )
            # Desde la tabla de usuarios
            .select_from(base_users)

            # Unión de tablas
            .outerjoin(
                m2m_base_users__role_ids,
                base_users__id == m2m_base_users__role_ids.x,
            )
            .outerjoin(
                base_users_role,
                m2m_base_users__role_ids.y == base_users_role__id,
            )
            .outerjoin(
                m2m_base_users_role__group_ids,
                base_users_role__id == m2m_base_users_role__group_ids.x,
            )
            .outerjoin(
                base_user_groups,
                m2m_base_users_role__group_ids.y == base_user_groups__id,
            )
            .outerjoin(
                base_user_access,
                base_user_groups__id == base_user_access__group_id,
            )
            .outerjoin(
                base_model,
                base_user_access__model_id == base_model__id
            )

            # Donde...
            .where(
                # La ID de usuario sea igual a la proporcionada
                base_users__id == execution_ctx.uid,
                # El tipo de permiso esté concedido
                permission_instance == True,
                # El nombre de modelo sea igual al proporcionado
                base_model__model == model_name,
            )
        )

        # Obtención de conteo de permisos concedidos para el usuario
        count: int = (
            execution_ctx.conn
            .execute(stmt)
            .scalar()
        )

        # Evaluación de si el usuario tiene permiso para realizar la acción
        user_has_permission = (
            # El conteo es mayor a cero
            count > 0
            # El bypass está activado
            or self.PERMISSIONS_BYPASS
        )

        # Si el usuario no tiene permiso para la realizar la acción...
        if not user_has_permission:
            # Se arroja error de permiso denegado
            raise PermissionDeniedError(f'El usuario con la ID {execution_ctx.uid} no tiene permisos para realizar la acción en el modelo [{model_name}].')

    def __init__(
        self,
        models_bearer: ModelsBearer[_M],
    ) -> None:

        self._models_bearer = models_bearer
        self._dml = DML()
        self._dql = DQL()
        self._input_processing = InputProcessing()

    def create(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        data: ItemOrList[RecordData],
    ) -> list[int]:

        # Revisión de permisos
        self._check_access(
            execution_ctx,
            model_name,
            'create',
        )

        # Se asegura una lista de datos
        data = self._input_processing.to_list(data)

        # Validación de los datos
        execution_ctx.validations.validate(
            'create',
            execution_ctx,
            model_name,
            data,
        )

        # Procesamiento de los datos
        processed_data = self._add_create_and_update_uid(data, execution_ctx)

        # Creación de contexto de operaciones de relación
        rel_op_ctx = RelationOperationsContext(execution_ctx, model_name, self._models_bearer)

        # Creación de registros y obtención de las IDs creadas
        created_ids = self._dml.create(rel_op_ctx, execution_ctx, model_name, processed_data)

        # Ejecución de las automatizaciones después de la ejecución principal
        execution_ctx.automations.execute_on_create(
            execution_ctx,
            model_name,
            created_ids,
        )

        # Ejecución de operaciones de relación
        rel_op_ctx.run_relation_operations(self)

        # Se eliminan los registros si el modelo es transitorio
        self._destroy_if_transient(
            execution_ctx,
            model_name,
            created_ids,
        )

        return created_ids

    def search(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[int]:

        # Revisión de permisos
        self._check_access(
            execution_ctx,
            model_name,
            'read',
        )

        # Obtención de criterio de búsqueda con alcance del usuario
        scoped_search_criteria = self._get_record_rules(
            execution_ctx,
            'read',
            model_name,
            search_criteria,
        )

        # Obtención de los registros del usuario
        record_ids = self._dql.search(
            execution_ctx,
            model_name,
            scoped_search_criteria,
            offset,
            limit,
        )

        return record_ids

    def search_read(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        fields: list[FieldReadDeclaration] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None,
    ) -> list[_Record]:

        # Revisión de permisos
        self._check_access(
            execution_ctx,
            model_name,
            'read',
        )

        # Inicialización de contexto de expansión
        expansion_ctx = ExpansionContext(execution_ctx, self)

        # Obtención de criterio de búsqueda con alcance del usuario
        scoped_search_criteria = self._get_record_rules(
            execution_ctx,
            'read',
            model_name,
            search_criteria,
        )

        # Normalización de campos
        normalized_fields = expansion_ctx.intercept(fields)

        data = self._dql.search_read(
            execution_ctx,
            model_name,
            scoped_search_criteria,
            normalized_fields,
            offset,
            limit,
            sortby,
            ascending,
        )

        # Expansión de datos en caso de haberse especificado
        expanded_data = expansion_ctx.resolve(
            model_name,
            data,
        )

        return expanded_data

    def search_count(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
    ) -> int:

        # Revisión de permisos
        self._check_access(
            execution_ctx,
            model_name,
            'read',
        )

        # Obtención de criterio de búsqueda con alcance del usuario
        scoped_search_criteria = self._get_record_rules(
            execution_ctx,
            'read',
            model_name,
            search_criteria,
        )

        # Obtención del conteo de resultados
        count = self._dql.search_count(
            execution_ctx,
            model_name,
            scoped_search_criteria,
        )

        return count

    def read(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        fields: list[FieldReadDeclaration] = [],
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None
    ) -> list[_Record]:

        # Revisión de permisos
        self._check_access(
            execution_ctx,
            model_name,
            'read',
        )

        # Inicialización de contexto de expansión
        expansion_ctx = ExpansionContext(execution_ctx, self)

        # Se asegura una lista de datos
        record_ids = self._input_processing.to_list(record_ids)

        # Evaluación de IDs permitidas
        self._evalute_allowed_ids(
            execution_ctx,
            'read',
            model_name,
            record_ids,
        )

        # Normalización de campos
        normalized_fields = expansion_ctx.intercept(fields)

        # Obtención de los datos
        data = self._dql.read(
            execution_ctx,
            model_name,
            record_ids,
            normalized_fields,
            sortby,
            ascending,
        )

        # Expansión de datos en caso de haberse especificado
        expanded_data = expansion_ctx.resolve(
            model_name,
            data,
        )

        return expanded_data

    def update(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        data: RecordData,
    ) -> Literal[True]:

        # Revisión de permisos
        self._check_access(
            execution_ctx,
            model_name,
            'update',
        )

        # Se asegura una lista de datos
        record_ids = to_list(record_ids)

        # Evaluación de IDs permitidas
        self._evalute_allowed_ids(
            execution_ctx,
            'update',
            model_name,
            record_ids,
        )

        # Validación de los datos
        execution_ctx.validations.validate(
            'update',
            execution_ctx,
            model_name,
            [data],
        )

        # Procesamiento de los datos
        processed_data = self._add_update_uid(data, execution_ctx)

        # Creación de contexto de operaciones de relación
        rel_op_ctx = RelationOperationsContext(execution_ctx, model_name, self._models_bearer)

        # Actualización de datos
        updated_ids = self._dml.update(
            rel_op_ctx,
            execution_ctx,
            model_name,
            record_ids,
            processed_data,
        )

        # Ejecución de automatizaciones
        execution_ctx.automations.execute_on_update(execution_ctx, model_name, updated_ids)

        # Ejecución de acciones de relación
        rel_op_ctx.run_relation_operations(self)

        return True

    def delete(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
    ) -> Literal[True]:

        # Revisión de permisos
        self._check_access(
            execution_ctx,
            model_name,
            'delete',
        )

        # Se asegura una lista de datos
        record_ids = to_list(record_ids)

        # Evaluación de IDs permitidas
        self._evalute_allowed_ids(
            execution_ctx,
            'delete',
            model_name,
            record_ids,
        )

        # Inicialización de función para ejecución de automatizaciones tras eliminación de registros
        execute_automations_on_delete = execution_ctx.automations.prepare_on_delete(
            execution_ctx,
            model_name,
            record_ids,
        )

        # Eliminación de registros
        self._dml.delete(
            execution_ctx,
            model_name,
            record_ids,
        )

        # Ejecución de automatizaciones
        execute_automations_on_delete()

        return True

    def _evalute_allowed_ids(
        self,
        execution_ctx: ExecutionContext[_M],
        permission: CRUDPermission,
        model_name: ModelName[_M],
        declared_record_ids: list[int],
    ) -> None:

        # Obtención de criterio de búsqueda con alcance del usuario
        scoped_search_criteria = self._get_record_rules(
            execution_ctx,
            'read',
            model_name,
            [(FIELD_NAME.ID, 'in', declared_record_ids)]
        )

        # Obtención de las IDs que el usuario puede leer
        allowed_ids =  self._dql.search(
            execution_ctx,
            model_name,
            scoped_search_criteria,
        )

        # Obtención de IDs prohibidas
        forbidden_ids = set(declared_record_ids) - set(allowed_ids)

        # Si se encontraron IDs restringidas dentro de las IDs provistas...
        if len(forbidden_ids):
            # Se arroja error
            raise RecordRulesPermissionError(f'No puedes realizar la acción [{permission}] los registros {list(forbidden_ids)} del modelo [{model_name}]')

    def _get_record_rules(
        self,
        execution_ctx: ExecutionContext[_M],
        permission: CRUDPermission,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
    ) -> CriteriaStructure:

        # Si el bypass de revisión de permisos está activado...
        if self.PERMISSIONS_BYPASS:
            # Se termina la ejecución
            return search_criteria

        # Obtención de modelo de roles de usuario
        base_users = self._models_bearer.get_model(MODEL_NAME.BASE_USERS)
        # Obtención de modelo de roles de usuario
        base_users_role = self._models_bearer.get_model(MODEL_NAME.BASE_USERS_ROLE)
        # Obtención de modelo de grupos de acceso
        base_user_groups = self._models_bearer.get_model(MODEL_NAME.BASE_USER_GROUPS)
        # Obtención de modelo de reglas de registro
        base_rules = self._models_bearer.get_model(MODEL_NAME.BASE_RULES)
        # Obtención de modelo de modelos
        base_model = self._models_bearer.get_model(MODEL_NAME.BASE_MODEL)

        # Obtención de relación de roles a grupos
        m2m_base_users_role__base_user_groups = self._models_bearer.get_m2m_model(MODEL_NAME.BASE_USERS_ROLE, 'group_ids')
        # Obtención de relación de grupos a reglas de registro
        m2m_base_user_groups__base_rules = self._models_bearer.get_m2m_model(MODEL_NAME.BASE_USER_GROUPS, 'rule_ids')
        # Obtención de relación de usuarios a roles
        m2m_base_users__base_users_role = self._models_bearer.get_m2m_model(MODEL_NAME.BASE_USERS, 'role_ids')

        # Obtención de instancia de ID de usuario
        base_users__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USERS, FIELD_NAME.ID)
        # Obtención de instancia de ID de rol
        base_users_role__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USERS_ROLE, FIELD_NAME.ID)
        # Obtención de instancia de ID de grupo
        base_user_groups__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_USER_GROUPS, FIELD_NAME.ID)
        # Obtención de instancia de ID de regla de registro
        base_rules__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_RULES, FIELD_NAME.ID)
        # Obtención de instancia de ID de modelo
        base_model__id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_MODEL, FIELD_NAME.ID)
        # Obtención de instancia de modelo vinculado de regla de registro
        base_rules__model_id = self._models_bearer.get_field_instance(MODEL_NAME.BASE_RULES, 'model_id')
        # Obtención de instancia de nombre de modelo de modelo
        base_model__model = self._models_bearer.get_field_instance(MODEL_NAME.BASE_MODEL, 'model')

        # Obtención de instancia de dominio de reglas de registro
        base_rules__domain = self._models_bearer.get_field_instance(MODEL_NAME.BASE_RULES, 'domain')

        # Columna a buscar
        permission_column = self._adapter[permission]
        # Obtención de instancia de permiso
        permission_instance = self._models_bearer.get_field_instance(MODEL_NAME.BASE_RULES, permission_column)

        stmt = (
            select(
                func.array_agg(base_rules__domain),
            )
            .select_from(base_users)
            .outerjoin(
                m2m_base_users__base_users_role,
                base_users__id == m2m_base_users__base_users_role.x
            )
            .outerjoin(
                base_users_role,
                m2m_base_users__base_users_role.y == base_users_role__id
            )
            .outerjoin(
                m2m_base_users_role__base_user_groups,
                base_users_role__id == m2m_base_users_role__base_user_groups.x,
            )
            .outerjoin(
                base_user_groups,
                m2m_base_users_role__base_user_groups.y == base_user_groups__id,
            )
            .outerjoin(
                m2m_base_user_groups__base_rules,
                base_user_groups__id == m2m_base_user_groups__base_rules.x,
            )
            .outerjoin(
                base_rules,
                m2m_base_user_groups__base_rules.y == base_rules__id,
            )
            .outerjoin(
                base_model,
                base_rules__model_id == base_model__id,
            )
            .where(
                base_users__id == execution_ctx.uid,
                permission_instance == True,
                base_model__model == model_name,
            )
            .group_by(base_users__id)
        )

        # Obtención de reglas de registro para el usuario en la transacción
        found_records = (
            execution_ctx.conn
            .execute(stmt)
            .fetchall()
        )

        # Si fueron encontrados registros...
        if found_records:
            # Destructuración del valor de lista de reglas de registro sin compilar
            [ ( string_record_rules, ) ] = found_records

            # Compilación de las reglas de registro
            compiled_record_rules = [
                parse_record_rule(execution_ctx, str_rec_rule)
                for str_rec_rule
                in string_record_rules
            ]

            # Si hay más de una regla de registro...
            if len(compiled_record_rules) > 1:
                # Inicialización de lista de reglas de registro unificadas con el primer elemento destructurado
                unified_record_rules = [*compiled_record_rules[0]]
                # Iteración por el resto de reglas de registro
                for comp_rec_rule in compiled_record_rules[1:]:
                    # Se unen las reglas por operador [OR]
                    unified_record_rules = ['|', *unified_record_rules, *comp_rec_rule]

                # Reasignación de reglas de registro unificadas a reglas de registro compiladas
                compiled_record_rules = unified_record_rules

            # Si no hay más de una regla de registro...
            else:
                # Destructuración y reasignación del único elemento de reglas de registro compiladas
                [ compiled_record_rules ] = compiled_record_rules

        # Si no fueron encontrados registros...
        else:
            # Asignación de una lista vacía a la variable de reglas de registro compiladas
            compiled_record_rules = []

        # Si hay un criterio de búsqueda a usar...
        if search_criteria:
            # Si existen reglas de registro compiladas...
            if compiled_record_rules:
                # Unión de criterio de búsqueda con reglas de registro compiladas
                search_criteria = ['&', *search_criteria, *compiled_record_rules]

        # SI no hay un criterio de búsqueda a usar...
        else:
            # Si existen reglas de registro compiladas...
            if compiled_record_rules:
                # Reasignación de variable
                search_criteria = compiled_record_rules

        return search_criteria

    def _add_create_and_update_uid(
        self,
        data: list[dict],
        execution_ctx: ExecutionContext[_M],
    ) -> list[dict]:

        # Iteración por cada registro en los datos
        for record in data:
            # Se coloca la ID de usuario del contexto de ejecución
            record[FIELD_NAME.CREATE_UID] = execution_ctx.uid
            record[FIELD_NAME.UPDATE_UID] = execution_ctx.uid

        return data

    def _add_update_uid(
        self,
        data: RecordData,
        execution_ctx: ExecutionContext[_M],
    ) -> RecordData:

        # Se coloca la ID de usuario del contexto de ejecución
        data[FIELD_NAME.UPDATE_UID] = execution_ctx.uid

        return data

    def _destroy_if_transient(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        created_ids: list[int],
    ) -> None:

        # Lectura del registro del modelo
        [ model_record ] = self._dql.search_read(
            execution_ctx,
            'base.model',
            [('model', '=', model_name)],
            ['transient'],
        )

        # Obtención del valor de transitorio
        transient = model_record['transient']

        # Si el modelo es transitorio...
        if transient:
            # Se eliminan los registros
            self._dml.delete(
                execution_ctx,
                model_name,
                created_ids,
            )
