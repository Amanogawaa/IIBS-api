import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from api import models

from api.schema.response import ResponseModel
from api.schema.business_info import *

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

def createInfo(db: Session, info_data: BusinessInfoCreate, attr_data: Optional[list[BusinessInfoAttributesCreate]]) -> ResponseModel:
    query = db.query(models.BusinessInfo).filter(models.BusinessInfo.name == info_data.name).first()

    if query:
        raise HTTPException(detail='Info already exist', status_code=404)

    info = models.BusinessInfo(
        name=info_data.name,
        logo=info_data.logo,
        description=info_data.description
    )

    db.add(info)
    db.commit()
    db.refresh(info)

    if attr_data is not None:
        for attr in attr_data:
            if attr.attribute_type == 'list':
                attr_value = json.dumps(attr.attribute_value)
            else:
                attr_value = attr.attribute_value
            
            attr_response = models.BusinessInfoAttribute(
                business_info_id = info.id,
                attribute_name=attr.attribute_name,
                attribute_value=attr_value,
                attribute_type=attr.attribute_type
            )

            db.add(attr_response)
        db.commit()

    return ResponseModel(
        message="Info Created Successfully",
        status_code=201,
    )


def update_information(db: Session, info_id: int, info_data:BusinessInfoCreate)-> ResponseModel:
    query = db.query(models.BusinessInfo).filter(models.BusinessInfo.id == info_id).first()

    if not query:
        raise HTTPException(status_code=404, detail='BusinessInfo not found')
    
    query.name = info_data.name
    query.logo = info_data.logo
    query.description = info_data.description

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
