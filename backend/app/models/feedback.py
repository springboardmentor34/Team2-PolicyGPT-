from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=True)
    rating = Column(Integer, default=5, nullable=True)
    message = Column(Text, nullable=True)

    # Optional fields for backward compatibility
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    subject = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    status = Column(String, default="Open", nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="feedback")

