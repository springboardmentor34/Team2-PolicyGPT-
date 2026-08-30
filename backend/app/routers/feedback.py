from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import create_feedback_service, get_all_feedbacks_service, delete_feedback_service
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)

@router.post("", response_model=FeedbackResponse, status_code=201)
@router.post("/", response_model=FeedbackResponse, status_code=201)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    """Submit user feedback (user_name, rating, message)."""
    user_id = None
    user_name = None
    
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            from app.auth.security import decode_access_token
            payload = decode_access_token(token)
            if payload and "sub" in payload:
                user_email = payload.get("sub")
                user = db.query(User).filter(User.email == user_email).first()
                if user:
                    user_id = user.id
                    user_name = user.full_name or user.email
        except Exception:
            pass

    return create_feedback_service(
        db=db,
        feedback=feedback,
        user_id=user_id,
        fallback_user_name=user_name
    )

@router.get("", response_model=list[FeedbackResponse])
@router.get("/", response_model=list[FeedbackResponse])
def get_feedbacks(db: Session = Depends(get_db)):
    """View all submitted feedback."""
    return get_all_feedbacks_service(db)

@router.delete("/{feedback_id}", status_code=200)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """Delete a feedback entry by ID."""
    success = delete_feedback_service(db, feedback_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback with id {feedback_id} not found."
        )
    return {"message": f"Feedback with id {feedback_id} deleted successfully."}

