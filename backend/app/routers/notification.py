from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.notification import NotificationResponse
from app.services.notification_service import get_all_notifications_service
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/", response_model=list[NotificationResponse])
def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_notifications_service(db)
