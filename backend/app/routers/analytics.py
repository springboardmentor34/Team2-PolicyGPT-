from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsOverviewResponse, DepartmentAnalyticsResponse
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview", response_model=AnalyticsOverviewResponse)
def get_analytics_overview(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive analytics and usage statistics metrics.
    Restricted to Administrator and Official roles.
    """
    if current_user.role not in ["administrator", "government_official"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to access analytics."
        )
        
    try:
        report = AnalyticsService.get_overview_analytics(db)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load analytics: {str(e)}")

@router.get("/departments", response_model=list[str])
def get_departments(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["administrator", "government_official"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return AnalyticsService.get_departments_service(db)

@router.get("/department/{department_name}", response_model=DepartmentAnalyticsResponse)
def get_department_analytics(
    department_name: str,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["administrator", "government_official"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        return AnalyticsService.get_department_analytics_service(db, department_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load department analytics: {str(e)}")

from pydantic import BaseModel

class SearchLogRequest(BaseModel):
    query: str
    filters: str = ""

class EligibilityLogRequest(BaseModel):
    entity_id: int = 0

@router.post("/log-search", status_code=status.HTTP_201_CREATED)
def log_search(
    request: SearchLogRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.search_history import SearchHistory
    new_search = SearchHistory(
        user_id=current_user.id,
        query=request.query,
        filters=request.filters
    )
    db.add(new_search)
    db.commit()
    return {"message": "Logged search successfully"}

@router.post("/log-eligibility", status_code=status.HTTP_201_CREATED)
def log_eligibility(
    request: EligibilityLogRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.audit_log import AuditLog
    new_log = AuditLog(
        user_id=current_user.id,
        action="eligibility_check",
        entity="scheme",
        entity_id=request.entity_id,
        comment="User performed eligibility check"
    )
    db.add(new_log)
    db.commit()
    return {"message": "Logged eligibility check"}

@router.post("/log-comparison", status_code=status.HTTP_201_CREATED)
def log_comparison(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.audit_log import AuditLog
    new_log = AuditLog(
        user_id=current_user.id,
        action="policy_comparison",
        entity="policy",
        entity_id=0,
        comment="User compared policies"
    )
    db.add(new_log)
    db.commit()
    return {"message": "Logged comparison"}
