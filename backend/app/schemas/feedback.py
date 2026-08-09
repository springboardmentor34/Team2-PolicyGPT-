from datetime import datetime
from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    user_id: int | None = None
    subject: str
    rating: int | None = None
    comments: str


class FeedbackResponse(BaseModel):
    id: int
    user_id: int | None = None
    subject: str
    rating: int | None = None
    comments: str
    created_at: datetime

    class Config:
        from_attributes = True
