from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.scheme import SchemeCreate, SchemeUpdate, SchemeResponse
from app.services.scheme_service import (
    create_scheme_service,
    get_all_schemes_service,
    get_scheme_by_id_service,
    update_scheme_service,
    delete_scheme_service,
)

router = APIRouter(
    prefix="/schemes",
    tags=["Schemes"]
)


@router.post("/", response_model=SchemeResponse)
def create_scheme(scheme: SchemeCreate, db: Session = Depends(get_db)):
    return create_scheme_service(db, scheme)


@router.get("/", response_model=list[SchemeResponse])
def get_all_schemes(db: Session = Depends(get_db)):
    return get_all_schemes_service(db)


@router.get("/{scheme_id}", response_model=SchemeResponse)
def get_scheme(scheme_id: int, db: Session = Depends(get_db)):
    scheme = get_scheme_by_id_service(db, scheme_id)

    if scheme is None:
        raise HTTPException(status_code=404, detail="Scheme not found")

    return scheme


@router.put("/{scheme_id}", response_model=SchemeResponse)
def update_scheme(
    scheme_id: int,
    scheme: SchemeUpdate,
    db: Session = Depends(get_db)
):
    updated_scheme = update_scheme_service(db, scheme_id, scheme)

    if updated_scheme is None:
        raise HTTPException(status_code=404, detail="Scheme not found")

    return updated_scheme


@router.delete("/{scheme_id}")
def delete_scheme(scheme_id: int, db: Session = Depends(get_db)):
    deleted_scheme = delete_scheme_service(db, scheme_id)

    if deleted_scheme is None:
        raise HTTPException(status_code=404, detail="Scheme not found")

    return {"message": "Scheme deleted successfully"}