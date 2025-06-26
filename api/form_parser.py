from fastapi import Form
from api.schema.announcement import AnnouncementCreate
from api.schema.service import ServiceCreate
from api.schema.business_info import BusinessInfoCreate

async def parse_announcement_form(
   name: str = Form(...),
    description: str = Form(...),
    platform: str = Form(...),
    user_id: int = Form(...),
) -> AnnouncementCreate:
    return AnnouncementCreate(
        name=name,
        description=description,
        platform=platform,
        user_id=user_id,
    )

async def service_form(
        name: str = Form(...),
        description: str = Form(...),
        status: str = Form(...),
        user_id: int = Form(...),
        category_id: int = Form(...)
) -> ServiceCreate:
    return ServiceCreate(
        name=name,
        description=description,
        status=status,
        user_id=user_id,
        category_id=category_id,
    )

from datetime import date
from typing import Optional
from fastapi import Form

async def business_info_form(
    name: str = Form(...),
    description: str = Form(...),
    tagline: Optional[str] = Form(None),
    user_id: int = Form(...),

    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    postal_code: Optional[str] = Form(None),
    
    industry: Optional[str] = Form(None),
    business_type: Optional[str] = Form(None),
    founded_date: Optional[date] = Form(None),
    employee_count_range: Optional[str] = Form(None),

    business_hours: Optional[str] = Form(None), 
    timezone: Optional[str] = Form(None),
    
    social_media: Optional[str] = Form(None), 
) -> BusinessInfoCreate:
    return BusinessInfoCreate(
        # Core Public Information
        name=name,
        description=description,
        tagline=tagline,
        user_id=user_id,
        
        # Contact & Location
        email=email,
        phone=phone,
        website=website,
        address=address,
        city=city,
        state=state,
        country=country,
        postal_code=postal_code,
        
        # Business Details
        industry=industry,
        business_type=business_type,
        founded_date=founded_date,
        employee_count_range=employee_count_range,
        
        # Operating Information
        business_hours=business_hours,
        timezone=timezone,
        
        # Social & Online Presence
        social_media=social_media,
    )