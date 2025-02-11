from pydantic import BaseModel
from typing import List, Optional

"""

User Schemas

"""
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginBase(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str


"""

Service Schemas

"""
class Service(BaseModel):
    name: str
    description: str
    

"""

Requirements Schemas

"""

class Requirement(BaseModel):
    name: str
    description: str
    category_id: int
    service_ids: List[int]
    
    class Config:
        orm_mode: True

    
"""

Category Schemas

"""

class Category(BaseModel):
    name: str
    
    class Config:
        orm_mode: True
    

"""

Announcement Schemas

"""

class Announcement(BaseModel):
    name: str
    description: str
    user_id: int
    
    class Config:
        orm_mode: True