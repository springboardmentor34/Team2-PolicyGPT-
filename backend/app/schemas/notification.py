from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import Optional

class NotificationResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    message: Optional[str] = None
    type: Optional[str] = None
    is_read: Optional[bool] = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UnreadCountResponse(BaseModel):
    unread_count: int
