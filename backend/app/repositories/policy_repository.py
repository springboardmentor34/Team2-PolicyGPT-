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


def search_policies(
    db: Session,
    keyword: str | None = None,
    category: str | None = None,
    state: str | None = None,
    status: str | None = None
):
    from sqlalchemy import or_

    query = db.query(Policy)

    if keyword:
        search = f"%{keyword}%"
        query = query.filter(
            or_(
                Policy.title.ilike(search),
                Policy.description.ilike(search),
                Policy.category.ilike(search),
                Policy.department.ilike(search),
                Policy.state.ilike(search),
                Policy.status.ilike(search)
            )
        )

    if category and category != "All":
        query = query.filter(Policy.category.ilike(category))

    if state and state != "All":
        query = query.filter(Policy.state.ilike(state))

    if status and status != "All":
        query = query.filter(Policy.status.ilike(status))

    return query.all()