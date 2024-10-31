from pydantic import BaseModel
from typing import List, Optional
from .models import VoiceType, UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None

class UserBase(BaseModel):
    username: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class ContentItemBase(BaseModel):
    description: str
    order: int

class ContentItemCreate(ContentItemBase):
    pass

class ContentItem(ContentItemBase):
    id: int
    audio_path: Optional[str]
    data_unit_id: int

    class Config:
        from_attributes = True

class DataUnitBase(BaseModel):
    order: int
    is_active: bool = True

class DataUnitCreate(DataUnitBase):
    content_items: List[ContentItemCreate]

class DataUnit(DataUnitBase):
    id: int
    storage_id: int
    content_items: List[ContentItem]

    class Config:
        from_attributes = True

class DataUnitStorageBase(BaseModel):
    name: str
    voice_type: VoiceType
    start_time: str
    break_on_translation: bool = False
    is_active: bool = True

class DataUnitStorageCreate(DataUnitStorageBase):
    pass

class DataUnitStorage(DataUnitStorageBase):
    id: int
    data_units: List[DataUnit]

    class Config:
        from_attributes = True