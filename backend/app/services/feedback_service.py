from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.feedback_repository import create_feedback, get_all_feedbacks, delete_feedback, get_feedback_by_id
from app.schemas.feedback import FeedbackCreate

def create_feedback_service(db: Session, feedback: FeedbackCreate, user_id: Optional[int] = None, fallback_user_name: Optional[str] = None):
    return create_feedback(db, feedback, user_id=user_id, fallback_user_name=fallback_user_name)

def get_all_feedbacks_service(db: Session):
    return get_all_feedbacks(db)

def delete_feedback_service(db: Session, feedback_id: int) -> bool:
    return delete_feedback(db, feedback_id)

