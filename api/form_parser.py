from fastapi import Form
from api.schema.announcement import AnnouncementCreate
from api.schema.service import ServiceCreate

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