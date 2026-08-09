from datetime import datetime
from pydantic import BaseModel


class ReportCreate(BaseModel):
    title: str
    report_type: str
    generated_by: int | None = None
    file_url: str | None = None
    summary: str | None = None


class ReportResponse(BaseModel):
    id: int
    title: str
    report_type: str
    generated_by: int | None = None
    file_url: str | None = None
    summary: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
