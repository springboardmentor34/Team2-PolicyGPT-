from sqlalchemy.orm import Session
from app.models.notification import Notification

def get_all_notifications(db: Session):
    return db.query(Notification).all()
