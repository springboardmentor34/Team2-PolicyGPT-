from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")

    notifications = relationship("Notification", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    search_history = relationship("SearchHistory", back_populates="user")