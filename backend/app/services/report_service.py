from sqlalchemy.orm import Session
from app.repositories.report_repository import (
    create_report,
    get_all_reports,
    get_report_by_id,
    delete_report,
)
from app.schemas.report import ReportCreate


def create_report_service(db: Session, report: ReportCreate):
    return create_report(db, report)


def get_all_reports_service(db: Session):
    return get_all_reports(db)


def get_report_by_id_service(db: Session, report_id: int):
    return get_report_by_id(db, report_id)


def delete_report_service(db: Session, report_id: int):
    return delete_report(db, report_id)
