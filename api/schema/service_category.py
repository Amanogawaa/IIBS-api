from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, timedelta
from api.schema.requirement import *


class CategoryBase(BaseModel):
    name: str
    service_ids: List[int] = []


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    requirements: List[RequirementResponse] = []

    model_config = ConfigDict(from_attributes=True)


class CategoryCreation(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Cat_Service_Res(BaseModel):
    id: int
    name: str
    requirements: List[Req_Service_Res] = []

    model_config = ConfigDict(from_attributes=True)
