from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name:str
    description: str
    status: str = 'active'

class CreateCategory(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)