from sqlalchemy.orm import Session

from app.repositories.policy_repository import (
    create_policy,
    get_all_policies,
    get_policy_by_id,
    update_policy,
    delete_policy,
)
from app.schemas.policy import PolicyCreate, PolicyUpdate


def create_policy_service(db: Session, policy: PolicyCreate):
    return create_policy(db, policy)


def get_all_policies_service(db: Session):
    return get_all_policies(db)


def get_policy_by_id_service(db: Session, policy_id: int):
    return get_policy_by_id(db, policy_id)


def update_policy_service(db: Session, policy_id: int, policy: PolicyUpdate):
    return update_policy(db, policy_id, policy)


def delete_policy_service(db: Session, policy_id: int):
    return delete_policy(db, policy_id)