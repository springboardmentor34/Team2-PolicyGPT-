from sqlalchemy.orm import Session
from app.models.search_history import SearchHistory
from app.schemas.search_history import SearchHistoryCreate


def create_search_history(db: Session, search: SearchHistoryCreate):
    new_search = SearchHistory(**search.model_dump())
    db.add(new_search)
    db.commit()
    db.refresh(new_search)
    return new_search


def get_all_search_history(db: Session, user_id: int | None = None):
    query = db.query(SearchHistory)
    if user_id is not None:
        query = query.filter(SearchHistory.user_id == user_id)
    return query.all()


def delete_search_history(db: Session, search_id: int):
    db_search = db.query(SearchHistory).filter(SearchHistory.id == search_id).first()
    if db_search is None:
        return None
    db.delete(db_search)
    db.commit()
    return db_search
