from sqlalchemy.orm import Session
from app.repositories.notification_repository import (
    create_notification,
    get_all_notifications,
    get_notification_by_id,
    update_notification,
    delete_notification,
)
from app.schemas.notification import NotificationCreate, NotificationUpdate


def create_notification_service(db: Session, notification: NotificationCreate):
    return create_notification(db, notification)


def get_all_notifications_service(db: Session, user_id: int | None = None):
    return get_all_notifications(db, user_id)


def get_notification_by_id_service(db: Session, notif_id: int):
    return get_notification_by_id(db, notif_id)


def update_notification_service(db: Session, notif_id: int, notification: NotificationUpdate):
    return update_notification(db, notif_id, notification)


def delete_notification_service(db: Session, notif_id: int):
    return delete_notification(db, notif_id)
