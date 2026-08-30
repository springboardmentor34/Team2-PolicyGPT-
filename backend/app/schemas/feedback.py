from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class FeedbackCreate(BaseModel):
    user_name: Optional[str] = Field(default="Anonymous", description="Name of the user submitting feedback")
    rating: Optional[int] = Field(default=5, ge=1, le=5, description="Rating from 1 to 5")
    message: Optional[str] = Field(default=None, description="Feedback message")
    
    # Optional fields for backward compatibility with existing API callers
    subject: Optional[str] = None
    content: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    user_name: Optional[str] = "Anonymous"
    rating: Optional[int] = 5
    message: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = "Open"
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

