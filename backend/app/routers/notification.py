from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.notification import NotificationResponse, UnreadCountResponse
from app.services.notification_service import (
    get_user_notifications_service,
    get_unread_notification_count_service,
    mark_notification_read_service,
    mark_all_notifications_read_service
)
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/", response_model=list[NotificationResponse])
def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_notifications_service(db, current_user.id)

@router.get("/unread-count", response_model=UnreadCountResponse)
def get_unread_count(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    count = get_unread_notification_count_service(db, current_user.id)
    return {"unread_count": count}

@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notif = mark_notification_read_service(db, notification_id, current_user.id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notif

@router.put("/read-all")
def mark_all_read(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_count = mark_all_notifications_read_service(db, current_user.id)
    return {"message": f"Marked {updated_count} notifications as read", "updated_count": updated_count}

