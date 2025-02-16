from sqlalchemy.orm import Session, joinedload
from api import models
from typing import Union, Optional
from fastapi import HTTPException

# modules
from api.schema.service import *
from api.schema.response import ResponseModel


def create_service(db: Session, body: ServiceCreate):
    if db.query(models.Service).filter(models.Service.name == body.name).first():
        raise HTTPException(status_code=400, detail="Service already exists")

    service = models.Service(
        name=body.name, description=body.description, user_id=body.user_id
    )
    db.add(service)
    db.commit()
    db.refresh(service)

    return ResponseModel(
        message="Service Created Successfully",
        data=ServiceResponse(
            id=service.id,
            name=service.name,
            description=service.description,
            categories=[],
            created_at=service.created_at,
            updated_at=service.updated_at,
        ),
        status_code=200,
    )


def get_all_services(db: Session, service_id: Union[int, None] = None):
    query = db.query(models.Service).options(
        joinedload(models.Service.categories),
        joinedload(models.Service.categories).joinedload(
            models.ServiceCategory.requirements
        ),
    )

    if service_id:
        query = query.filter(models.Service.id == service_id)

    services = query.all()

    if not services:
        raise HTTPException(status_code=404, detail="Service not found")

    service_responses = [
        ServiceResponse.model_validate(service, from_attributes=True)
        for service in services
    ]

    return {
        "message": "Service Found" if service_id else "All Services",
        "data": service_responses,
        "status_code": 200,
    }


def update_service(db: Session, service_id: int, service_data: ServiceCreate):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.name = service_data.name or service.name
    service.description = service_data.description or service.description
    service.user_id = service_data.user_id or service.user_id

    db.commit()
    db.refresh(service)

    return ResponseModel(message="Service Updated Successfully", status_code=200)


def delete_service(db: Session, service_id: int):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()

    return ResponseModel(message="Service Deleted Successfully", status_code=200)
