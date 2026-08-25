from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.policy import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyApprovalRequest,
    PolicyRejectionRequest,
)
from app.services.policy_service import (
    create_policy_service,
    get_all_policies_service,
    get_policy_by_id_service,
    update_policy_service,
    delete_policy_service,
    submit_policy_service,
    approve_policy_service,
    reject_policy_service,
    publish_policy_service,
    get_pending_policies_service,
    get_published_policies_service,
)
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="",
    tags=["Policies"]
)


@router.post("", response_model=PolicyResponse)
@router.post("/", response_model=PolicyResponse)
def create_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "GOVERNMENT_OFFICIAL":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only government officials can create policies."
        )
    return create_policy_service(db, policy, current_user.id)


@router.get("", response_model=list[PolicyResponse])
@router.get("/", response_model=list[PolicyResponse])
def get_all_policies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.upper()
    if role == "ADMINISTRATOR":
        return get_all_policies_service(db)
    elif "OFFICIAL" in role:
        all_policies = get_all_policies_service(db)
        # Return policies created by this official OR any published policy
        return [p for p in all_policies if p.created_by == current_user.id or (p.status or "").upper() == "PUBLISHED"]
    else:
        # CITIZEN and others see all published policies
        return get_published_policies_service(db)


@router.get("/pending-approval", response_model=list[PolicyResponse])
@router.get("/pending-approval/", response_model=list[PolicyResponse])
def get_pending_policies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMINISTRATOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can view policies pending approval."
        )
    return get_pending_policies_service(db)


@router.get("/published", response_model=list[PolicyResponse])
@router.get("/published/", response_model=list[PolicyResponse])
def get_published_policies(
    db: Session = Depends(get_db),
):
    return get_published_policies_service(db)


@router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    policy = get_policy_by_id_service(db, policy_id)

    if policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")

    # Authorize access
    role = current_user.role.upper()
    if role == "CITIZEN" and (policy.status or "DRAFT").upper() != "PUBLISHED":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this policy")
    elif role == "GOVERNMENT_OFFICIAL" and policy.created_by != current_user.id and (policy.status or "DRAFT").upper() != "PUBLISHED":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this policy")

    return policy


@router.get("/{policy_id}/audit-logs")
def get_policy_audit_logs(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.models.audit_log import AuditLog
    policy = get_policy_by_id_service(db, policy_id)
    if policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")

    role = current_user.role.upper()
    if role == "CITIZEN" and (policy.status or "DRAFT").upper() != "PUBLISHED":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view these audit logs")
    elif role == "GOVERNMENT_OFFICIAL" and policy.created_by != current_user.id and (policy.status or "DRAFT").upper() != "PUBLISHED":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this policy")

    logs = db.query(AuditLog).filter(AuditLog.policy_id == policy_id).order_by(AuditLog.timestamp.asc()).all()
    
    results = []
    for log in logs:
        results.append({
            "id": log.id,
            "action": log.action,
            "old_status": log.old_status,
            "new_status": log.new_status,
            "comment": log.comment,
            "timestamp": log.timestamp,
            "user_name": log.user.full_name if log.user else "System",
            "user_email": log.user.email if log.user else ""
        })
    return results


@router.put("/{policy_id}", response_model=PolicyResponse)
def update_policy(
    policy_id: int,
    policy: PolicyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_policy = get_policy_by_id_service(db, policy_id)
    if db_policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")

    # Only creator can update, and status must be DRAFT or REJECTED
    role = current_user.role.upper()
    if role != "ADMINISTRATOR":
        if db_policy.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this policy."
            )
        status_str = (db_policy.status or "DRAFT").upper()
        if status_str not in ["DRAFT", "REJECTED"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot edit policy that is in {status_str} status."
            )

    updated_policy = update_policy_service(db, policy_id, policy, current_user.id)
    return updated_policy


@router.delete("/{policy_id}")
def delete_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_policy = get_policy_by_id_service(db, policy_id)
    if db_policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")

    role = current_user.role.upper()
    if role != "ADMINISTRATOR" and db_policy.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this policy."
        )

    deleted_policy = delete_policy_service(db, policy_id)
    return {"message": "Policy deleted successfully"}


@router.post("/{policy_id}/submit", response_model=PolicyResponse)
def submit_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "GOVERNMENT_OFFICIAL":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only government officials can submit policies for approval."
        )
    return submit_policy_service(db, policy_id, current_user.id)


@router.post("/{policy_id}/approve", response_model=PolicyResponse)
def approve_policy(
    policy_id: int,
    req: PolicyApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMINISTRATOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can approve policies."
        )
    return approve_policy_service(db, policy_id, current_user.id, req.comment)


@router.post("/{policy_id}/reject", response_model=PolicyResponse)
def reject_policy(
    policy_id: int,
    req: PolicyRejectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMINISTRATOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can reject policies."
        )
    return reject_policy_service(db, policy_id, current_user.id, req.comment)


@router.post("/{policy_id}/publish", response_model=PolicyResponse)
def publish_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.upper() != "ADMINISTRATOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can publish policies."
        )
    return publish_policy_service(db, policy_id, current_user.id)
