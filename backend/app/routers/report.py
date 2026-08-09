from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.report import ReportCreate, ReportResponse
from app.services.report_service import (
    create_report_service,
    get_all_reports_service,
    get_report_by_id_service,
    delete_report_service,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/", response_model=ReportResponse)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    return create_report_service(db, report)


@router.get("/", response_model=list[ReportResponse])
def get_all_reports(db: Session = Depends(get_db)):
    return get_all_reports_service(db)


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    rep = get_report_by_id_service(db, report_id)
    if rep is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return rep


@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    deleted_rep = delete_report_service(db, report_id)
    if deleted_rep is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": "Report deleted successfully"}
