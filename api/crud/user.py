from sqlalchemy.orm import Session
from api import models
from fastapi import HTTPException
from typing import Union, Optional

# modules
from api.utils import hash_password, verify_password, create_access_token, refresh_token
from api.schema.user import *
from api.schema.response import ResponseModel


def register_user(db: Session, user: UserCreate):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    hash_pass = hash_password(user.password)

    db_user = models.User(username=user.username, email=user.email, password=hash_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return ResponseModel(
        message="User Created Successfully",
        status_code=200,
    )


def login_user(req: LoginBase, db: Session):
    user = db.query(models.User).filter(models.User.email == req.email).first()

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid Email")

    if not verify_password(req.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid Password")

    access = create_access_token(user.id, [user.email, user.username])
    refresh = refresh_token(user.id)

    return Token(access_token=access, refresh_token=refresh)


def get_all_users(db: Session, user_id: Optional[int] = None):
    if user_id is not None:
        user = db.query(models.User).filter(models.User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return ResponseModel(
            message="User Found",
            data=UserResponse.model_validate(user),
            status_code=200,
        )

    result = db.query(models.User).all()
    return ResponseModel(
        message="All Users",
        data=[UserResponse.model_validate(user) for user in result],
        status_code=200,
    )
