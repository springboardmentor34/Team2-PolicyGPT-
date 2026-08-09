from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate


def create_feedback(db: Session, feedback: FeedbackCreate):
    new_fb = Feedback(**feedback.model_dump())
    db.add(new_fb)
    db.commit()
    db.refresh(new_fb)
    return new_fb


def get_all_feedback(db: Session):
    return db.query(Feedback).all()


def get_feedback_by_id(db: Session, feedback_id: int):
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()


def delete_feedback(db: Session, feedback_id: int):
    db_fb = get_feedback_by_id(db, feedback_id)
    if db_fb is None:
        return None
    db.delete(db_fb)
    db.commit()
    return db_fb
