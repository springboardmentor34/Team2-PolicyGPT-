from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ReportResponse(BaseModel):
    id: int
    title: Optional[str] = "System Analytics Report"
    report_type: Optional[str] = "PDF"
    generated_by: Optional[Any] = "System"
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    content: Optional[str] = "PolicyGPT Analytics & Intelligence Report"
    summary: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReportSummaryResponse(BaseModel):
    timestamp: datetime
    total_policies: int
    published_policies: int
    draft_policies: int
    pending_policies: int
    rejected_policies: int
    total_schemes: int
    active_schemes: int
    total_feedback: int
    average_rating: float
    policies_by_category: Dict[str, int]
    schemes_by_category: Dict[str, int]
    recent_feedback: List[Dict[str, Any]]

