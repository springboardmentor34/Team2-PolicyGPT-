from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


def create_notification(db: Session, notification: NotificationCreate):
    new_notif = Notification(**notification.model_dump())
    db.add(new_notif)
    db.commit()
    db.refresh(new_notif)
    return new_notif


def get_all_notifications(db: Session, user_id: int | None = None):
    query = db.query(Notification)
    if user_id is not None:
        query = query.filter(Notification.user_id == user_id)
    return query.all()


def get_notification_by_id(db: Session, notif_id: int):
    return db.query(Notification).filter(Notification.id == notif_id).first()


def update_notification(db: Session, notif_id: int, notification: NotificationUpdate):
    db_notif = get_notification_by_id(db, notif_id)
    if db_notif is None:
        return None
    update_data = notification.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_notif, key, value)
    db.commit()
    db.refresh(db_notif)
    return db_notif


def delete_notification(db: Session, notif_id: int):
    db_notif = get_notification_by_id(db, notif_id)
    if db_notif is None:
        return None
    db.delete(db_notif)
    db.commit()
    return db_notif
