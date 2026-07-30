from sqlalchemy.orm import Session

from app.repositories.scheme_repository import (
    create_scheme,
    get_all_schemes,
    get_scheme_by_id,
    update_scheme,
    delete_scheme,
)
from app.schemas.scheme import SchemeCreate, SchemeUpdate


def create_scheme_service(db: Session, scheme: SchemeCreate):
    return create_scheme(db, scheme)


def get_all_schemes_service(db: Session):
    return get_all_schemes(db)


def get_scheme_by_id_service(db: Session, scheme_id: int):
    return get_scheme_by_id(db, scheme_id)


def update_scheme_service(db: Session, scheme_id: int, scheme: SchemeUpdate):
    return update_scheme(db, scheme_id, scheme)


def delete_scheme_service(db: Session, scheme_id: int):
    return delete_scheme(db, scheme_id)