from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    type: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UnreadCountResponse(BaseModel):
    unread_count: int

