from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate


def create_audit_log(db: Session, audit_log: AuditLogCreate):
    new_log = AuditLog(**audit_log.model_dump())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


def get_all_audit_logs(db: Session, user_id: int | None = None):
    query = db.query(AuditLog)
    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)
    return query.all()


def get_audit_log_by_id(db: Session, log_id: int):
    return db.query(AuditLog).filter(AuditLog.id == log_id).first()
