from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.database import engine
from app.database.base import Base

# Import all models so SQLAlchemy creates the tables
from app.models.user import User
from app.models.policy import Policy
from app.models.scheme import Scheme
from app.models.eligibility_rule import EligibilityRule
from app.models.notification import Notification
from app.models.feedback import Feedback
from app.models.report import Report
from app.models.audit_log import AuditLog
from app.models.search_history import SearchHistory

# Import routers
from app.routers.auth import router as auth_router
from app.routers.policy import router as policy_router
from app.routers.scheme import router as scheme_router
from app.routers.feedback import router as feedback_router
from app.routers.notification import router as notification_router
from app.routers.report import router as report_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# Dynamically apply table schema modifications if table already exists (for PostgreSQL compatibility)
def run_migrations():
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            # policies table adjustments
            conn.execute(text("ALTER TABLE policies ADD COLUMN IF NOT EXISTS created_by INTEGER REFERENCES users(id);"))
            conn.execute(text("ALTER TABLE policies ADD COLUMN IF NOT EXISTS reviewed_by INTEGER REFERENCES users(id);"))
            conn.execute(text("ALTER TABLE policies ADD COLUMN IF NOT EXISTS review_comment TEXT;"))
            conn.execute(text("ALTER TABLE policies ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE;"))
            conn.execute(text("ALTER TABLE policies ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITHOUT TIME ZONE;"))
            conn.execute(text("ALTER TABLE policies ADD COLUMN IF NOT EXISTS published_at TIMESTAMP WITHOUT TIME ZONE;"))
            
            # audit_logs table adjustments
            conn.execute(text("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS old_status VARCHAR;"))
            conn.execute(text("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS new_status VARCHAR;"))
            conn.execute(text("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS comment TEXT;"))
            conn.execute(text("ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS policy_id INTEGER REFERENCES policies(id);"))
            conn.commit()

            # Seed developer test users if they don't exist
            from app.database.database import SessionLocal
            from app.models.user import User
            from app.auth.security import hash_password
            
            db = SessionLocal()
            try:
                seed_users = [
                    {"email": "official@policygpt.gov.in", "password": "Password123", "full_name": "Official Administrator", "role": "government_official"},
                    {"email": "admin@policygpt.gov.in", "password": "Password123", "full_name": "Main Administrator", "role": "administrator"},
                    {"email": "citizen@policygpt.gov.in", "password": "Password123", "full_name": "Citizen User", "role": "citizen"}
                ]
                for su in seed_users:
                    exists = db.query(User).filter(User.email == su["email"]).first()
                    if not exists:
                        user = User(
                            email=su["email"],
                            password=hash_password(su["password"]),
                            full_name=su["full_name"],
                            role=su["role"]
                        )
                        db.add(user)
                        db.commit()
                        print(f"Seeded user: {su['email']}")
            except Exception as se:
                print(f"Seeding error: {se}")
            finally:
                db.close()

            print("Database self-healing schema migration ran successfully.")
    except Exception as e:
        print(f"Migration error: {e}")

run_migrations()


app = FastAPI(
    title="PolicyGPT API",
    description="Government Policy & Public Scheme Intelligence Platform",
    version="1.0.0"
)

# ---------------------------------------------------------------------------
# CORS — allow Angular dev server (port 4200) to call the API (port 8000)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(policy_router, prefix="/policies", tags=["Policies"])
app.include_router(scheme_router, prefix="/schemes", tags=["Government Schemes"])
app.include_router(feedback_router)
app.include_router(notification_router)
app.include_router(report_router)


@app.get("/", tags=["Health"])
def home():
    """Health check — verifies database connectivity."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"message": "PolicyGPT API is running. Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}