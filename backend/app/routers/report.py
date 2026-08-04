from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.report import ReportResponse
from app.services.report_service import get_all_reports_service
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_reports_service(db)
