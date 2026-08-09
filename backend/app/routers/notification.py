from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
)
from app.services.notification_service import (
    create_notification_service,
    get_all_notifications_service,
    get_notification_by_id_service,
    update_notification_service,
    delete_notification_service,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    return create_notification_service(db, notification)


@router.get("/", response_model=list[NotificationResponse])
def get_all_notifications(user_id: int | None = None, db: Session = Depends(get_db)):
    return get_all_notifications_service(db, user_id=user_id)


@router.get("/{notif_id}", response_model=NotificationResponse)
def get_notification(notif_id: int, db: Session = Depends(get_db)):
    notif = get_notification_by_id_service(db, notif_id)
    if notif is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notif


@router.put("/{notif_id}", response_model=NotificationResponse)
def update_notification(
    notif_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db)
):
    updated_notif = update_notification_service(db, notif_id, notification)
    if updated_notif is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notif


@router.delete("/{notif_id}")
def delete_notification(notif_id: int, db: Session = Depends(get_db)):
    deleted_notif = delete_notification_service(db, notif_id)
    if deleted_notif is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted successfully"}
