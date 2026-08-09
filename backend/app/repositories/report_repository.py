from sqlalchemy.orm import Session
from app.models.report import Report
from app.schemas.report import ReportCreate


def create_report(db: Session, report: ReportCreate):
    new_report = Report(**report.model_dump())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


def get_all_reports(db: Session):
    return db.query(Report).all()


def get_report_by_id(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()


def delete_report(db: Session, report_id: int):
    db_report = get_report_by_id(db, report_id)
    if db_report is None:
        return None
    db.delete(db_report)
    db.commit()
    return db_report
