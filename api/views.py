from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

# schemas
from api.database import SessionLocal
from api.utils import JWT_Bearer
from api.schema.user import *
from api.schema.service import *
from api.schema.announcement import *
from api.schema.faqs import *

# v2
from api.schema.category import *
from api.schema.service import * 

# crud
import api.crud.user as user
import api.crud.category as category
import api.crud.service as service
import api.crud.announcement as announcement
import api.crud.faqs as faqs

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

@Routes.get("/auth/{user_id}/", tags=["auth"])
async def get_user(db: Session = Depends(con_db), user_id: int | None = None):
    return user.get_all_users(db, user_id)

@Routes.get("/auth/", tags=["auth"])
async def get_users(db: Session = Depends(con_db)):
    return user.get_all_users(db)

@Routes.post("/auth/", tags=["auth"])
async def create_user(user_data: UserCreate, db: Session = Depends(con_db)):
    return user.register_user(db, user_data)

@Routes.post("/auth/login/", tags=["auth"])
async def login(db: Session = Depends(con_db), req: LoginBase | None = None):
    return user.login_user(req, db)


"""
Category Routes
"""

@Routes.post('/category/', tags=['category'])
async def create_category( cat_data: CreateCategory, db: Session = Depends(con_db)):
    return category.createCategory(db, cat_data)

@Routes.get('/category/', tags=['category'])    
async def get_category(cat_id: Optional[int | None] = None, db: Session = Depends(con_db)):
    return category.getCategories(db, cat_id)

@Routes.put('/category/{cat_id}', tags=['category'])
async def update_category(cat_id: int, cat_data: CreateCategory, db: Session = Depends(con_db)):
    return category.updateCategory(db, cat_id, cat_data)

@Routes.delete('/category/{cat_id}', tags=['category'])
async def delete_category(cat_id: int, db: Session = Depends(con_db)):
    return category.deleteCategory(db, cat_id)

"""
Services Routes
"""

@Routes.post('/services/', tags=['services'])
async def create_service(service_data: ServiceCreate, db: Session = Depends(con_db)):
    return service.createService(db, service_data)

@Routes.put('/services/{service_id}',  tags=['services'])
async def update_service(service_id: int, service_data: ServiceCreate,db: Session = Depends(con_db) ):
    return service.update_service(db, service_id, service_data)

@Routes.get('/services/', tags=['services'])
async def get_services(service_id: Optional[int | None] = None, db: Session = Depends(con_db)):
    return service.get_service(db, service_id)

@Routes.delete('/services/{service_id}', tags=['services'])
async def delete_category(service_id: int, db: Session = Depends(con_db)):
    return service.delete_service(db, service_id)



"""
Announcement Routes
"""

@Routes.get("/announcements/", tags=["announcements"])
async def get_announcements(db: Session = Depends(con_db)):
    return announcement.get_announcements(db)

@Routes.get("/announcements/{ann_id}", tags=["announcements"])
async def get_announcement(ann_id: int, db: Session = Depends(con_db)):
    return announcement.get_announcements(db, ann_id)

@Routes.post("/announcements/", tags=["announcements"])
async def create_announcement(
    name: str = Form(...),
    description: str = Form(...),
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(con_db),
):
    return announcement.create_announcement(db, name, description, user_id, file)

@Routes.put(
    "/announcements/{ann_id}",
    tags=["announcements"],
    dependencies=[Depends(JWT_Bearer())],
)
async def update_announcement(
    ann_id: int, ann: Announcement, db: Session = Depends(con_db)
):
    return announcement.update_announcement(db, ann_id, ann)

@Routes.delete(
    "/announcements/{ann_id}",
    tags=["announcements"],
    dependencies=[Depends(JWT_Bearer())],
)
async def delete_announcement(ann_id: int, db: Session = Depends(con_db)):
    return announcement.delete_announcement(db, ann_id)

""" 
FAQS Routes
"""

@Routes.get("/faqs", tags=["faqs"])
async def get_faqs(db: Session = Depends(con_db)):
    return faqs.get_all_faqs(db)

@Routes.get("/faqs/{faqs_id}", tags=["faqs"])
async def get_faq(faqs_id: int, db: Session = Depends(con_db)):
    return faqs.get_all_faqs(db, faqs_id)

@Routes.post("/faqs/", tags=["faqs"], dependencies=[Depends(JWT_Bearer())])
async def create_faq(faq: FaqCreate, db: Session = Depends(con_db)):
    return faqs.create_faq(db, faq)

@Routes.put("/faqs/{faqs_id}", tags=["faqs"], dependencies=[Depends(JWT_Bearer())])
async def update_faq(faqs_id: int, faq: FaqCreate, db: Session = Depends(con_db)):
    return faqs.update_faq(db, faqs_id, faq)

@Routes.delete("/faqs/{faqs_id}", tags=["faqs"], dependencies=[Depends(JWT_Bearer())])
async def delete_faq(faqs_id: int, db: Session = Depends(con_db)):
    return faqs.delete_faq(db, faqs_id)
