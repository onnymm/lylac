from .._constants import STATIC_FIELDS
from .._contexts import PoliciesContext
from .._resources import PolicyProperties
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R

def _reject_static_fields(ctx: PoliciesContext[_M, _R]):

    # Iteración por cada registro
    for record in ctx.records:
        # Iteración por los campos estáticos
        for static_field in STATIC_FIELDS:
            # Si existe el campo en los datos...
            if static_field in record:
                # Se captura el registro con el campo estático
                ctx.catch(record, static_field)

def _forbid_direct_password_input(ctx: PoliciesContext[_M, _R]):

    # Iteración por cada registro
    for record in ctx.records:
        # Si el campo de contraseña se encuentra en los datos...
        if 'password' in record:
            # Se captura el registro
            ctx.catch(record, show_error_data= False)

PRESET_POLICIES: list[PolicyProperties] = [

    PolicyProperties(
        ['create', 'update'],
        _reject_static_fields,
        'El campo {value} no puede ser declarado ni modificado manualmente.',
    ),

    PolicyProperties(
        ['create', 'update'],
        _forbid_direct_password_input,
        'El campo de contraseña no puede ser directamente modificado.',
        'base.users',
    ),

]
