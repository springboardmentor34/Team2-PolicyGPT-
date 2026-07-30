from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyResponse
from app.services.policy_service import (
    create_policy_service,
    get_all_policies_service,
    get_policy_by_id_service,
    update_policy_service,
    delete_policy_service,
)

router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)


@router.post("/", response_model=PolicyResponse)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    return create_policy_service(db, policy)


@router.get("/", response_model=list[PolicyResponse])
def get_all_policies(db: Session = Depends(get_db)):
    return get_all_policies_service(db)


@router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = get_policy_by_id_service(db, policy_id)

    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    return policy


@router.put("/{policy_id}", response_model=PolicyResponse)
def update_policy(
    policy_id: int,
    policy: PolicyUpdate,
    db: Session = Depends(get_db)
):
    updated_policy = update_policy_service(db, policy_id, policy)

    if updated_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    return updated_policy


@router.delete("/{policy_id}")
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    deleted_policy = delete_policy_service(db, policy_id)

    if deleted_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    return {"message": "Policy deleted successfully"}