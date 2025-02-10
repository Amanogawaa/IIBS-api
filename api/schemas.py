from pydantic import BaseModel

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
    

    
