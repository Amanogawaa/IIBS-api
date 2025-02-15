from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# schemas
from api.database import SessionLocal
from api import utils
from api.utils import JWT_Bearer
from api.schema.user import *
from api.schema.service import *
from api.schema.service_category import *
from api.schema.requirement import *
from api.schema.announcement import *

# crud
import api.crud.user as user
import api.crud.services as services
import api.crud.category as category
import api.crud.requirements as requirements
import api.crud.announcement as announcement

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
Services Routes
"""


@Routes.get("/services/{service_id}", tags=["services"])
async def get_service(service_id: int, db: Session = Depends(con_db)):
    return services.get_all_services(db, service_id)


@Routes.get("/services/", tags=["services"])
async def get_services(db: Session = Depends(con_db)):
    return services.get_all_services(db)


@Routes.post("/services/", tags=["services"], dependencies=[Depends(JWT_Bearer())])
async def create_service(service: ServiceCreate, db: Session = Depends(con_db)):
    return services.create_service(db, service)


@Routes.put(
    "/services/{service_id}", tags=["services"], dependencies=[Depends(JWT_Bearer())]
)
async def update_service(
    service_id: int, service: ServiceCreate, db: Session = Depends(con_db)
):
    return services.update_service(db, service_id, service)


@Routes.delete(
    "/services/{service_id}", tags=["services"], dependencies=[Depends(JWT_Bearer())]
)
async def delete_service(service_id: int, db: Session = Depends(con_db)):
    return services.delete_service(db, service_id)


"""
Req Categories Routes
"""


@Routes.get("/categories/", tags=["categories"])
async def get_categories(db: Session = Depends(con_db)):
    return category.get_categories(db)


@Routes.get("/categories/{cat_id}", tags=["categories"])
async def get_category(cat_id: int, db: Session = Depends(con_db)):
    return category.get_categories(db, cat_id)


@Routes.post("/categories/", tags=["categories"], dependencies=[Depends(JWT_Bearer())])
async def create_category(cat: CategoryBase, db: Session = Depends(con_db)):
    return category.create_category(db, cat)


@Routes.put(
    "/categories/{cat_id}", tags=["categories"], dependencies=[Depends(JWT_Bearer())]
)
async def update_category(
    cat_id: int, cat: CategoryBase, db: Session = Depends(con_db)
):
    return category.update_category(db, cat_id, cat)


@Routes.delete(
    "/categories/{cat_id}", tags=["categories"], dependencies=[Depends(JWT_Bearer())]
)
async def delete_category(cat_id: int, db: Session = Depends(con_db)):
    return category.delete_category(db, cat_id)


"""
Requirements Routes
"""


@Routes.get("/requirements/", tags=["requirements"])
async def get_requirements(db: Session = Depends(con_db)):
    return requirements.get_requirements(db)


@Routes.get("/requirements/{req_id}", tags=["requirements"])
async def get_requirement(req_id: int, db: Session = Depends(con_db)):
    return requirements.get_requirements(db, req_id)


@Routes.post(
    "/requirements/", tags=["requirements"], dependencies=[Depends(JWT_Bearer())]
)
async def create_requirement(req: RequirementBase, db: Session = Depends(con_db)):
    return requirements.create_requirement(db, req)


@Routes.put(
    "/requirements/{req_id}",
    tags=["requirements"],
    dependencies=[Depends(JWT_Bearer())],
)
async def update_requirement(
    req_id: int, req: RequirementBase, db: Session = Depends(con_db)
):
    return requirements.update_requirement(db, req_id, req)


@Routes.delete(
    "/requirements/{req_id}",
    tags=["requirements"],
    dependencies=[Depends(JWT_Bearer())],
)
async def delete_requirement(req_id: int, db: Session = Depends(con_db)):
    return requirements.delete_requirement(db, req_id)


"""
Announcement Routes
"""


@Routes.get("/announcements/", tags=["announcements"])
async def get_announcements(db: Session = Depends(con_db)):
    return announcement.get_announcements(db)


@Routes.get("/announcements/{ann_id}", tags=["announcements"])
async def get_announcement(ann_id: int, db: Session = Depends(con_db)):
    return announcement.get_announcements(db, ann_id)


@Routes.post(
    "/announcements/", tags=["announcements"], dependencies=[Depends(JWT_Bearer())]
)
async def create_announcement(ann: Announcement, db: Session = Depends(con_db)):
    return announcement.create_announcement(db, ann)


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
