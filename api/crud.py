from sqlalchemy.orm import Session
from api import models, schemas
from api.schemas import  Token
from typing import Union
from fastapi import HTTPException
from api.utils import hash_password, verify_password, create_access_token, refresh_token


""" 

Service CRUD Operations

"""


# <-- Post  Method -->

""" 

TODO: Add a method to check if the service already exists in the database

"""

def create_service(db: Session, service: schemas.Service):
    
    if check_service(db, service.name):
        raise HTTPException(status_code=400, detail="Service already exists")
    
    db_service = models.Service(name=service.name, description=service.description)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service

def check_service(db: Session, service: str):
    service = db.query(models.Service).filter(models.Service.name == service).first()
    
    if service:
        return True
    return False    

# <-- Get Method -->

def get_all_services(db: Session, service_id: Union[int | None] = None):
    if service_id:
        service = db.query(models.Service).filter(models.Service.id == service_id).first()
        
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        return service
    
    return db.query(models.Service).all()



""" 

User CRUD Operations

"""

# <-- Post  Method -->

""" 

TODO: Add a method to check if the username already exists in the database [/]
TODO: Add a method to check if the email already exists in the database [/]
TODO: Validate if the email is a valid email [x]
    
"""

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


