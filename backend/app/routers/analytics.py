from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsOverviewResponse
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
    if current_user.role not in ["administrator", "official"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to access analytics."
        )
        
    try:
        report = AnalyticsService.get_overview_analytics(db)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load analytics: {str(e)}")

