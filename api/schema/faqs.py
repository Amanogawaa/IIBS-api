from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, timedelta


class FaqCreate(BaseModel):
    question: str
    answer: str
    service_id: int


class Faq(FaqCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
