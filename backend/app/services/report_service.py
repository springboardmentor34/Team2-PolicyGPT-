from sqlalchemy.orm import Session
from app.repositories.report_repository import get_all_reports

def get_all_reports_service(db: Session):
    return get_all_reports(db)
