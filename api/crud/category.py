from sqlalchemy.orm import Session, joinedload
from api import models
from typing import Optional
from fastapi import HTTPException

# modules
from api.schema.response import ResponseModel
from api.schema.category import *

def createCategory(db: Session, cat_data: CreateCategory) -> ResponseModel: 
    if db.query(models.Category).filter(models.Category.name == cat_data.name).first():
        raise HTTPException(status_code=400, detail="Category already exists")
    
    category = models.Category(name=cat_data.name, description=cat_data.description, status=cat_data.status)

    db.add(category)
    db.commit()
    db.refresh(category)

    return ResponseModel(
        message="Category Created Successfully",
        data=CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            status=category.status,
            created_at=category.created_at,
            updated_at=category.updated_at,
        ),
        status_code=201,
    )

def getCategories(db: Session, category_id: Optional[int | None]= None):
    query = db.query(models.Category)

    if category_id:
        query = query.filter(models.Category.id == category_id)

    categories = query.all()

    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    
    category_response = [CategoryResponse.model_validate(
        cat, from_attributes=True
    ) for cat in categories]

    return ResponseModel(
        message="Categories fetched successfully",
        data=category_response,
        status_code=200,
    )


def updateCategory(db: Session, cat_id: int, cat_data: CreateCategory) -> ResponseModel:
    query = db.query(models.Category).filter(models.Category.id == cat_id).first()

    if not query:
        raise HTTPException(status_code=404, detail="Category not found")
    
    query.name = cat_data.name
    query.description = cat_data.description
    query.status = cat_data.status

    db.commit()
    db.refresh(query)

    return ResponseModel(
        message="Category Updated Successfully",
        data=CategoryResponse.model_validate(query, from_attributes=True),
        status_code=200,
    )

def deleteCategory(db: Session, cat_id: int) -> ResponseModel:
    query = db.query(models.Category).filter(models.Category.id == cat_id).first()

    if not query:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(query)
    db.commit()

    return ResponseModel(
        message="Category Deleted Successfully",
        status_code=200,
    )