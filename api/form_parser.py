from fastapi import Form
from api.schema.announcement import *


async def parse_announcement_form(
   name: str = Form(...),
    description: str = Form(...),
    is_urgent: bool = Form(...),
    platform: str = Form(...),
    user_id: int = Form(...),
) -> AnnouncementCreate:
    return AnnouncementCreate(
        name=name,
        description=description,
        is_urgent=is_urgent,
        platform=platform,
        user_id=user_id,
    )