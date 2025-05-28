from pydantic import BaseModel, ConfigDict, computed_field
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

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.image_path:
            base_url = "http://127.0.0.1:8000" 
            return f"{base_url}/{self.image_path}"
        return None


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