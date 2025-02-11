from sqlalchemy.orm import Session
from api import models, schemas
from api.schemas import  Token
from typing import Union
from fastapi import HTTPException
from api.utils import hash_password, verify_password, create_access_token, refresh_token

""" 

User CRUD Operations

"""

# <-- Post  Method -->
def create_user(db:Session, user: schemas.UserCreate):
    # checks if the email and username already exists in the database | query the User Table and filter by email and username
    user_email = db.query(models.User).filter(models.User.email == user.email).first()
    user_name = db.query(models.User).filter(models.User.username == user.username).first()

    try:
        # validations
        if user_email:
            raise HTTPException(status_code=400, detail="Email already exists")
        if user_name:
            raise HTTPException(status_code=400, detail="Username already exists")

        # hashes the password if 2  validations return False
        hash_pass = hash_password(user.password)

        # creates a new user
        db_user = models.User(username=user.username, email=user.email, password=hash_pass)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {'message': 'User Created Successfully', 'status': 200}

    except Exception as e:
        return {'message': e, 'status': 400}

def login_user(req: schemas.LoginBase, db: Session):
    user = db.query(models.User).filter(models.User.email == req.email).first()

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid Email")

    # hash_password(req.password)

    if not verify_password(req.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid Password")

    access = create_access_token(user.id)
    refresh = refresh_token(user.id)

    return Token(access_token=access, refresh_token=refresh)

# <-- Get Method -->
def get_users(db: Session, user_id: Union[int | None] = None):
    if user_id:
        user = db.query(models.User).filter(models.User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    return db.query(models.User).all()


""" 

Service CRUD Operations

"""

# <-- Post  Method -->
def create_service(db: Session, service: schemas.Service):
    ser_name = db.query(models.Service).filter(models.Service.name == service.name).first()
    
    if ser_name:
        raise HTTPException(status_code=400, detail="Service already exists")
    
    db_service = models.Service(name=service.name, description=service.description)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service

# <-- Get Method -->
def get_all_services(db: Session, service_id: Union[int | None] = None):
    if service_id:
        service = db.query(models.Service).filter(models.Service.id == service_id).first()
        
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        return service
    
    return db.query(models.Service).all()

# <-- Put Method -->
def update_service(db: Session, service_id: int, service: schemas.Service):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")   
    
    update_service = models.Service(name=service.name, description=service.description)
    db.add(update_service) 
    db.commit()
    db.refresh(update_service)
     
    return {'message': 'Service Updated Successfully', 'status': 200}
    
# <-- Delete Method -->
def delete_service(db:Session, service_id: int):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()

    return {'message': 'Service Deleted Successfully', 'status': 200}

"""

Requirement CRUD Operations

"""

# <-- Get Method -->
def get_requirements(db:Session, req_id: Union[int | None] = None):
    
    if req_id:
        req = db.query(models.Requirement).filter(models.Requirement.id == req_id).first()

        if not req:
            raise HTTPException(status_code=404, detail="Requirement not found")

        return req 
        
    return db.query(models.Requirement).all()

# <-- Post Method -->
def create_requirement(db: Session, req: schemas.Requirement):
    name = db.query(models.Requirement).filter(models.Requirement.name == req.name).first()
    
    if name:
        raise HTTPException(status_code=400, detail="Requirement already exists")
    
    services = db.query(models.Service).filter(models.Service.id.in_(req.service_ids)).all()
    
    if not services:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db_req = models.Requirement(
        name=req.name,
        description=req.description, 
        category_id=req.category_id,
        services=services  
    )
    
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    
    return {'message': 'Requirement Created Successfully', 'status': 200}

# <-- Put Method -->
def update_requirement(db: Session, req_id: int, req: schemas.Requirement):
    req = db.query(models.Requirement).filter(models.Requirement.id == req_id).first()
    
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    update_req = models.Requirement(name=req.name, description=req.description)
    
    db.add(update_req)
    db.commit()
    db.refresh(update_req)

    return {'message': 'Requirement Updated Successfully', 'status': 200}

# <-- Delete Method -->
def delete_requirement(db:Session, req_id: int):
    req = db.query(models.Requirement).filter(models.Requirement.id == req_id).first()

    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")

    db.delete(req)
    db.commit()

    return {'message': 'Requirement Deleted Successfully', 'status': 200}

"""

Category Crud Operations

"""

# <-- Get Method -->
def get_categories(db:Session, cat_id: Union[int | None] = None):
    if cat_id:
        cat = db.query(models.RequirementCategory).filter(models.RequirementCategory.id == cat_id).first()
        
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
        
        return cat
    
    return db.query(models.RequirementCategory).all()

# <-- Post Method -->
def create_category(db: Session, req: schemas.Category):
    cat = db.query(models.RequirementCategory).filter(models.RequirementCategory.name == req.name).first()
    
    if cat:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db_cat = models.RequirementCategory(name=req.name)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    
    return {'message': 'Category Created Successfully', 'status': 200}   

# <-- Put Method -->
def update_category(db: Session, cat_id: int, cat: schemas.Category):
    cat = db.query(models.RequirementCategory).filter(models.RequirementCategory.id == cat_id).first()
    
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_cat = models.RequirementCategory(name=cat.name)
    
    db.add(update_cat)
    db.commit()
    db.refresh(update_cat)
    
    return {'message': 'Category Updated Successfully', 'status': 200}

# <-- Delete Method -->
def delete_category(db: Session, cat_id: int):
    cat = db.query(models.RequirementCategory).filter(models.RequirementCategory.id == cat_id).first()
    
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(cat)
    db.commit()
    
    return {'message': 'Category Deleted Successfully', 'status': 200}

"""

Announcement Crud Operations

"""

# <-- Get Method -->
def get_announcements(db:  Session, announcement_id: Union[int | None] = None):
    if announcement_id:
        announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
        
        if not announcement:
            raise HTTPException(status_code=404, detail="Announcement not found")
        
        return announcement
    return db.query(models.Announcement).all()

# <-- Post Method -->
def create_announcement(db: Session, user_id: int, req: schemas.Announcement):
    if not user_id:
        raise HTTPException(status_code=400, detail="User id not found")
    
    db_announcement = models.Announcement(name=req.name, description=req.description, user_id=user_id)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    
    return {'message': 'Announcement Created Successfully', 'status': 200}

# <-- Put Method -->
def update_announcement(db:Session, announcement_id: int, req: schemas.Announcement):
    announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    update_announcement = models.Announcement(name=req.name, description=req.description)
    
    db.add(update_announcement)
    db.commit()
    db.refresh(update_announcement)
    
    return {'message': 'Announcement Updated Successfully', 'status': 200}

# <-- Delete Method -->
def delete_announcement(db: Session, announcement_id: int):
    announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    db.delete(announcement)
    db.commit()
    
    return {'message': 'Announcement Deleted Successfully', 'status': 200}