from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, timedelta


class Feedback(BaseModel):
    rating: int
    comment: str


class FeedbackResponse(Feedback):
    id: int
    service_id:  Optional[int] = None
    announcement_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
