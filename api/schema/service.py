from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict

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
    image_path: str
    attributes: list[AttributeCreate]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 

class ServiceCreate(ServiceBase):
    attributes: Optional[list[AttributeCreate]] = None
    
    model_config = ConfigDict(from_attributes=True)