from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from app.database.database import Base


class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True)
    rule_name = Column(String, nullable=False)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    min_income = Column(Float, nullable=True)
    max_income = Column(Float, nullable=True)
    occupation = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    state = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
