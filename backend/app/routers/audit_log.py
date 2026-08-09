from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.audit_log import AuditLogCreate, AuditLogResponse
from app.services.audit_log_service import (
    create_audit_log_service,
    get_all_audit_logs_service,
    get_audit_log_by_id_service,
)

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.post("/", response_model=AuditLogResponse)
def create_audit_log(audit_log: AuditLogCreate, db: Session = Depends(get_db)):
    return create_audit_log_service(db, audit_log)


@router.get("/", response_model=list[AuditLogResponse])
def get_all_audit_logs(user_id: int | None = None, db: Session = Depends(get_db)):
    return get_all_audit_logs_service(db, user_id=user_id)


@router.get("/{log_id}", response_model=AuditLogResponse)
def get_audit_log(log_id: int, db: Session = Depends(get_db)):
    log = get_audit_log_by_id_service(db, log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log
