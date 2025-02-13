from typing import List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, timedelta

class Announcement(BaseModel):
    name: str
    description: str
    user_id: int

class AnnouncementResponse(Announcement):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)