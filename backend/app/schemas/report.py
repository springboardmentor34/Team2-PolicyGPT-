from datetime import datetime
from pydantic import BaseModel

class ReportResponse(BaseModel):
    id: int
    title: str
    content: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
