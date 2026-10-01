from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class PhotoResponse(BaseModel):
    id: uuid.UUID
    captured_at: Optional[datetime]
    camera_model: Optional[str]
    thumbnail_url: str
    original_url: str
    is_favorite: bool
    
    class Config:
        from_attributes = True


class AlbumCreate(BaseModel):
    title: str = Field(..., min_lenght=1, max_lenght=100, description="Nazwa albumu")

class AlbumResponse(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime
    photo_count: Optional[int] = -0
    
    class Config:
        from_attributes = True

class AlbumAddPhotos(BaseModel):
    photos_ids: List[uuid.UUID]