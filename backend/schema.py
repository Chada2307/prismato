from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

class PhotoResponse(BaseModel):
    id: uuid.UUID
    captured_at: Optional[datetime]
    camera_model: Optional[str]
    thumbnail_url: str
    original_url: str
    
    class Config:
        from_attributes = True