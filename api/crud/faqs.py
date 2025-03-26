from sqlalchemy.orm import Session
from api import models
from fastapi import HTTPException
from typing import Union, Optional

# modules
from api.schema.faqs import *
from api.schema.response import ResponseModel

def get_all_faqs(db: Session, faqs_id: Optional[int | None] = None):
    query = db.query(models.Faq)

    if faqs_id:
        query = query.filter(models.Faq.id == faqs_id)

    reqs = query.all()

    if not reqs:
        raise HTTPException(status_code=404, detail="No FAQS found")

    reqs_response = [Faq.model_validate(req, from_attributes=True) for req in reqs]

    return ResponseModel(
        message="Requirements fetched successfully", data=reqs_response, status_code=200
    )

def create_faq(db: Session, data: FaqCreate):
    query = db.query(models.Faq).filter(models.Faq.question == data.question).first()

    if query:
        raise HTTPException(status_code=400, detail="FAQ already exists")

    faq = models.Faq(
        question=data.question, answer=data.answer, service_id=data.service_id
    )

    db.add(faq)
    db.commit()
    db.refresh(faq)

    return ResponseModel(
        message="FAQ Created Successfully",
        status_code=200,
    )

def update_faq(db: Session, faq_id: int, data: FaqCreate):
    query = db.query(models.Faq).filter(models.Faq.id == faq_id).first()

    if not query:
        raise HTTPException(status_code=404, detail="FAQ not found")

    if data.question is not None:
        query.question = data.question
    if data.answer is not None:        
        query.answer = data.answer
    if data.service_id is not None:        
        query.service_id = data.service_id

    db.commit()
    db.refresh(query)

    return ResponseModel(
        message="FAQ Updated Successfully",
        status_code=200,
    )

def delete_faq(db: Session, faq_id: int):
    query = db.query(models.Faq).filter(models.Faq.id == faq_id).first()

    if not query:
        raise HTTPException(status_code=404, detail="FAQ not found")

    db.delete(query)
    db.commit()

    return ResponseModel(message="FAQ Deleted Successfully", data=None, status_code=200)
