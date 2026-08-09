from datetime import datetime
from pydantic import BaseModel


class AuditLogCreate(BaseModel):
    user_id: int | None = None
    action: str
    ip_address: str | None = None
    details: str | None = None


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None = None
    action: str
    ip_address: str | None = None
    details: str | None = None
    timestamp: datetime

    class Config:
        from_attributes = True
