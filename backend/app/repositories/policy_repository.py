from sqlalchemy.orm import Session

from app.models.policy import Policy
from app.schemas.policy import PolicyCreate, PolicyUpdate


def create_policy(db: Session, policy: PolicyCreate):
    new_policy = Policy(**policy.model_dump())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy


def get_all_policies(db: Session):
    return db.query(Policy).all()


def get_policy_by_id(db: Session, policy_id: int):
    return db.query(Policy).filter(Policy.id == policy_id).first()


def update_policy(db: Session, policy_id: int, policy: PolicyUpdate):
    db_policy = get_policy_by_id(db, policy_id)

    if db_policy is None:
        return None

    update_data = policy.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_policy, key, value)

    db.commit()
    db.refresh(db_policy)

    return db_policy


def delete_policy(db: Session, policy_id: int):
    db_policy = get_policy_by_id(db, policy_id)

    if db_policy is None:
        return None

    db.delete(db_policy)
    db.commit()

    return db_policy