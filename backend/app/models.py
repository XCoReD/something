from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class VoiceType(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    ROBOT = "robot"
    CHILD = "child"

class UserRole(str, enum.Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    SUPERVISOR = "supervisor"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)

class DataUnitStorage(Base):
    __tablename__ = "data_unit_storages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    voice_type = Column(Enum(VoiceType))
    start_time = Column(String)  # Format: HH:MM
    break_on_translation = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    data_units = relationship("DataUnit", back_populates="storage", 
                            cascade="all, delete-orphan")

class DataUnit(Base):
    __tablename__ = "data_units"

    id = Column(Integer, primary_key=True, index=True)
    storage_id = Column(Integer, ForeignKey("data_unit_storages.id"))
    order = Column(Integer)
    is_active = Column(Boolean, default=True)
    
    storage = relationship("DataUnitStorage", back_populates="data_units")
    content_items = relationship("ContentItem", back_populates="data_unit",
                               cascade="all, delete-orphan")

class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True, index=True)
    data_unit_id = Column(Integer, ForeignKey("data_units.id"))
    description = Column(String)
    audio_path = Column(String)
    order = Column(Integer)
    
    data_unit = relationship("DataUnit", back_populates="content_items")