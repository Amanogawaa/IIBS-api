from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, computed_field

class ServiceBase(BaseModel):
    name: str
    description: str
    status: str = 'Active'
    user_id: int
    category_id: int
   
    
class AttributeCreate(BaseModel):
    attribute_name: str
    attribute_value: Union[list, str]
    attribute_type: str

    model_config = ConfigDict(from_attributes=True)

class ServiceResponse(ServiceBase):
    id: int
    image_path: Optional[str] = None
    attributes: list[AttributeCreate]
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.image_path:
            base_url = "http://127.0.0.1:8000"  # Update for production
            return f"{base_url}/{self.image_path}"
        return None

    model_config = ConfigDict(from_attributes=True) 

class ServiceCreate(ServiceBase):
    attributes: Optional[list[AttributeCreate]] = None
    
    model_config = ConfigDict(from_attributes=True)