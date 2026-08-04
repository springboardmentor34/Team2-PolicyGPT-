from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"))
    parameter = Column(String, index=True)
    operator = Column(String)
    value = Column(String)

    scheme = relationship("Scheme", back_populates="eligibility_rules")
