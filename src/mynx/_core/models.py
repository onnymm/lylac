from datetime import datetime
from datetime import timedelta
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import types
from sqlalchemy import ForeignKey
from ..security import default_password
from .._typing.literals import TTypeName

class TABLE_NAME:
    BASE_MODEL_DATA = 'base_model_data'
    BASE_MODEL_DATA_PROCESS = 'base_model_data_process'
    BASE_MODEL_DATA_PROCESS_STEP = 'base_model_data_process_step'
    BASE_MODEL_DATA_PROCESS_STEP_RECORD = 'base_model_data_process_step_record'
    BASE_USERS = 'base_users'
    BASE_USER_SESSION = 'base_user_session'
    BASE_MODEL = 'base_model'
    BASE_MODEL_FIELD = 'base_model_field'
    BASE_MODEL_FIELD_SELECTION = 'base_model_field_selection'

class Feature:
    class Archivable:
        # Es activo
        active: Mapped[bool] = mapped_column(types.Boolean, default= True)

    class FactoryState:
        # Tipo de modelo
        state: Mapped[str] = mapped_column(types.String(255), nullable= False, default= 'generic')

    class LabeledModel:
        # Nombre legible del modelo
        label: Mapped[str] = mapped_column(types.String(255), nullable= False)

    class HasSequence:
        # Secuencia
        sequence: Mapped[str] = mapped_column(types.Integer, nullable= False)

class _Base(DeclarativeBase):
    ...

class ModelTemplate():
    # ID del registro
    id: Mapped[int] = mapped_column(types.Integer, primary_key= True, autoincrement= True)
    # Nombre o título representativo del registro
    name: Mapped[str] = mapped_column(types.String(120), nullable= True)
    # Fecha de creación del registro
    create_date: Mapped[datetime] = mapped_column(types.DateTime, default= datetime.now)
    # Última fecha de modificación del registro
    update_date: Mapped[datetime] = mapped_column(types.DateTime, default= datetime.now, onupdate= datetime.now)
    # Usuario de creación
    create_uid: Mapped[int] = mapped_column(ForeignKey(f'{TABLE_NAME.BASE_USERS}.id', ondelete= 'RESTRICT'), nullable= True)
    # Usuario de modificación
    update_uid: Mapped[int] = mapped_column(ForeignKey(f'{TABLE_NAME.BASE_USERS}.id', ondelete= 'RESTRICT'), nullable= True)

class Metadata:

    class BaseUsers(
        ModelTemplate,
        _Base,
        Feature.Archivable,
    ):
        __tablename__ = TABLE_NAME.BASE_USERS

        # Inicio de sesión
        login: Mapped[str] = mapped_column(types.String(255), nullable= False)
        # Contraseña
        password: Mapped[str] = mapped_column(types.String(255), nullable= False, default= default_password)
        # Foto de perfil
        profile_picture: Mapped[str] = mapped_column(types.LargeBinary, nullable= True)

    class BaseModel(
        ModelTemplate,
        _Base,
        Feature.FactoryState,
        Feature.LabeledModel,
    ):
        __tablename__ = TABLE_NAME.BASE_MODEL

        # Nombre representativo para usarse en el servidor
        model: Mapped[str] = mapped_column(types.String(255), nullable= False, unique= True)
        # Descripción del modelo
        description: Mapped[str] = mapped_column(types.Text, nullable= True)
        # Tiene secuencia
        has_sequence: Mapped[bool] = mapped_column(types.Boolean, default= False)
        # Es archivable
        is_archivable: Mapped[bool] = mapped_column(types.Boolean, default= False)
        # Es archivable
        has_label: Mapped[bool] = mapped_column(types.Boolean, default= False)
        # Es modelo transitorio
        transient: Mapped[bool] = mapped_column(types.Boolean, default= False)

    class BaseModelData(
        ModelTemplate,
        _Base,
    ):
        __tablename__ = TABLE_NAME.BASE_MODEL_DATA

        # Nombre del modelo al que pertenece
        model_name: Mapped[str] = mapped_column(types.String(255), nullable= False)
        # ID de recurso
        res_id: Mapped[int] = mapped_column(types.Integer, nullable= True)

    class BaseModelDataProcess(
        ModelTemplate,
        _Base,
    ):
        __tablename__ = TABLE_NAME.BASE_MODEL_DATA_PROCESS

    class BaseModelDataProcessStep(
        ModelTemplate,
        _Base,
        Feature.HasSequence,
    ):
        __tablename__ = TABLE_NAME.BASE_MODEL_DATA_PROCESS_STEP

        # Proceso
        process_id: Mapped[int] = mapped_column(ForeignKey(f'{TABLE_NAME.BASE_MODEL_DATA_PROCESS}.id', ondelete= 'CASCADE'))
        # Nombre del modelo al que pertenece
        model_name: Mapped[str] = mapped_column(types.String(255), nullable= False)

    class BaseModelDataProcessStepRecord(
        ModelTemplate,
        _Base,
        Feature.HasSequence,
    ):
        __tablename__ = TABLE_NAME.BASE_MODEL_DATA_PROCESS_STEP_RECORD

        # Paso de proceso
        step_id: Mapped[int] = mapped_column(ForeignKey(f'{TABLE_NAME.BASE_MODEL_DATA_PROCESS_STEP}.id', ondelete= 'CASCADE'))
        # Datos a crear
        data: Mapped[dict | list] = mapped_column(JSONB, nullable= False)

    class BaseModelField(
        ModelTemplate,
        _Base,
        Feature.FactoryState,
        Feature.LabeledModel,
    ):
        __tablename__ = TABLE_NAME.BASE_MODEL_FIELD

        # ID del modelo al que pertenece
        model_id: Mapped[int] = mapped_column(ForeignKey(f'{TABLE_NAME.BASE_MODEL}.id', ondelete= 'CASCADE'), nullable= False)
        # Tipo de dato del campo
        ttype: Mapped[TTypeName] = mapped_column(types.String(255), nullable= False)
        # El valor del campo puede ser nulo
        nullable: Mapped[bool] = mapped_column(types.Boolean, default= True)
        # En eliminación...
        on_delete: Mapped[str] = mapped_column(types.String(20), nullable= True)
        # Es requerido
        is_required: Mapped[str] = mapped_column(types.Boolean, default= False)
        # Solo lectura
        readonly: Mapped[bool] = mapped_column(types.Boolean, default= False)
        # Valor inicial
        default_value: Mapped[dict] = mapped_column(types.JSON, nullable= True)
        # El valor del campo debe ser único en toda la tabla
        unique: Mapped[bool] = mapped_column(types.Boolean, default= False)
        # Información de ayuda
        help_info: Mapped[str] = mapped_column(types.Text, nullable= True)
        # Modelo de relación
        related_model_id: Mapped[int] = mapped_column(ForeignKey(f'{TABLE_NAME.BASE_MODEL}.id', ondelete= 'RESTRICT'), nullable= True)
        # Campo de relación
        related_field: Mapped[str] = mapped_column(types.String(255), nullable= True)
        # Modelo computado
        is_computed: Mapped[bool] = mapped_column(types.Boolean, nullable= False, default= False)

    class BaseModelFieldSelection(
        ModelTemplate,
        _Base,
        Feature.LabeledModel,
    ):
        __tablename__ = TABLE_NAME.BASE_MODEL_FIELD_SELECTION

        # ID del campo al que pertenece
        field_id: Mapped[int] = mapped_column(ForeignKey(f'{TABLE_NAME.BASE_MODEL_FIELD}.id', ondelete= 'CASCADE'), nullable= False)

    class BaseUserSession(
        ModelTemplate,
        _Base,
    ):
        __tablename__ = TABLE_NAME.BASE_USER_SESSION
        # Usuario
        user_id: Mapped[int] = mapped_column(ForeignKey(f'{TABLE_NAME.BASE_USERS}.id', ondelete= 'CASCADE'))
        # Tiempo de expiración
        validity_time: Mapped[timedelta] = mapped_column(types.Interval)
