from datetime import datetime
from pydantic import BaseModel


# Schema for creating a new policy
class PolicyCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    department: str | None = None
    state: str | None = None
    status: str | None = "Draft"


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
    created_by: int | None = None
    reviewed_by: int | None = None
    review_comment: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    reviewed_at: datetime | None = None
    published_at: datetime | None = None

    class Config:
        from_attributes = True


class PolicyApprovalRequest(BaseModel):
    comment: str | None = None


class PolicyRejectionRequest(BaseModel):
    comment: str


class PolicyStatusResponse(BaseModel):
    policy_id: int
    old_status: str | None
    new_status: str
    message: str
