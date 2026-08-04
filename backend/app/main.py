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