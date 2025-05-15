import os
from sqlalchemy.orm import Session
from api import models
from fastapi import HTTPException
from typing import Union, Optional

# modules
from api.schema.feedback import *
from api.schema.response import ResponseModel
from api.validator import ProfanityFilter, is_meaningful_text
import logging

_profanity_filter = ProfanityFilter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_feedback(db: Session, feed_id: Optional[int | None] = None):
    query = db.query(models.Feedback)

    if feed_id:
        query = query.filter(models.Feedback.id ==  feed_id)

    reqs = query.all()

    if not reqs:
        raise HTTPException(status_code=404, detail="No Feedback found")

    reqs_response = [FeedbackResponse.model_validate(req, from_attributes=True) for req in reqs]

    return ResponseModel(
        message="Requirements fetched successfully", data=reqs_response, status_code=200
    )

def create_feedback(
    db: Session, feedback: Feedback, announcement_id: Optional[int] = None, service_id: Optional[int] = None
):
    
    if feedback.comment:
        # Trim whitespace
        sanitized_comment = feedback.comment.strip()
        
        # Advanced profanity check - test the raw comment
        if _profanity_filter.contains_profanity(sanitized_comment):
            # Log the rejected comment for review
            logger.warning(f"Profanity detected in feedback: {sanitized_comment}")
            raise HTTPException(
                status_code=400,
                detail="Comment contains inappropriate language"
            )
        
        # Check if comment is meaningful with our enhanced validation
        if not is_meaningful_text(sanitized_comment):
            logger.info(f"Non-meaningful comment rejected: {sanitized_comment}")
            raise HTTPException(
                status_code=400,
                detail="Comment must be meaningful (at least 3 words, contain letters, and avoid excessive punctuation or profanity)"
            )
        
        # Update the feedback comment with sanitized version
        feedback.comment = sanitized_comment

    # Validate rating is within acceptable range
    if not (1 <= feedback.rating <= 5):
        raise HTTPException(
            status_code=400, 
            detail="Rating must be between 1 and 5"
        )
    
    if announcement_id and service_id:
        raise HTTPException(
            status_code=400, detail="Feedback cannot be tied to both an announcement and a service"
        )

    db_feedback = models.Feedback(
        rating=feedback.rating,
        comment=feedback.comment,
        announcement_id=announcement_id,
        service_id=service_id,
    )

    db.add(db_feedback)
    try:
        db.commit()
        db.refresh(db_feedback)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create feedback: {str(e)}")

    feedback_response = Feedback.model_validate(db_feedback, from_attributes=True)

    return ResponseModel(
        message="Feedback created successfully",
        data=feedback_response,
        status_code=201
    )