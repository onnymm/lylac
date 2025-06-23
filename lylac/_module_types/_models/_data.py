from typing import Optional
from pydantic import BaseModel
from .._base_categories import (
    ModelName,
    TType,
)

class _BaseRecord(BaseModel):
    id: int
    """
    #### ID
    Id del registro.
    """
    name: str
    """
    #### Nombre
    Nombre del registro.
    """
    create_date: str
    """
    #### Fecha de creación
    Fecha de creación del registro.
    """
    write_date: str
    """
    #### Fecha de modificación
    Fecha de modificación del registro.
    """

class _HasLabel_Model(BaseModel):
    label: str
    """
    #### Etiqueta
    Etiqueta del registro.
    """

class ModelRecord():
    """
    #### Datos de registros
    Tipados de datos de registros de diferentes modelos.

    Los tipos disponibles son:
    - `Model`: Modelo
    - `ModelField`: Campo
    - `ModelFieldSelection`: Selección de campo
    - `User`: Usuario
    """

    class BaseModel_(
        _BaseRecord,
        _HasLabel_Model
    ):
        """
        #### Datos de modelo
        Tipado de datos de registros de modelo.
        >>> class BaseModel_(BaseModel):
        >>>     # ID
        >>>     id: int
        >>>     # Nombre
        >>>     name: str
        >>>     # Fecha de creación
        >>>     create_date: str
        >>>     # Fecha de modificación
        >>>     write_date: str
        >>>     # Etiqueta
        >>>     label: str
        >>>     # Nombre de modelo
        >>>     model: ModelName
        >>>     # Descripción
        >>>     description: str
        """
        model: ModelName
        """
        #### Nombre de modelo
        Nombre de modelo base de la base de datos.
        """
        description: str
        """
        #### Descripción
        Descripción del modelo.
        """

    class BaseModelField(
        _BaseRecord,
        _HasLabel_Model
    ):
        """
        #### Datos de campo
        Tipado de datos de registros de campo.
        >>> class BaseModelField(BaseModel):
        >>>     # ID
        >>>     id: int
        >>>     # Nombre
        >>>     name: str
        >>>     # Fecha de creación
        >>>     create_date: str
        >>>     # Fecha de modificación
        >>>     write_date: str
        >>>     # Etiqueta
        >>>     label: str
        >>>     # Tipo de dato en campo de modelo en la base de datos
        >>>     ttype: TType
        >>>     # ID de modelo
        >>>     model_id: int
        >>>     # Puede ser nulo
        >>>     nullable: bool
        >>>     # Es único
        >>>     unique: bool
        >>>     # Requerido
        >>>     is_required: bool
        >>>     # Valor predeterminado
        >>>     default_value: Optional[str]
        >>>     # Información
        >>>     help_info: str | None
        >>>     # ID de modelo relacionado
        >>>     related_model_id: int | None
        """
        ttype: TType
        """
        #### Tipo de dato en campo de modelo en la base de datos
        Tipo de dato válido en un campo de un modelo de la base de datos.
        - `'integer'`: Entero
        - `'char'`: Cadena de texto
        - `'float'`: Flotante
        - `'boolean'`: Booleano
        - `'date'`: Fecha
        - `'datetime'`: Fecha y hora
        - `'time'`: Hora
        - `'file'`: Archivo binario
        - `'text'`: Texto largo
        - `'selection'`: Selección
        - `'many2one'`: Muchos a uno
        - `'one2many'`: Uno a muchos
        - `'many2many'`: Muchos a muchos
        """
        model_id: int
        """
        #### ID de modelo
        ID del registro del modelo a relacionar.
        """
        nullable: bool
        """
        #### Puede ser nulo
        Valor booleano que indica si este campo puede iniciarse como nulo en la
        creación de un nuevo registro en el modelo relacionado.
        """
        unique: bool
        """
        #### Es único
        Valor booleano que indica que el valor de este campo en los registros no puede
        existir repetido.
        """
        is_required: bool
        """
        #### Requerido
        Indicador de si el valor del campo es requerido en la creación del campo.
        """
        default_value: Optional[str]
        """
        #### Valor predeterminado
        Valor que se usará como predeterminado en caso de no especificarse un valor
        para el campo en la creación de un nuevo registro.
        """
        help_info: str | None
        """
        #### Información
        Información de ayuda para identificar el uso o la función de este campo.
        """
        related_model_id: int | None
        """
        #### ID de modelo relacionado
        ID del modelo relacionado en caso de haberlo. Para esto, el tipo de campo debe
        ser `many2one`.
        """

    class BaseModelFieldSelection(
        _BaseRecord,
        _HasLabel_Model
    ):
        """
        #### Datos de selección de campo
        Tipado de datos de registros de modelo.
        >>> class BaseModelFieldSelection(BaseModel):
        >>>     # ID
        >>>     id: int
        >>>     # Nombre
        >>>     name: str
        >>>     # Fecha de creación
        >>>     create_date: str
        >>>     # Fecha de modificación
        >>>     write_date: str
        >>>     # Etiqueta
        >>>     label: str
        >>>     # ID de campo
        >>>     field_id: int
        """
        field_id: int
        """
        #### ID de campo
        ID del campo relacionado.
        """

    class BaseUser(_BaseRecord):
        """
        #### Datos de usuario
        Tipado de datos de registro de usuario.
        >>> class BaseUser(BaseModel):
        >>>     # ID
        >>>     id: int
        >>>     # Nombre
        >>>     name: str
        >>>     # Fecha de creación
        >>>     create_date: str
        >>>     # Fecha de modificación
        >>>     write_date: str
        >>>     # Nombre de usuario
        >>>     login: str
        >>>     # ID de Odoo
        >>>     odoo_id: int
        >>>     # Sincronizar
        >>>     sync: bool
        >>>     # Activo
        >>>     active: bool
        """
        login: str
        """
        #### Nombre de usuario
        Nombre de usuario para inicio de sesión.
        """
        odoo_id: int
        """
        #### ID de Odoo
        ID de usuario en Odoo correspondiente a este usuario.
        """
        sync: bool
        """
        #### Sincronizar
        Valor que indica si este registro se sincronizará con datos externos.
        """
        active: bool
        """
        #### Activo
        Indicador de si el usuario está activo.
        """
