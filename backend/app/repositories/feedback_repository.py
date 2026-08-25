from typing import Optional
from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

def create_feedback(db: Session, feedback: FeedbackCreate, user_id: Optional[int] = None, fallback_user_name: Optional[str] = None):
    raw_data = feedback.model_dump()
    
    # Extract message / content
    msg = raw_data.get("message") or raw_data.get("content") or ""
    cnt = raw_data.get("content") or msg
    sbj = raw_data.get("subject") or f"Feedback Rating: {raw_data.get('rating', 5)}/5"
    
    uname = raw_data.get("user_name")
    if not uname or uname == "Anonymous":
        if fallback_user_name:
            uname = fallback_user_name
        else:
            uname = "Anonymous"

    new_feedback = Feedback(
        user_name=uname,
        rating=raw_data.get("rating", 5),
        message=msg,
        subject=sbj,
        content=cnt,
        comments=msg,
        status="Open",
        user_id=user_id
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

def get_all_feedbacks(db: Session):
    return db.query(Feedback).order_by(Feedback.id.desc()).all()

def get_feedback_by_id(db: Session, feedback_id: int):
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()

def delete_feedback(db: Session, feedback_id: int) -> bool:
    item = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

