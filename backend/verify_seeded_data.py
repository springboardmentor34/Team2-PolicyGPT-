import sys
import os

# Allow direct script execution inside backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.models.user import User
from app.models.policy import Policy
from app.models.scheme import Scheme
from app.models.eligibility_rule import EligibilityRule
from app.models.notification import Notification
from app.models.feedback import Feedback
from app.models.report import Report
from app.models.audit_log import AuditLog
from app.models.search_history import SearchHistory

def check():
    db = SessionLocal()
    try:
        policies = db.query(Policy).all()
        schemes = db.query(Scheme).all()
        print(f"Total Policies in PostgreSQL my_database: {len(policies)}")
        for p in policies:
            print(f" - [{p.status}] {p.title} ({p.category})")
        print(f"\nTotal Schemes in PostgreSQL my_database: {len(schemes)}")
        for s in schemes:
            print(f" - [{s.status}] {s.title} ({s.category})")
    finally:
        db.close()

if __name__ == "__main__":
    check()
