from sqlalchemy.orm import Session
from api import models
from typing import Union, Optional
from fastapi import HTTPException

# modules
from api.schema.requirement import *
from api.schema.response import ResponseModel


def get_requirements(
        db: Session, req_id: Union[int | None] = None
):
    query = db.query(models.Requirement)

    if req_id:
        query = query.filter(models.Requirement.id == req_id)

    reqs = query.all()

    if not reqs:
        raise HTTPException(status_code=404, detail="No requirements found")

    reqs_response = [RequirementResponse.model_validate(req, from_attributes=True) for req in reqs]

    return ResponseModel(
        message="Requirements fetched successfully",
        data=reqs_response,
        status_code=200
    )


def create_requirement(db: Session, req: RequirementBase):
    existing_req = db.query(models.Requirement).filter(models.Requirement.name == req.name).first()
    if existing_req:
        raise HTTPException(status_code=400, detail="Requirement already exists")

    # not actually neeeded to get the categories
    # might need to remove the categories-id from response
    categories = db.query(models.ServiceCategory).filter(models.ServiceCategory.id.in_(req.category_ids)).all()
    if not categories or len(categories) != len(req.category_ids):
        raise HTTPException(status_code=404, detail="One or more categories not found")

    db_req = models.Requirement(
        name=req.name,
        description=req.description,
        categories=categories,
    )

    db.add(db_req)
    db.commit()
    db.refresh(db_req)

    return ResponseModel(
        message="Requirement Created Successfully",
        data=RequirementResponse.model_validate(db_req, from_attributes=True),
        status_code=200
    )


def update_requirement(db: Session, req_id: int, req_data: RequirementBase):
    db_req = db.query(models.Requirement).filter(models.Requirement.id == req_id).first()

    if not db_req:
        raise HTTPException(status_code=404, detail="Requirement not found")

    categories = db.query(models.ServiceCategory).filter(models.ServiceCategory.id.in_(req_data.category_ids)).all()
    if not categories or len(categories) != len(req_data.category_ids):
        raise HTTPException(status_code=404, detail="One or more categories not found")

    db_req.name = req_data.name or db_req.name
    db_req.description = req_data.description or db_req.description
    db_req.categories = categories

    db.commit()
    db.refresh(db_req)

    return ResponseModel(
        message="Successfully updated",
        data=RequirementResponse.model_validate(db_req, from_attributes=True),
        status_code=200
    )


def delete_requirement(db: Session, req_id: int):
    req = db.query(models.Requirement).filter(models.Requirement.id == req_id).first()

    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")

    db.delete(req)
    db.commit()

    return ResponseModel(
        message="Requirement Deleted Successfully", status_code=200
    )
