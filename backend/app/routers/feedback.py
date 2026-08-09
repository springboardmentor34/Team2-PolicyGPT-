from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import (
    create_feedback_service,
    get_all_feedback_service,
    get_feedback_by_id_service,
    delete_feedback_service,
)

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


@router.post("/", response_model=FeedbackResponse)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    return create_feedback_service(db, feedback)


@router.get("/", response_model=list[FeedbackResponse])
def get_all_feedback(db: Session = Depends(get_db)):
    return get_all_feedback_service(db)


@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    fb = get_feedback_by_id_service(db, feedback_id)
    if fb is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return fb


@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    deleted_fb = delete_feedback_service(db, feedback_id)
    if deleted_fb is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}
