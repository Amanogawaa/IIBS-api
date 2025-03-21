from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ServiceBase(BaseModel):
    name: str
    description: str
    status: str = 'Active'
    file_path: str
    image_path: str
    user_id: int = 1
    category_id: int = 1

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 