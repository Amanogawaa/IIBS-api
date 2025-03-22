from pydantic import ConfigDict, BaseModel
from datetime import datetime

class BusinessInfoBase(BaseModel):
    name: str
    logo: str
    description: str

class BusinessInfoCreate(BusinessInfoBase):
    pass

class BusinessInfoResponse(BusinessInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

