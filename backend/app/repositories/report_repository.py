from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.report import Report
from app.models.policy import Policy
from app.models.scheme import Scheme
from app.models.feedback import Feedback

def get_all_reports(db: Session):
    return db.query(Report).all()

def get_report_summary_data(db: Session):
    # Policy counts
    total_policies = db.query(Policy).count()
    published_policies = db.query(Policy).filter(Policy.status == "PUBLISHED").count()
    draft_policies = db.query(Policy).filter(Policy.status == "DRAFT").count()
    pending_policies = db.query(Policy).filter(Policy.status == "PENDING_APPROVAL").count()
    rejected_policies = db.query(Policy).filter(Policy.status == "REJECTED").count()

    # Policies by category
    policy_cat_counts = {}
    p_cats = db.query(Policy.category, func.count(Policy.id)).group_by(Policy.category).all()
    for cat, count in p_cats:
        policy_cat_counts[cat or "Uncategorized"] = count

    # Scheme counts
    total_schemes = db.query(Scheme).count()
    active_schemes = db.query(Scheme).filter(Scheme.status == "Active").count()

    # Schemes by category
    scheme_cat_counts = {}
    s_cats = db.query(Scheme.category, func.count(Scheme.id)).group_by(Scheme.category).all()
    for cat, count in s_cats:
        scheme_cat_counts[cat or "Uncategorized"] = count

    # Feedback counts & rating
    total_feedback = db.query(Feedback).count()
    avg_rating_res = db.query(func.avg(Feedback.rating)).scalar()
    avg_rating = round(float(avg_rating_res), 2) if avg_rating_res is not None else 5.0

    recent_fb = db.query(Feedback).order_by(Feedback.id.desc()).limit(10).all()
    recent_fb_list = []
    for fb in recent_fb:
        recent_fb_list.append({
            "id": fb.id,
            "user_name": fb.user_name or "Anonymous",
            "rating": fb.rating or 5,
            "message": fb.message or fb.content or "",
            "created_at": fb.created_at.isoformat() if fb.created_at else None
        })

    return {
        "timestamp": datetime.now(timezone.utc),
        "total_policies": total_policies,
        "published_policies": published_policies,
        "draft_policies": draft_policies,
        "pending_policies": pending_policies,
        "rejected_policies": rejected_policies,
        "total_schemes": total_schemes,
        "active_schemes": active_schemes,
        "total_feedback": total_feedback,
        "average_rating": avg_rating,
        "policies_by_category": policy_cat_counts,
        "schemes_by_category": scheme_cat_counts,
        "recent_feedback": recent_fb_list
    }

def get_all_policies_data(db: Session):
    return db.query(Policy).order_by(Policy.id.asc()).all()

def get_all_schemes_data(db: Session):
    return db.query(Scheme).order_by(Scheme.id.asc()).all()

def get_all_feedback_data(db: Session):
    return db.query(Feedback).order_by(Feedback.id.asc()).all()

