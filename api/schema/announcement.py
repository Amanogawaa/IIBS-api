from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional
from datetime import datetime

class AnnouncementLinkCreate(BaseModel):
    url: str
    title: Optional[str] = None

class AnnouncementBase(BaseModel):
    name: str
    description: str
    image_path: Optional[str] = None
    platform: str
    user_id: int

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementLinkResponse(BaseModel):
    id: int
    url: str
    title: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AnnouncementResponse(AnnouncementBase):
    id: int
    links: Optional[List[AnnouncementLinkResponse]] = None  
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)