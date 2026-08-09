from datetime import datetime
from pydantic import BaseModel


class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    type: str | None = "info"


class NotificationUpdate(BaseModel):
    title: str | None = None
    message: str | None = None
    type: str | None = None
    is_read: bool | None = None


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
