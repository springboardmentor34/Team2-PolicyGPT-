from sqlalchemy.orm import Session

from app.models.scheme import Scheme
from app.schemas.scheme import SchemeCreate, SchemeUpdate


def create_scheme(db: Session, scheme: SchemeCreate):
    db_scheme = Scheme(**scheme.model_dump())
    db.add(db_scheme)
    db.commit()
    db.refresh(db_scheme)
    return db_scheme


def get_all_schemes(db: Session):
    return db.query(Scheme).all()


def get_scheme_by_id(db: Session, scheme_id: int):
    return db.query(Scheme).filter(Scheme.id == scheme_id).first()


def update_scheme(db: Session, scheme_id: int, scheme: SchemeUpdate):
    db_scheme = get_scheme_by_id(db, scheme_id)

    if db_scheme is None:
        return None

    update_data = scheme.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_scheme, key, value)

    db.commit()
    db.refresh(db_scheme)

    return db_scheme


def delete_scheme(db: Session, scheme_id: int):
    db_scheme = get_scheme_by_id(db, scheme_id)

    if db_scheme is None:
        return None

    db.delete(db_scheme)
    db.commit()

    return db_scheme