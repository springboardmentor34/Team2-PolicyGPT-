from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.search_history import SearchHistoryCreate, SearchHistoryResponse
from app.services.search_history_service import (
    create_search_history_service,
    get_all_search_history_service,
    delete_search_history_service,
)

router = APIRouter(
    prefix="/search-history",
    tags=["Search History"]
)


@router.post("/", response_model=SearchHistoryResponse)
def create_search_history(search: SearchHistoryCreate, db: Session = Depends(get_db)):
    return create_search_history_service(db, search)


@router.get("/", response_model=list[SearchHistoryResponse])
def get_all_search_history(user_id: int | None = None, db: Session = Depends(get_db)):
    return get_all_search_history_service(db, user_id=user_id)


@router.delete("/{search_id}")
def delete_search_history(search_id: int, db: Session = Depends(get_db)):
    deleted_search = delete_search_history_service(db, search_id)
    if deleted_search is None:
        raise HTTPException(status_code=404, detail="Search history entry not found")
    return {"message": "Search history deleted successfully"}
