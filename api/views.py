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

@Routes.put('/services/{service_id}', tags=['services'], dependencies=[Depends(JWT_Bearer())])
async def update_service(service_id: int, service: schemas.Service, db: Session = Depends(con_db)):
    return crud.update_service(db, service_id, service)

@Routes.delete('/services/{service_id}', tags=['services'], dependencies=[Depends(JWT_Bearer())])
async def delete_service(service_id: int, db: Session = Depends(con_db)):
    return crud.delete_service(db, service_id)

""" 

Requirements Routes

"""

@Routes.post('/requirements/' ,tags=['requirements'], dependencies=[Depends(JWT_Bearer())])
async def create_requirement( req: schemas.Requirement, db: Session = Depends(con_db)):
    return crud.create_requirement(db, req)

@Routes.put('/requirements/{req_id}', tags=['requirements'], dependencies=[Depends(JWT_Bearer())])
async def update_requirement(req_id: int, req: schemas.Requirement, db: Session = Depends(con_db)):
    return crud.update_requirement(db, req_id, req)

@Routes.delete('/requirements/{req_id}', tags=['requirements'], dependencies=[Depends(JWT_Bearer())])
async def delete_requirement(req_id: int, db: Session = Depends(con_db)):
    return crud.delete_requirement(db, req_id)

@Routes.get('/requirements/', tags=['requirements'], dependencies=[Depends(JWT_Bearer())])
async def get_requirements(db: Session = Depends(con_db)):
    return crud.get_requirements(db)

@Routes.get('/requirements/{req_id}', tags=['requirements'], dependencies=[Depends(JWT_Bearer())])
async def get_requirement(req_id: int, db: Session = Depends(con_db)):
    return crud.get_requirement(db, req_id)


""" 

Req Categories Routes

"""

@Routes.get('/categories/', tags=['categories'], dependencies=[Depends(JWT_Bearer())])
async def get_categories(db: Session = Depends(con_db)):
    return crud.get_categories(db)

@Routes.get('/categories/{cat_id}', tags=['categories'], dependencies=[Depends(JWT_Bearer())])
async def get_category(cat_id: int, db: Session = Depends(con_db)):
    return crud.get_categories(db, cat_id)

@Routes.post('/categories/', tags=['categories'], dependencies=[Depends(JWT_Bearer())])
async def create_category(cat: schemas.Category, db: Session=Depends(con_db)):
    return crud.create_category(db, cat)

@Routes.put('/categories/{cat_id}', tags=['categories'], dependencies=[Depends(JWT_Bearer())])
async def update_category(cat_id: int, cat: schemas.Category, db: Session = Depends(con_db)):
    return crud.update_category(db, cat_id, cat)

@Routes.delete('/categories/{cat_id}', tags=['categories'], dependencies=[Depends(JWT_Bearer())])
async def delete_category(cat_id: int, db: Session = Depends(con_db)):
    return crud.delete_category(db, cat_id)

"""

Announcement Routes

"""

@Routes.get('/announcements/', tags=['announcements'], dependencies=[Depends(JWT_Bearer())])
async def get_announcements(db: Session = Depends(con_db)):
    return crud.get_announcements(db)

@Routes.get('/announcements/{ann_id}', tags=['announcements'], dependencies=[Depends(JWT_Bearer())])    
async def get_announcement(ann_id: int, db: Session = Depends(con_db)):
    return crud.get_announcements(db, ann_id)

@Routes.post('/announcements/', tags=['announcements'], dependencies=[Depends(JWT_Bearer())])
async def create_announcement(ann: schemas.Announcement, db: Session = Depends(con_db)):
    return crud.create_announcement(db, ann)

@Routes.put('/announcements/{ann_id}', tags=['announcements'], dependencies=[Depends(JWT_Bearer())])
async def update_announcement(ann_id: int, ann: schemas.Announcement, db: Session = Depends(con_db)):
    return crud.update_announcement(db, ann_id, ann)

@Routes.delete('/announcements/{ann_id}', tags=['announcements'], dependencies=[Depends(JWT_Bearer())])
async def delete_announcement(ann_id: int, db: Session = Depends(con_db)):
    return crud.delete_announcement(db, ann_id)

