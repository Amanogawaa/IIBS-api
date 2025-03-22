from sqlalchemy.orm import Session
from api import models
from fastapi import HTTPException, UploadFile, File, Form, Depends
from typing import Optional
import os
from uuid import uuid4
import shutil
from datetime import datetime

from api.schema.announcement import *
from api.schema.response import ResponseModel

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_announcement(
    db: Session,
    announcement_data: AnnouncementCreate,
    links: Optional[List[AnnouncementLinkCreate]],
    file: Optional[UploadFile] = None,
) -> ResponseModel:
    if db.query(models.Announcement).filter(models.Announcement.name == announcement_data.name).first():
        raise HTTPException(status_code=400, detail="Announcement already exists")

    image_path = None
    if file:
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type")
        unique_filename = f"{uuid4().hex}.{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    db_announcement = models.Announcement(
        name=announcement_data.name,
        description=announcement_data.description,
        image=image_path,
        is_urgent=announcement_data.is_urgent,
        platform=announcement_data.platform,
        user_id=announcement_data.user_id,
    )

    db_links = None
    if links:
        db_links = [
            models.AnnouncementLink(url=link.url, title=link.title, announcement=db_announcement)
            for link in links
        ]
        db.add_all(db_links)

    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)

    response_links = [
        AnnouncementLinkResponse(id=link.id, url=link.url, title=link.title)
        for link in db_announcement.links 
    ] if db_announcement.links else None

    response_data = AnnouncementResponse(
        id=db_announcement.id,
        name=db_announcement.name,
        description=db_announcement.description,
        image=db_announcement.image,
        is_urgent=db_announcement.is_urgent,
        platform=db_announcement.platform,
        links=response_links,
        user_id=db_announcement.user_id,
        created_at=db_announcement.created_at,
        updated_at=db_announcement.updated_at,
    )

    return ResponseModel(
        message="Announcement Created Successfully",
        data=response_data,
        status_code=201,
    )

def get_announcements(db: Session, announcement_id: Optional[int | None] = None):

    query = db.query(models.Announcement)

    if announcement_id:
        query = query.filter(models.Announcement.id == announcement_id)

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

def update_announcement(
    db: Session,
    announcement_id: int,
    announcement_data: AnnouncementCreate,
    links: Optional[List[AnnouncementLinkCreate]],
    file: Optional[UploadFile] = None,
) -> ResponseModel:
    db_announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    image_path = db_announcement.image
    if file:
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type")
        unique_filename = f"{uuid4().hex}.{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        if db_announcement.image and os.path.exists(db_announcement.image):
            os.remove(db_announcement.image)

    db_announcement.name = announcement_data.name
    db_announcement.description = announcement_data.description
    db_announcement.image = image_path
    db_announcement.is_urgent = announcement_data.is_urgent
    db_announcement.platform = announcement_data.platform
    db_announcement.user_id = announcement_data.user_id

    if links is not None:  
        db.query(models.AnnouncementLink).filter(models.AnnouncementLink.announcement_id == announcement_id).delete()
        if links:
            db_links = [
                models.AnnouncementLink(
                    url=link.url,
                    title=link.title,
                    announcement_id=announcement_id
                )
                for link in links
            ]
            db.add_all(db_links)

    db.commit()
    db.refresh(db_announcement)

    response_links = [
        AnnouncementLinkResponse(id=link.id, url=link.url, title=link.title)
        for link in db_announcement.links
    ] if db_announcement.links else None

    response_data = AnnouncementResponse(
        id=db_announcement.id,
        name=db_announcement.name,
        description=db_announcement.description,
        image=db_announcement.image,
        is_urgent=db_announcement.is_urgent,
        platform=db_announcement.platform,
        links=response_links,
        user_id=db_announcement.user_id,
        created_at=db_announcement.created_at,
        updated_at=db_announcement.updated_at,
    )

    return ResponseModel(
        message="Announcement Updated Successfully",
        data=response_data,
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
