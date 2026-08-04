from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String, index=True)
    generated_by = Column(String)
    file_path = Column(String)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
