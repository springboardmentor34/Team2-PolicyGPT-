from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    subject = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)
    comments = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
