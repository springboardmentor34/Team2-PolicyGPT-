from datetime import datetime
from pydantic import BaseModel


class EligibilityRuleCreate(BaseModel):
    rule_name: str
    scheme_id: int | None = None
    policy_id: int | None = None
    min_age: int | None = None
    max_age: int | None = None
    min_income: float | None = None
    max_income: float | None = None
    occupation: str | None = None
    gender: str | None = None
    state: str | None = None
    description: str | None = None


class EligibilityRuleUpdate(BaseModel):
    rule_name: str | None = None
    scheme_id: int | None = None
    policy_id: int | None = None
    min_age: int | None = None
    max_age: int | None = None
    min_income: float | None = None
    max_income: float | None = None
    occupation: str | None = None
    gender: str | None = None
    state: str | None = None
    description: str | None = None


class EligibilityRuleResponse(BaseModel):
    id: int
    rule_name: str
    scheme_id: int | None = None
    policy_id: int | None = None
    min_age: int | None = None
    max_age: int | None = None
    min_income: float | None = None
    max_income: float | None = None
    occupation: str | None = None
    gender: str | None = None
    state: str | None = None
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
