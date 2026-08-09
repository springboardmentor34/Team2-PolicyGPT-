from sqlalchemy.orm import Session
from app.repositories.feedback_repository import (
    create_feedback,
    get_all_feedback,
    get_feedback_by_id,
    delete_feedback,
)
from app.schemas.feedback import FeedbackCreate


def create_feedback_service(db: Session, feedback: FeedbackCreate):
    return create_feedback(db, feedback)


def get_all_feedback_service(db: Session):
    return get_all_feedback(db)


def get_feedback_by_id_service(db: Session, feedback_id: int):
    return get_feedback_by_id(db, feedback_id)


def delete_feedback_service(db: Session, feedback_id: int):
    return delete_feedback(db, feedback_id)
