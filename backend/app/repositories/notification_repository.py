from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.notification import Notification

def get_all_notifications(db: Session):
    return db.query(Notification).order_by(desc(Notification.created_at)).all()

def get_notifications_by_user(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(desc(Notification.created_at)).all()

def get_unread_count(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).count()

def mark_notification_as_read(db: Session, notification_id: int, user_id: int):
    notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    return notification

def mark_all_as_read(db: Session, user_id: int):
    notifications = db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).all()
    for notif in notifications:
        notif.is_read = True
    db.commit()
    return len(notifications)

