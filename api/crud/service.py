from sqlalchemy.orm import Session, joinedload
from api import models
from typing import Optional
from fastapi import HTTPException

# modules
from api.schema.response import ResponseModel
from api.schema.service import *

def createService(db: Session, service_data: ServiceCreate)-> ResponseModel:
    if db.query(models.Service).filter(models.Service.name == service_data.name).first():
        raise HTTPException(status_code=400, detail="Service already exists")
    
    service = models.Service(
        name=service_data.name,
        description=service_data.description,
        status=service_data.status,
        file_path=service_data.file_path,
        image_path=service_data.image_path,
        user_id=service_data.user_id,
        category_id=service_data.category_id,
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return ResponseModel(
        message="Service Created Successfully",
        data=ServiceResponse(
            id=service.id,
            name=service_data.name,
            description=service_data.description,
            status=service_data.status,
            file_path=service_data.file_path,
            image_path=service_data.image_path,
            user_id=service_data.user_id,
            category_id=service_data.category_id,
            created_at=service.created_at,
            updated_at=service.updated_at,
        ),
        status_code=201,
    )

def update_service(db: Session, service_id: int, service_data:ServiceCreate)-> ResponseModel:
    query = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not query:
        raise HTTPException(status_code=404, detail='Service not found')
    
    query.name = service_data.name
    query.description = service_data.description
    query.status = service_data.status
    query.file_path = service_data.file_path
    query.image_path = service_data.image_path
    query.user_id = service_data.user_id
    query.category_id = service_data.category_id

    db.commit()
    db.refresh(query)

    return ResponseModel(
        message="Service Updated Successfully",
        data=ServiceResponse.model_validate(query, from_attributes=True),
        status_code=200
    )

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