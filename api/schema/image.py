from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, ConfigDict, EmailStr, computed_field
from datetime import datetime, timedelta

class ImageResponse(BaseModel):
    image_path: str
    name: str
    size: int
    type: str    

    @computed_field
    @property
    def url(self) -> Optional[str]:
        if self.image_path:
            base_url = "http://127.0.0.1:8000" 
            return f"{base_url}/{self.image_path}"
        return None

class VideoResponse(BaseModel):
    video_path: str
    name: str
    size: int
    type: str

    @computed_field
    @property
    def url(self) -> Optional[str]:
        if self.video_path:
            base_url = "http://127.0.0.1:8000" 
            return f"{base_url}/{self.video_path}"
        return None