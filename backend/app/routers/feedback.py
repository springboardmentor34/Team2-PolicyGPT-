from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import create_feedback_service, get_all_feedbacks_service
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)

@router.post("/", response_model=FeedbackResponse, status_code=201)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_feedback_service(db, feedback, current_user.id)

@router.get("/", response_model=list[FeedbackResponse])
def get_feedbacks(db: Session = Depends(get_db)):
    return get_all_feedbacks_service(db)
