from sqlalchemy.orm import Session
from api import models
from typing import Union, Optional
from fastapi import HTTPException, UploadFile, File, Form

from api.schema.announcement import *
from api.schema.response import ResponseModel

import os
from uuid import uuid4
import shutil

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_announcement(
    db: Session,
    name: str = Form(...),
    description: str = Form(...),
    user_id: int = Form(...),
    file: UploadFile = File(...),
):
    if db.query(models.Announcement).filter(models.Announcement.name == name).first():
        raise HTTPException(status_code=400, detail="Announcement already exists")

    image_path = None

    if file:
        file_ext = file.filename.split(".")[-1]
        unique_filename = f"{uuid4().hex}.{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    db_announcement = models.Announcement(
        name=name,
        description=description,
        user_id=user_id,
        image_path=image_path,
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)

    response_data = {
        "id": db_announcement.id,
        "name": db_announcement.name,
        "description": db_announcement.description,
        "user_id": db_announcement.user_id,
        "image_path": (
            f"/uploads/announcements/{unique_filename}" if image_path else None
        ),
        "created_at": db_announcement.created_at,
        "updated_at": db_announcement.updated_at,
    }

    return ResponseModel(
        message="Announcement Created Successfully",
        data=response_data,
        status_code=200,
    )


def get_announcements(db: Session, announcement_id: Union[int | None] = None):

    query = db.query(models.Announcement)

    if announcement_id:
        announcements = query.filter(models.Announcement.id == announcement_id).first()

    announcements = query.all()

    if not announcements:
        raise HTTPException(status_code=404, detail="Announcements not found")

    announcement_response = [
        AnnouncementResponse.model_validate(announcement)
        for announcement in announcements
    ]

    return ResponseModel(
        message="Announcements Found" if announcement_id else "All Announcements",
        data=announcement_response,
        status_code=200,
    )


def update_announcement(db: Session, announcement_id: int, req: Announcement):
    announcement = (
        db.query(models.Announcement)
        .filter(models.Announcement.id == announcement_id)
        .first()
    )

    if not announcement_id:
        raise HTTPException(status_code=404, detail="Announcement not found")

    announcement.name = req.name or announcement.name
    announcement.description = req.description or announcement.description
    announcement.user_id = req.user_id or announcement.user_id

    db.commit()
    db.refresh(announcement)

    return ResponseModel(
        message="Announcement Updated Successfully",
        status_code=200,
    )


def delete_announcement(db: Session, announcement_id: int):
    announcement = (
        db.query(models.Announcement)
        .filter(models.Announcement.id == announcement_id)
        .first()
    )

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    db.delete(announcement)
    db.commit()

    return ResponseModel(
        message="Announcement Deleted Successfully",
        status_code=200,
    )
