from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ServiceBase(BaseModel):
    name: str
    description: str
    status: str = 'Active'
    file_path: str
    image_path: str
    user_id: int = 1
    category_id: int = 1
   
    
class AttributeCreate(BaseModel):
    attribute_name: str
    attribute_value: list | str
    attribute_type: str

    model_config = ConfigDict(from_attributes=True)

class ServiceResponse(ServiceBase):
    id: int
    attributes: list[AttributeCreate]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 

class ServiceCreate(ServiceBase):
    attributes: Optional[list[AttributeCreate]] = None
    
    model_config = ConfigDict(from_attributes=True)