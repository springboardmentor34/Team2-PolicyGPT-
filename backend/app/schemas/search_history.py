from datetime import datetime
from pydantic import BaseModel


class SearchHistoryCreate(BaseModel):
    user_id: int | None = None
    query: str
    filters: str | None = None
    results_count: int | None = 0


class SearchHistoryResponse(BaseModel):
    id: int
    user_id: int | None = None
    query: str
    filters: str | None = None
    results_count: int
    created_at: datetime

    class Config:
        from_attributes = True
