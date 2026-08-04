from sqlalchemy.orm import Session
from app.repositories.feedback_repository import create_feedback, get_all_feedbacks
from app.schemas.feedback import FeedbackCreate

def create_feedback_service(db: Session, feedback: FeedbackCreate, user_id: int):
    return create_feedback(db, feedback, user_id)

def get_all_feedbacks_service(db: Session):
    return get_all_feedbacks(db)
