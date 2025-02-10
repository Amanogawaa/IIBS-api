from sqlalchemy.orm import Session
from api import models, schemas

def get_all_services(db: Session):
    return db.query(models.Service).all()

def create_service(db: Session, service: schemas.Service):
    db_service = models.Service(name=service.name, description=service.description)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service