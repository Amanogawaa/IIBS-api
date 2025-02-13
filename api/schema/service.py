from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, timedelta
from api.schema.requirement import *
from api.schema.service_category import *


class ServiceBase(BaseModel):
    name: str
    description: str


class ServiceCreate(ServiceBase):
    user_id: int
    pass


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    categories: List[Cat_Service_Res]

    model_config = ConfigDict(from_attributes=True)
