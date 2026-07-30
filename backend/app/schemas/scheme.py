from datetime import datetime
from pydantic import BaseModel


class SchemeCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    department: str | None = None
    state: str | None = None
    status: str | None = None


class SchemeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    department: str | None = None
    state: str | None = None
    status: str | None = None


class SchemeResponse(BaseModel):
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