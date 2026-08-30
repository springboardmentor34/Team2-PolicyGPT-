from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database.base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    report_type = Column(String, index=True, nullable=True)
    generated_by = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    file_url = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

