from typing import Optional, Union
from pydantic import ConfigDict, BaseModel, computed_field
from datetime import datetime, date


class BusinessInfoBase(BaseModel):
    # Core Public Information
    name: str
    logo: Optional[str] = None
    description: str
    tagline: Optional[str] = None
    user_id: int
    
    # Contact & Location
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    
    # Business Details
    industry: Optional[str] = None
    business_type: Optional[str] = None
    founded_date: Optional[date] = None
    employee_count_range: Optional[str] = None
    
    # Operating Information
    business_hours: Optional[str] = None 
    timezone: Optional[str] = None
    services: Optional[str] = None 
    specialties: Optional[str] = None 
    
    # Social & Online Presence
    social_media: Optional[str] = None 
    certifications: Optional[str] = None 
    awards: Optional[str] = None 

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.logo:
            base_url = "http://127.0.0.1:8000"
            return f"{base_url}/{self.logo}"
        return None

    model_config = ConfigDict(from_attributes=True)


class BusinessInfoCreate(BusinessInfoBase):
    # attributes: Optional[list[BusinessInfoAttributesCreate]]
    pass


class BusinessInfoUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    tagline: Optional[str] = None
    
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

    industry: Optional[str] = None
    business_type: Optional[str] = None
    founded_date: Optional[date] = None
    employee_count_range: Optional[str] = None
    
    business_hours: Optional[str] = None
    timezone: Optional[str] = None
    
    social_media: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BusinessInfoResponse(BusinessInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)