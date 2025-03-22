import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

# utils
from api.utils import JWT_Bearer
from api.form_parser import parse_announcement_form

# schemas
from api.database import SessionLocal
from api.schema.user import *
from api.schema.service import *
from api.schema.announcement import *
from api.schema.faqs import *
from api.schema.category import *
from api.schema.service import * 
from api.schema.business_info import * 

# crud
import api.crud.user as user
import api.crud.category as category
import api.crud.service as service
import api.crud.announcement as announcements
import api.crud.faqs as faqs
import api.crud.business_info as infos

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

@Routes.get("/auth/", tags=["auth"])
async def get_users(db: Session = Depends(con_db)):
    return user.get_all_users(db)

@Routes.get("/auth/{user_id}/", tags=["auth"])
async def get_user(db: Session = Depends(con_db), user_id: int | None = None):
    return user.get_all_users(db, user_id)

@Routes.post("/auth/", tags=["auth"])
async def create_user(user_data: UserCreate, db: Session = Depends(con_db)):
    return user.register_user(db, user_data)

@Routes.post("/auth/login/", tags=["auth"])
async def login(db: Session = Depends(con_db), req: LoginBase | None = None):
    return user.login_user(req, db)


"""
Category Routes
"""

@Routes.get('/category/', tags=['category'])    
async def get_category(db: Session = Depends(con_db)):
    return category.getCategories(db)

@Routes.get('/category/{cat_id}', tags=['category'])    
async def get_category(cat_id: Optional[int | None] = None, db: Session = Depends(con_db)):
    return category.getCategories(db, cat_id)

@Routes.post('/category/', tags=['category'])
async def create_category( cat_data: CreateCategory, db: Session = Depends(con_db)):
    return category.createCategory(db, cat_data)

@Routes.put('/category/{cat_id}', tags=['category'])
async def update_category(cat_id: int, cat_data: CreateCategory, db: Session = Depends(con_db)):
    return category.updateCategory(db, cat_id, cat_data)

@Routes.delete('/category/{cat_id}', tags=['category'])
async def delete_category(cat_id: int, db: Session = Depends(con_db)):
    return category.deleteCategory(db, cat_id)

"""
Services Routes
"""

@Routes.get('/services/', tags=['services'])
async def get_services(db: Session = Depends(con_db)):
    return service.get_service(db)

@Routes.get('/services/{service_id}', tags=['services'])
async def get_services(service_id: Optional[int | None] = None, db: Session = Depends(con_db)):
    return service.get_service(db, service_id)

@Routes.post('/services/', tags=['services'])
async def create_service(service_data: ServiceCreate, db: Session = Depends(con_db)):
    return service.createService(db, service_data)

@Routes.put('/services/{service_id}',  tags=['services'])
async def update_service(service_id: int, service_data: ServiceCreate,db: Session = Depends(con_db) ):
    return service.update_service(db, service_id, service_data)

@Routes.delete('/services/{service_id}', tags=['services'])
async def delete_category(service_id: int, db: Session = Depends(con_db)):
    return service.delete_service(db, service_id)

"""
Announcement Routes
"""

@Routes.get("/announcements/", tags=["announcements"])
async def get_faqs(db: Session = Depends(con_db)):
    return announcements.get_announcements(db)

@Routes.get("/announcements/{announcement_id}", tags=["announcements"])
async def get_faq(announcement_id: int, db: Session = Depends(con_db)):
    return announcements.get_announcements(db, announcement_id)

@Routes.post("/announcements/", tags=["announcements"])
async def create_announcement(
    announcement: AnnouncementCreate = Depends(parse_announcement_form),
    links: Optional[str] = Form(None), 
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(con_db),
):
    links_list = None
    if links:
        try:
            links_list = json.loads(links)
            if not isinstance(links_list, list):
                raise ValueError("Links must be a list")
            links_list = [AnnouncementLinkCreate(**item) for item in links_list]
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=422, detail=f"Invalid links format: {str(e)}")
    
    return announcements.create_announcement(db, announcement, links_list, file)

@Routes.put(
    "/announcements/{announcement_id}",
    tags=["announcements"]
)
async def update_announcement(
    announcement_id: int,
    announcement: AnnouncementCreate = Depends(parse_announcement_form),
    links: Optional[str] = Form(None), 
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(con_db),
):
    links_list = None
    if links:
        try:
            links_list = json.loads(links)
            if not isinstance(links_list, list):
                raise ValueError("Links must be a list")
            links_list = [AnnouncementLinkCreate(**item) for item in links_list]
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=422, detail=f"Invalid links format: {str(e)}")
    
    return announcements.update_announcement(db,announcement_id, announcement, links_list, file)


@Routes.delete(
    "/announcements/{ann_id}",
    tags=["announcements"]
)
async def delete_announcement(ann_id: int, db: Session = Depends(con_db)):
    return announcements.delete_announcement(db, ann_id)

""" 
FAQS Routes
"""

@Routes.get("/faqs/", tags=["faqs"])
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

"""
Information Routes
"""

@Routes.get('/information/', tags=['information'])
async def get_infos(db: Session = Depends(con_db)):
    return infos.get_information(db)

@Routes.get('/information/{info_id}', tags=['information'])
async def get_infos(info_id: int, db: Session = Depends(con_db)):
    return infos.get_information(db, info_id)

@Routes.post('/information/', tags=['information'])
async def creat_information(info_data: BusinessInfoCreate, db: Session = Depends(con_db)):
    return infos.createInfo(db, info_data)

@Routes.put("/information/{info_id}", tags=["information"],)
async def update_info(info_id: int, info_data: BusinessInfoCreate, db: Session = Depends(con_db)):
    return infos.update_information(db, info_id, info_data)

@Routes.delete("/information/{info_id}", tags=["information"])
async def delete_info(info_id: int, db: Session = Depends(con_db)):
    return infos.delete_information(db, info_id)
