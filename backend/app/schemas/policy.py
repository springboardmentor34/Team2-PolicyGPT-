from datetime import datetime
from pydantic import BaseModel


# Schema for creating a new policy
class PolicyCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    department: str | None = None
    state: str | None = None
    status: str | None = None


# Schema for updating a policy
class PolicyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    department: str | None = None
    state: str | None = None
    status: str | None = None


# Schema for returning policy data
class PolicyResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    category: str | None = None
    department: str | None = None
    state: str | None = None
    status: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True