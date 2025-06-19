from sqlalchemy.orm import Session, joinedload
from api import models
from typing import Optional
from fastapi import HTTPException

# modules
from api.schema.response import ResponseModel
from api.schema.category import *

def getCategories(db: Session, category_id: Optional[int] = None):
    query = db.query(models.Category)

    if category_id:
        # For specific category by ID, return 404 if not found
        category = query.filter(models.Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        return ResponseModel(
            message="Category found",
            data=CategoryResponse.model_validate(category, from_attributes=True),
            status_code=200,
        )
    
    # For "get all" operations, return empty array if none found
    categories = query.all()
    category_response = [CategoryResponse.model_validate(
        cat, from_attributes=True
    ) for cat in categories]

    return ResponseModel(
        message="Categories fetched successfully",
        data=category_response,
        status_code=200,
    )

def createCategory(db: Session, cat_data: CreateCategory) -> ResponseModel: 
    if db.query(models.Category).filter(models.Category.name == cat_data.name).first():
        raise HTTPException(status_code=400, detail="Category already exists")
    
    category = models.Category(name=cat_data.name, description=cat_data.description, status=cat_data.status)

    db.add(category)
    db.commit()
    db.refresh(category)

    return ResponseModel(
        message="Category Created Successfully",
        status_code=201,
    )

def updateCategory(db: Session, cat_id: int, cat_data: CreateCategory) -> ResponseModel:
    query = db.query(models.Category).filter(models.Category.id == cat_id).first()

    if not query:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if cat_data.name is not None:
        query.name = cat_data.name
    if cat_data.description is not None:
        query.description = cat_data.description
    if cat_data.status is not None:
        query.status = cat_data.status

    db.commit()
    db.refresh(query)

    return ResponseModel(
        message="Category Updated Successfully",
        status_code=200,
    )

def deleteCategory(db: Session, cat_id: int) -> ResponseModel:
    query = db.query(models.Category).filter(models.Category.id == cat_id).first()

    if not query:
        raise HTTPException(status_code=404, detail="Category not found")

    services_count = db.query(models.Service).filter(models.Service.category_id == cat_id).count()
    if services_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category. There are {services_count} services still connected to this category. Please reassign or delete these services first.")

    db.delete(query)
    db.commit()

    return ResponseModel(
        message="Category Deleted Successfully",
        status_code=200,
    )