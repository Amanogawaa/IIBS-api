from sqlalchemy.orm import Session, joinedload
from api import models
from typing import Union
from fastapi import HTTPException

# module
from api.schema.response import ResponseModel
from api.schema.service_category import *


def get_categories(db: Session, category_id: Union[int, None] = None):
    query = db.query(models.ServiceCategory).options(joinedload(models.ServiceCategory.requirements))

    if category_id:
        query = query.filter(models.ServiceCategory.id == category_id)

    categories = query.all()

    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")

    category_response = [CategoryResponse.model_validate(cat, from_attributes=True) for cat in categories]

    return ResponseModel(
        message="Category Found" if category_id else 'All Categories',
        data=category_response,
        status_code=200,
    )


def create_category(db: Session, body: CategoryBase) -> ResponseModel:
    if db.query(models.ServiceCategory).filter(models.ServiceCategory.name == body.name).first():
        raise HTTPException(status_code=400, detail="Category already exists")

    services = db.query(models.Service).filter(models.Service.id.in_(body.service_ids)).all()

    category = models.ServiceCategory(name=body.name, services=services)
    db.add(category)
    db.commit()
    db.refresh(category)

    return ResponseModel(
        message="Category Created Successfully",
        data=CategoryResponse(
            id=category.id,
            name=category.name,
            created_at=category.created_at,
            updated_at=category.updated_at,
        ),
        status_code=200,
    )


def update_category(db: Session, cat_id: int, cat: CategoryBase):
    category = (
        db.query(models.ServiceCategory)
        .filter(models.ServiceCategory.id == cat_id)
        .first()
    )

    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = cat.name or category.name

    db.commit()
    db.refresh(category)

    return ResponseModel(
        message="Category Updated Successfully", status_code=200
    )


def delete_category(db: Session, cat_id: int):
    cat = (
        db.query(models.ServiceCategory)
        .filter(models.ServiceCategory.id == cat_id)
        .first()
    )

    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(cat)
    db.commit()

    return ResponseModel(
        message="Category Deleted Successfully", status_code=200
    )
