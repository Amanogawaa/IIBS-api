import json
from sqlalchemy.orm import Session, joinedload
from api import models
from typing import Optional
from fastapi import HTTPException

# modules
from api.schema.response import ResponseModel
from api.schema.service import *


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

def createService(db: Session, service_data: ServiceCreate, attr_data: Optional[list[AttributeCreate]])-> ResponseModel:
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

def update_service(db: Session, service_id: int, service_data:ServiceCreate, attr_data: Optional[list[AttributeCreate]])-> ResponseModel:
    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail='Service not found')
    
    if service_data.name and service_data.name != service.name:
        if db.query(models.Service).filter(
            models.Service.name == service_data.name,
            models.Service.id != service_id
        ).first():
            raise HTTPException(status_code=400, detail="Service name already exists")

    if service_data.name is not None:
        service.name = service_data.name
    if service_data.description is not None:
        service.description = service_data.description
    if service_data.status is not None:
        service.status = service_data.status
    if service_data.file_path is not None:
        service.file_path = service_data.file_path
    if service_data.image_path is not None:
        service.image_path = service_data.image_path
    if service_data.user_id is not None:
        service.user_id = service_data.user_id
    if service_data.category_id is not None:
        service.category_id = service_data.category_id

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