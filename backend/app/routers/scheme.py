from fastapi import APIRouter, Depends, HTTPException, status
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
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="",
    tags=["Schemes"]
)

def verify_scheme_manager(current_user: User = Depends(get_current_user)):
    role = (current_user.role or "").lower()
    if role not in ["government_official", "administrator", "official"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Government Officials and Administrators are authorized to create, edit, or delete schemes."
        )
    return current_user


@router.post("", response_model=SchemeResponse)
@router.post("/", response_model=SchemeResponse)
def create_scheme(
    scheme: SchemeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_scheme_manager)
):
    return create_scheme_service(db, scheme)


@router.get("", response_model=list[SchemeResponse])
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
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_scheme_manager)
):
    updated_scheme = update_scheme_service(db, scheme_id, scheme)

    if updated_scheme is None:
        raise HTTPException(status_code=404, detail="Scheme not found")

    return updated_scheme


@router.delete("/{scheme_id}")
def delete_scheme(
    scheme_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_scheme_manager)
):
    deleted_scheme = delete_scheme_service(db, scheme_id)

    if deleted_scheme is None:
        raise HTTPException(status_code=404, detail="Scheme not found")

    return {"message": "Scheme deleted successfully"}