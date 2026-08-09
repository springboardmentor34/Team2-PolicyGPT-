from sqlalchemy.orm import Session
from app.repositories.audit_log_repository import (
    create_audit_log,
    get_all_audit_logs,
    get_audit_log_by_id,
)
from app.schemas.audit_log import AuditLogCreate


def create_audit_log_service(db: Session, audit_log: AuditLogCreate):
    return create_audit_log(db, audit_log)


def get_all_audit_logs_service(db: Session, user_id: int | None = None):
    return get_all_audit_logs(db, user_id)


def get_audit_log_by_id_service(db: Session, log_id: int):
    return get_audit_log_by_id(db, log_id)
