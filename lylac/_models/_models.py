from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)
from ..security import default_password

class ___Base(DeclarativeBase):
    # ID del registro
    id: Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement= True)
    # Nombre o título representativo del registro
    name: Mapped[str] = mapped_column(String(60), nullable= False)
    # Fecha de creación del registro
    create_date: Mapped[datetime] = mapped_column(DateTime, default= datetime.now)
    # Última fecha de modificación del registro
    write_date: Mapped[datetime] = mapped_column(DateTime, default= datetime.now, onupdate= datetime.now)



class ___BaseUsers(___Base):
    __tablename__ = 'base_users'

    # Inicio de sesión
    login: Mapped[str] = mapped_column(String(60), nullable= False)
    # Contraseña
    password: Mapped[str] = mapped_column(String(255), default= default_password)
    # ID de Odoo
    odoo_id: Mapped[int] = mapped_column(Integer, nullable= True)
    # Es activo
    active: Mapped[bool] = mapped_column(Boolean, default= True)
    # Sincronizar
    sync: Mapped[bool] = mapped_column(Boolean, default= True)



class __BaseModel_(___Base):
    __tablename__ = 'base_model'

    # Nombre representativo para usarse en el servidor
    model: Mapped[str] = mapped_column(String(60), nullable= False)
    # Etiqueta del modelo
    label: Mapped[str] = mapped_column(String(60), nullable= False)
    # Descripción del propósito del modelo
    description: Mapped[str] = mapped_column(Text, nullable= True)



class __BaseModelField(___Base):
    __tablename__ = 'base_model_field'

    # ID del modelo al que pertenece
    model_id: Mapped[int] = mapped_column(ForeignKey("base_model.id"), nullable= False)
    # Etiqueta del campo
    label: Mapped[str] = mapped_column(String(60), nullable= False)
    # Tipo de dato del campo
    ttype: Mapped[str] = mapped_column(String(60), nullable= False)
    # El valor del campo puede ser nulo
    nullable: Mapped[bool] = mapped_column(Boolean, default= True)
    # Es requerido
    is_required: Mapped[bool] = mapped_column(Boolean, default= False)
    # Valor inicial
    default_value: Mapped[Optional[str]] = mapped_column(String(255), nullable= True)
    # El valor del campo debe ser único en toda la tabla
    unique: Mapped[bool] = mapped_column(Boolean, default= False)
    # Información de ayuda
    help_info: Mapped[str] = mapped_column(Text, nullable= True)
    # Modelo de relación
    related_model_id: Mapped[Optional[int]] = mapped_column(ForeignKey('base_model.id'), nullable= True)

    # Relación con valores de selección (Solo si el tipo de dato del campo es `selection`)
    selection_ids: Mapped[Optional[List["__BaseModelFieldSelection"]]] = relationship(back_populates= 'field', cascade= 'all, delete-orphan')
    # Relación hacia el modelo al que pertenece
    model: Mapped["__BaseModel_"] = relationship(__BaseModel_, foreign_keys= [model_id])
    # Relación hacia el modelo relacionado (opcional, si es many2one)
    related_model: Mapped[Optional["__BaseModel_"]] = relationship(
        __BaseModel_,
        foreign_keys=[related_model_id],
    )



class __BaseModelFieldSelection(___Base):
    __tablename__ = 'base_model_field_selection'

    # ID del campo al que pertenece
    field_id: Mapped[int] = mapped_column(ForeignKey('base_model_field.id'), nullable= False)
    # Etiqueta del valor de selección
    label: Mapped[str] = mapped_column(String(60), nullable= False)

    # Relación al campo al que pertenece
    field: Mapped["__BaseModelField"] = relationship(back_populates= 'selection_ids')
