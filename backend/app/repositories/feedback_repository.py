from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

def create_feedback(db: Session, feedback: FeedbackCreate, user_id: int):
    new_feedback = Feedback(**feedback.model_dump(), user_id=user_id)
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

def get_all_feedbacks(db: Session):
    return db.query(Feedback).all()
