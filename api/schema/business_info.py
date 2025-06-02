from typing import Optional, Union
from pydantic import ConfigDict, BaseModel, computed_field
from datetime import datetime

class BusinessInfoBase(BaseModel):
    name: str
    logo: Optional[str] = None
    description: str

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.image_path:
            base_url = "http://127.0.0.1:8000" 
            return f"{base_url}/{self.image_path}"
        return None
    
    model_config = ConfigDict(from_attributes=True) 


class BusinessInfoAttributesCreate(BaseModel):
    # business_info_id: Optional[int] = None
    attribute_name: str
    attribute_value: Union[list, str]
    attribute_type: str

    model_config = ConfigDict(from_attributes=True)

class BusinessInfoCreate(BusinessInfoBase):
    # attributes: Optional[list[BusinessInfoAttributesCreate]]
    pass

class BusinessInfoResponse(BusinessInfoBase):
    id: int
    attributes: list[BusinessInfoAttributesCreate]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


