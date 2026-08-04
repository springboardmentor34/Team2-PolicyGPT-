from datetime import datetime
from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    subject: str
    content: str

class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    content: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
