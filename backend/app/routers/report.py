from typing import Optional
from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.report import ReportResponse, ReportSummaryResponse
from app.services.report_service import (
    get_all_reports_service,
    get_report_summary_service,
    generate_pdf_report_bytes,
    generate_excel_report_bytes
)

from app.auth.security import get_optional_current_user
from app.models.user import User

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/summary", response_model=ReportSummaryResponse)
def get_report_summary(
    format: Optional[str] = Query(None, description="Optional format: 'pdf', 'excel', or 'json'"),
    db: Session = Depends(get_db)
):
    """Fetch summary metrics across Schemes, Policies, and Feedback, or download PDF/Excel report."""
    if format:
        fmt = format.lower()
        if fmt == "pdf":
            return export_pdf_report(db=db)
        elif fmt in ["excel", "xlsx", "csv"]:
            return export_excel_report(db=db)

    return get_report_summary_service(db)

@router.get("/export/pdf")
def export_pdf_report(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Generate and download a PDF report containing Schemes, Policies, and Feedback data."""
    pdf_bytes = generate_pdf_report_bytes(db)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'inline; filename="PolicyGPT_System_Summary_Report.pdf"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@router.get("/export/excel")
def export_excel_report(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Generate and download an Excel/CSV spreadsheet report containing Schemes, Policies, and Feedback data."""
    excel_bytes = generate_excel_report_bytes(db)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="PolicyGPT_Analytics_Report.xlsx"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@router.get("/", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    """View stored historical reports list."""
    return get_all_reports_service(db)

