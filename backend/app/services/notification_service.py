from sqlalchemy.orm import Session
from app.repositories.notification_repository import (
    get_all_notifications,
    get_notifications_by_user,
    get_unread_count,
    mark_notification_as_read,
    mark_all_as_read
)

def get_all_notifications_service(db: Session):
    return get_all_notifications(db)

def get_user_notifications_service(db: Session, user_id: int):
    return get_notifications_by_user(db, user_id)

def get_unread_notification_count_service(db: Session, user_id: int):
    return get_unread_count(db, user_id)

def mark_notification_read_service(db: Session, notification_id: int, user_id: int):
    return mark_notification_as_read(db, notification_id, user_id)

def mark_all_notifications_read_service(db: Session, user_id: int):
    return mark_all_as_read(db, user_id)

