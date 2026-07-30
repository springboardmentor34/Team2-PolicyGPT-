from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database.database import Base


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    department = Column(String, nullable=True)
    state = Column(String, nullable=True)
    status = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))