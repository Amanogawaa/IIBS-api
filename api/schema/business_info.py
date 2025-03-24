from typing import Optional, Union
from pydantic import ConfigDict, BaseModel
from datetime import datetime

class BusinessInfoBase(BaseModel):
    name: str
    logo: str
    description: str

class BusinessInfoAttributesCreate(BaseModel):
    # business_info_id: Optional[int] = None
    attribute_name: str
    attribute_value: Union[list, str]
    attribute_type: str

    model_config = ConfigDict(from_attributes=True)

class BusinessInfoCreate(BusinessInfoBase):
    attributes: Optional[list[BusinessInfoAttributesCreate]]
    pass

class BusinessInfoResponse(BusinessInfoBase):
    id: int
    attributes: list[BusinessInfoAttributesCreate]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


