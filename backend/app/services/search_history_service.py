from sqlalchemy.orm import Session
from app.repositories.search_history_repository import (
    create_search_history,
    get_all_search_history,
    delete_search_history,
)
from app.schemas.search_history import SearchHistoryCreate


def create_search_history_service(db: Session, search: SearchHistoryCreate):
    return create_search_history(db, search)


def get_all_search_history_service(db: Session, user_id: int | None = None):
    return get_all_search_history(db, user_id)


def delete_search_history_service(db: Session, search_id: int):
    return delete_search_history(db, search_id)
