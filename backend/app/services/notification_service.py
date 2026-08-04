from sqlalchemy.orm import Session
from app.repositories.notification_repository import get_all_notifications

def get_all_notifications_service(db: Session):
    return get_all_notifications(db)
