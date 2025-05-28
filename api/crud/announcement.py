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
from PIL import Image

UPLOAD_DIR = "uploads/announcements/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
            raise HTTPException(status_code=400, detail="Invalid image_file type")
        
        unique_filename = f"{uuid4().hex}.{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)

        temp_path = image_path + ".temp"
        with open(temp_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)
        
        try:
            img = Image.open(temp_path)
            img.verify()

            img = Image.open(temp_path)

            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            img.save(image_path, quality=85, optimize=True)
            os.remove(temp_path) 

        except Exception as e:
            os.remove(temp_path)
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        finally:
            file.file.close()

    db_announcement = models.Announcement(
        name=announcement_data.name,
        description=announcement_data.description,
        image_path=image_path,
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

    return ResponseModel(
        message="Announcement Created Successfully",
        status_code=201,
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

    updated_path = db_announcement.image_path
    if file:
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid image_file type")
        
        unique_filename = f"{uuid4().hex}.{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)

        temp_path = image_path + ".temp"
        with open(temp_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)
        print(f"Temporary file saved: {os.path.exists(temp_path)}")
        
        try:
            img = Image.open(temp_path)
            img.verify()

            img = Image.open(temp_path)

            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            print(f"Saving processed image to: {image_path}")

            img.save(image_path, quality=85, optimize=True)
            print(f"Image saved: {os.path.exists(image_path)}")
            os.remove(temp_path) 

            updated_path = image_path

        except Exception as e:
            os.remove(temp_path)
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        finally:
            file.file.close()

    if announcement_data.name is not None:
        db_announcement.name = announcement_data.name
    if announcement_data.description is not None:
        db_announcement.description = announcement_data.description
    if announcement_data.is_urgent is not None:
        db_announcement.is_urgent = announcement_data.is_urgent
    if announcement_data.platform is not None:
        db_announcement.platform = announcement_data.platform
    if announcement_data.user_id is not None:
        db_announcement.user_id = announcement_data.user_id
    if updated_path:
        db_announcement.image_path = updated_path    
    

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
