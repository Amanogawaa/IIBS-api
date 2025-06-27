import json
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import Optional
from api import models
import os
from PIL import Image
from uuid import uuid4
import shutil

from api.schema.response import ResponseModel
from api.schema.business_info import *

UPLOAD_DIR = "uploads/business_info/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def business_info_exists_by_user(db: Session, user_id: int) -> bool:
    result = db.query(models.BusinessInfo).filter(models.BusinessInfo.user_id == user_id).first()
    print(result)
    return result is not None

def get_information(db: Session, info_id: Optional[int | None] = None)-> ResponseModel:
    query = db.query(models.BusinessInfo)

    if info_id:
        query = query.filter(models.BusinessInfo.id == info_id)

    informations = query.all()

    if not informations:
        raise HTTPException(status_code=404, detail='Business Information not found')
    
    service_response = [BusinessInfoResponse.model_validate(info, from_attributes=True) for info in informations]

    return ResponseModel(
        message='Successfully get all BusinessInfo',
        data=service_response,
        status_code=200
    )

def createInfo(db: Session, info_data: BusinessInfoCreate, file: Optional[UploadFile] = None) -> ResponseModel:
    query = db.query(models.BusinessInfo).filter(models.BusinessInfo.name == info_data.name).first()
    if query:
        raise HTTPException(detail='Info already exist', status_code=404)
    
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
    
    info = models.BusinessInfo(
        # Core Public Information
        name=info_data.name,
        logo=image_path,
        description=info_data.description,
        tagline=info_data.tagline,
        user_id=info_data.user_id,
        
        # Contact & Location
        email=info_data.email,
        phone=info_data.phone,
        website=info_data.website,
        address=info_data.address,
        city=info_data.city,
        state=info_data.state,
        country=info_data.country,
        postal_code=info_data.postal_code,
        
        # Business Details
        industry=info_data.industry,
        business_type=info_data.business_type,
        founded_date=info_data.founded_date,
        employee_count_range=info_data.employee_count_range,
        
        # Operating Information
        business_hours=info_data.business_hours,
        timezone=info_data.timezone,
        
        # Social & Online Presence
        social_media=info_data.social_media,
    )
    
    db.add(info)
    db.commit()
    db.refresh(info)
    
    return ResponseModel(
        message="Info Created Successfully",
        status_code=201,
    )


def update_information(db: Session, info_id: int, info_data:BusinessInfoCreate, file: Optional[UploadFile] = None)-> ResponseModel:
    query = db.query(models.BusinessInfo).filter(models.BusinessInfo.id == info_id).first()

    if not query:
        raise HTTPException(status_code=404, detail='BusinessInfo not found')
    
    updated_path = info_data.image_url
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


    if info_data.name is not None:
        query.name = info_data.name
    if info_data.description is not None:
        query.description = info_data.description
    if info_data.tagline is not None:
        query.tagline = info_data.tagline
    if info_data.user_id is not None:
        query.user_id = info_data.user_id
    if info_data.email is not None:
        query.email = info_data.email
    if info_data.phone is not None:
        query.phone = info_data.phone
    if info_data.website is not None:
        query.website = info_data.website
    if info_data.address is not None:
        query.address = info_data.address
    if info_data.city is not None:
        query.city = info_data.city
    if info_data.state is not None:
        query.state = info_data.state
    if info_data.country is not None:
        query.country = info_data.country
    if info_data.postal_code is not None:
        query.postal_code = info_data.postal_code
    if info_data.industry is not None:
        query.industry = info_data.industry
    if info_data.business_type is not None:
        query.business_type = info_data.business_type
    if info_data.founded_date is not None:
        query.founded_date = info_data.founded_date
    if info_data.employee_count_range is not None:
        query.employee_count_range = info_data.employee_count_range
    if info_data.business_hours is not None:
        query.business_hours = info_data.business_hours
    if info_data.timezone is not None:
        query.timezone = info_data.timezone
    if info_data.social_media is not None:
        query.social_media = info_data.social_media
    if updated_path:
        query.image_url = updated_path
   
    db.commit()
    db.refresh(query)

    return ResponseModel(
        message="BusinessInfo Updated Successfully",
        status_code=200
    )

def delete_information(db: Session, info_id: int)-> ResponseModel:
    query = db.query(models.BusinessInfo).filter(models.BusinessInfo.id == info_id).first()

    if not query:
        raise HTTPException(status_code=404, detail="BusinessInfo not found")

    db.delete(query)
    db.commit()

    return ResponseModel(
        message="BusinessInfo Deleted Successfully",
        status_code=200,
    )
