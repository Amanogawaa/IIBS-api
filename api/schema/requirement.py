from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, timedelta


class RequirementBase(BaseModel):
    name: str
    description: str
    category_ids: List[int] = []


class RequirementResponse(RequirementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Req_Service_Res(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
