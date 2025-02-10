from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api import crud, schemas
from typing import Annotated


Routes = APIRouter()

def con_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
# This is a dependency that will be used to inject the database session into the route functions.
db_dependency = Annotated[Session, Depends(con_db)]  

@Routes.get('/users')
async def get_users():
    return []

@Routes.post('/services/')
async def create_service(service: schemas.Service, db: db_dependency):
    return crud.create_service(db, service)
