from sqlalchemy.orm import Session
from app.models.report import Report

def get_all_reports(db: Session):
    return db.query(Report).all()
