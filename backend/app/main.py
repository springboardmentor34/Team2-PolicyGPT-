from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import text

from app.database.database import Base, engine
from app.models.user import User
from app.models.policy import Policy
from app.models.scheme import Scheme
from app.models.eligibility_rule import EligibilityRule
from app.models.notification import Notification
from app.models.feedback import Feedback
from app.models.report import Report
from app.models.audit_log import AuditLog
from app.models.search_history import SearchHistory

from app.routers.auth import router as auth_router
from app.routers.policy import router as policy_router
from app.routers.scheme import router as scheme_router
from app.routers.eligibility_rule import router as eligibility_rule_router
from app.routers.notification import router as notification_router
from app.routers.feedback import router as feedback_router
from app.routers.report import router as report_router
from app.routers.audit_log import router as audit_log_router
from app.routers.search_history import router as search_history_router

from fastapi.middleware.cors import CORSMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PolicyGPT API",
    description="Government Policy & Public Scheme Intelligence Platform",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Authentication Router
app.include_router(auth_router)

# Register routers (prefixes are handled inside the routers)
app.include_router(policy_router)
app.include_router(scheme_router)
app.include_router(eligibility_rule_router)
app.include_router(notification_router)
app.include_router(feedback_router)
app.include_router(report_router)
app.include_router(audit_log_router)
app.include_router(search_history_router)


@app.get("/")
def home():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "message": "Welcome to PolicyGPT API",
            "database": "Connected Successfully!"
        }
    except Exception as e:
        return {
            "message": "Welcome to PolicyGPT API",
            "database_error": str(e)
        }


@app.get("/login", response_class=FileResponse)
def login_page():
    return FileResponse("static/index.html")


@app.get("/register", response_class=FileResponse)
def register_page():
    return FileResponse("static/index.html")


