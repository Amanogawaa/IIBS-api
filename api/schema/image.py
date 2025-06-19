from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, ConfigDict, EmailStr, computed_field
from datetime import datetime, timedelta

class ImageResponse(BaseModel):
    image_path: str
    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.image_path:
            base_url = "http://127.0.0.1:8000" 
            return f"{base_url}/{self.image_path}"
        return None