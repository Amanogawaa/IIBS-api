from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api import crud, schemas, utils
from api.utils import JWT_Bearer

Routes = APIRouter()

def con_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

""" 

Auth Routes

"""

# create user
@Routes.post('/auth/', tags=['auth'])
async def create_user(user:schemas.UserCreate, db: Session = Depends(con_db)):
    return crud.create_user(db, user)

# login user
@Routes.post('/auth/login/', tags=['auth'])
async def login(db: Session = Depends(con_db), req: schemas.LoginBase | None = None):
    return crud.login_user(req, db)

# get single user
@Routes.get('/auth/{user_id}/', tags=['auth'])
async def get_user(db: Session = Depends(con_db), user_id: int | None = None):
    return crud.get_users(db, user_id)

# get all users
@Routes.get('/auth/', tags=['auth'])
async def get_users( db: Session = Depends(con_db)):
    return crud.get_users(db)


""" 

Services Routes

"""

@Routes.get('/services/{service_id}', tags=['services'],dependencies=[Depends(JWT_Bearer())])
async def get_service(service_id: int, db: Session = Depends(con_db) ):
    return crud.get_all_services(db, service_id)

@Routes.get('/services/', tags=['services'], dependencies=[Depends(JWT_Bearer())])
async def get_services(db: Session = Depends(con_db)):
    return crud.get_all_services(db)

@Routes.post('/services/', tags=['services'], dependencies=[Depends(JWT_Bearer())])
async def create_service(service: schemas.Service, db: Session = Depends(con_db)):
    return crud.create_service(db, service)


