import json
import shutil
from uuid import uuid4
from sqlalchemy.orm import Session, joinedload
from api import models
from typing import Optional
from fastapi import HTTPException, UploadFile
import os
from PIL import Image

# modules
from api.schema.response import ResponseModel
from api.schema.service import *

UPLOAD_DIR = "uploads/service/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_service(db: Session, service_id: Optional[int | None] = None)-> ResponseModel:
    query = db.query(models.Service)

    if service_id:
        query = query.filter(models.Service.id == service_id)

    services = query.all()

    if not services:
        raise HTTPException(status_code=404, detail='Service not found')
    
    service_response = [ServiceResponse.model_validate(service, from_attributes=True) for service in services]

    return ResponseModel(
        message='Successfully get all services',
        data=service_response,
        status_code=200
    )

def createService(db: Session, service_data: ServiceCreate, attr_data: Optional[list[AttributeCreate]],  file: Optional[UploadFile] = None,)-> ResponseModel:
    if db.query(models.Service).filter(models.Service.name == service_data.name).first():
        raise HTTPException(status_code=400, detail="Service already exists")
    
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


    service = models.Service(
        name=service_data.name,
        description=service_data.description,
        status=service_data.status,
        image_path=image_path,
        user_id=service_data.user_id,
        category_id=service_data.category_id,
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    if attr_data is not None:
        for attr in attr_data:
            if attr.attribute_type == 'list':
                attr_value = json.dumps(attr.attribute_value)
            else:
                attr_value = attr.attribute_value
            
            attr_response = models.ServiceAttribute(
                service_id=service.id,
                attribute_name=attr.attribute_name,
                attribute_value=attr_value,
                attribute_type=attr.attribute_type
            )

            db.add(attr_response)
        db.commit()

    return ResponseModel(
        message="Service Created Successfully",
        status_code=201,
    )

def update_service(db: Session, service_id: int, service_data:ServiceCreate, attr_data: Optional[list[AttributeCreate]], file: Optional[UploadFile] = None,)-> ResponseModel:
    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail='Service not found')
    
    if service_data.name and service_data.name != service.name:
        if db.query(models.Service).filter(
            models.Service.name == service_data.name,
            models.Service.id != service_id
        ).first():
            raise HTTPException(status_code=400, detail="Service name already exists")

    updated_path = service.image_path
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

            img.save(image_path, quality=85, optimize=True)
            os.remove(temp_path) 

            updated_path = image_path

        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        finally:
            file.file.close()

    if service_data.name is not None:
        service.name = service_data.name
    if service_data.description is not None:
        service.description = service_data.description
    if service_data.status is not None:
        service.status = service_data.status
    if service_data.user_id is not None:
        service.user_id = service_data.user_id
    if service_data.category_id is not None:
        service.category_id = service_data.category_id
    if updated_path:
        service.image_path = updated_path

    if attr_data is not None:
        db.query(models.ServiceAttribute).filter(models.ServiceAttribute.service_id == service_id).delete()

        for attr in attr_data:
            if attr.attribute_value == 'list':
                attr_value = json.dumps(attr.attribute_value)
            else: 
                attr_value = str(attr.attribute_value)

            attr_response = models.ServiceAttribute(
                service_id=service.id,  
                attribute_name=attr.attribute_name,
                attribute_value=attr_value,
                attribute_type=attr.attribute_type
            )
            db.add(attr_response)

    db.commit()
    db.refresh(service)

    return ResponseModel(
        message="Service Updated Successfully",
        status_code=200
    )

def delete_service(db: Session, service_id: int)-> ResponseModel:
    query = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not query:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(query)
    db.commit()

    return ResponseModel(
        message="Servie Deleted Successfully",
        status_code=200,
    )