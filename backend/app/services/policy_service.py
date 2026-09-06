from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.policy_repository import (
    create_policy,
    get_all_policies,
    get_policy_by_id,
    update_policy,
    delete_policy,
)
from app.schemas.policy import PolicyCreate, PolicyUpdate
from app.models.policy import Policy
from app.models.audit_log import AuditLog


from app.models.notification import Notification
from app.models.user import User

def log_workflow_action(
    db: Session,
    user_id: int,
    policy_id: int,
    action: str,
    old_status: str | None,
    new_status: str,
    comment: str | None = None,
    creator_id: int | None = None
):
    audit_record = AuditLog(
        user_id=user_id,
        action=action,
        entity="policy",
        entity_id=policy_id,
        policy_id=policy_id,
        old_status=old_status,
        new_status=new_status,
        comment=comment
    )
    db.add(audit_record)

    # Determine whom to notify based on the action
    target_users = []
    
    if action == "POLICY_SUBMITTED":
        # Notify all administrators
        admins = db.query(User).filter(User.role == "administrator").all()
        target_users = [admin.id for admin in admins]
    elif action in ["POLICY_APPROVED", "POLICY_REJECTED", "POLICY_PUBLISHED"]:
        # Notify the creator
        if creator_id:
            target_users = [creator_id]
        
    action_label = action.replace("POLICY_", "").replace("_", " ").title()
    msg = f"Policy #{policy_id}: Action '{action_label}' status updated to {new_status}."
    if comment:
        msg += f" Note: {comment}"
        
    for target_user_id in target_users:
        if target_user_id != user_id:  # Do not notify themselves
            notif = Notification(
                user_id=target_user_id,
                message=msg,
                type=action
            )
            db.add(notif)
            
    db.commit()


def create_policy_service(db: Session, policy: PolicyCreate, user_id: int = None):
    # Enforce UPPERCASE status, defaulting to DRAFT
    status_str = (policy.status or "DRAFT").upper()
    if status_str not in ["DRAFT", "PENDING_APPROVAL", "APPROVED", "REJECTED", "PUBLISHED"]:
        status_str = "DRAFT"
    policy.status = status_str
    
    new_policy = create_policy(db, policy, user_id)
    
    # Audit log creation
    log_workflow_action(
        db=db,
        user_id=user_id,
        policy_id=new_policy.id,
        action="POLICY_CREATED",
        old_status=None,
        new_status=status_str
    )
    return new_policy


def get_all_policies_service(db: Session):
    return get_all_policies(db)


def get_policy_by_id_service(db: Session, policy_id: int):
    return get_policy_by_id(db, policy_id)


def update_policy_service(db: Session, policy_id: int, policy: PolicyUpdate, user_id: int = None):
    db_policy = get_policy_by_id(db, policy_id)
    if db_policy is None:
        return None

    # Strict transition: if attempting to change status, validate it.
    # If the policy is currently REJECTED and they modify it, transition it to DRAFT.
    update_data = policy.model_dump(exclude_unset=True)
    
    old_status = (db_policy.status or "DRAFT").upper()
    new_status = update_data.get("status")
    
    if new_status:
        new_status = new_status.upper()
        update_data["status"] = new_status
        
        # Validate status change if they try to change it directly
        if old_status != new_status:
            validate_transition(old_status, new_status)
    elif old_status == "REJECTED":
        # Automatically transition to DRAFT on edit if no status is specified
        update_data["status"] = "DRAFT"
        # Audit log transition
        log_workflow_action(
            db=db,
            user_id=user_id or db_policy.created_by,
            policy_id=policy_id,
            action="POLICY_REJECTED_TO_DRAFT",
            old_status="REJECTED",
            new_status="DRAFT",
            comment="Automatic transition back to DRAFT during update"
        )
    
    # Save updates
    for key, value in update_data.items():
        setattr(db_policy, key, value)
    
    db_policy.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_policy)
    return db_policy


def delete_policy_service(db: Session, policy_id: int):
    return delete_policy(db, policy_id)


def validate_transition(old_status: str, new_status: str):
    allowed = {
        "DRAFT": ["PENDING_APPROVAL"],
        "PENDING_APPROVAL": ["APPROVED", "REJECTED"],
        "APPROVED": ["PUBLISHED"],
        "REJECTED": ["DRAFT"]
    }
    
    if new_status not in allowed.get(old_status, []):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Status transition from {old_status} to {new_status} is not allowed."
        )


def submit_policy_service(db: Session, policy_id: int, user_id: int):
    policy = get_policy_by_id(db, policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
        
    if policy.created_by != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this policy")
        
    old_status = (policy.status or "DRAFT").upper()
    if old_status != "DRAFT":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Policy must be in DRAFT status to submit. Current status: {old_status}."
        )
        
    policy.status = "PENDING_APPROVAL"
    policy.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(policy)
    
    log_workflow_action(
        db=db,
        user_id=user_id,
        policy_id=policy_id,
        action="POLICY_SUBMITTED",
        old_status=old_status,
        new_status="PENDING_APPROVAL",
        creator_id=policy.created_by
    )
    return policy


def approve_policy_service(db: Session, policy_id: int, reviewer_id: int, comment: str | None = None):
    policy = get_policy_by_id(db, policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
        
    if policy.created_by == reviewer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Approver cannot be the creator of the policy"
        )
        
    old_status = (policy.status or "DRAFT").upper()
    if old_status != "PENDING_APPROVAL":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Policy must be in PENDING_APPROVAL status before it can be approved. Current status: {old_status}."
        )
        
    policy.status = "APPROVED"
    policy.reviewed_by = reviewer_id
    policy.reviewed_at = datetime.now(timezone.utc)
    policy.review_comment = comment
    policy.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(policy)
    
    log_workflow_action(
        db=db,
        user_id=reviewer_id,
        policy_id=policy_id,
        action="POLICY_APPROVED",
        old_status=old_status,
        new_status="APPROVED",
        comment=comment,
        creator_id=policy.created_by
    )
    return policy


def reject_policy_service(db: Session, policy_id: int, reviewer_id: int, comment: str):
    if not comment or not comment.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection comment must be required."
        )
        
    policy = get_policy_by_id(db, policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
        
    old_status = (policy.status or "DRAFT").upper()
    if old_status != "PENDING_APPROVAL":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Policy must be in PENDING_APPROVAL status to reject. Current status: {old_status}."
        )
        
    policy.status = "REJECTED"
    policy.reviewed_by = reviewer_id
    policy.reviewed_at = datetime.now(timezone.utc)
    policy.review_comment = comment
    policy.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(policy)
    
    log_workflow_action(
        db=db,
        user_id=reviewer_id,
        policy_id=policy_id,
        action="POLICY_REJECTED",
        old_status=old_status,
        new_status="REJECTED",
        comment=comment,
        creator_id=policy.created_by
    )
    return policy


def publish_policy_service(db: Session, policy_id: int, reviewer_id: int):
    policy = get_policy_by_id(db, policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
        
    old_status = (policy.status or "DRAFT").upper()
    if old_status != "APPROVED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Policy must be in APPROVED status before it can be published. Current status: {old_status}."
        )
        
    policy.status = "PUBLISHED"
    policy.published_at = datetime.now(timezone.utc)
    policy.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(policy)
    
    log_workflow_action(
        db=db,
        user_id=reviewer_id,
        policy_id=policy_id,
        action="POLICY_PUBLISHED",
        old_status=old_status,
        new_status="PUBLISHED",
        creator_id=policy.created_by
    )
    return policy


def get_pending_policies_service(db: Session):
    return db.query(Policy).filter(Policy.status == "PENDING_APPROVAL").all()


def get_published_policies_service(db: Session):
    return db.query(Policy).filter(Policy.status == "PUBLISHED").all()
