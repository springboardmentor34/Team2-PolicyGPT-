from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import text

from app.database.database import Base, engine
from app.models.user import User
from app.models.policy import Policy
from app.models.scheme import Scheme
from app.routers.auth import router as auth_router
from app.routers.policy import router as policy_router
from app.routers.scheme import router as scheme_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PolicyGPT API",
    description="Government Policy & Public Scheme Intelligence Platform",
    version="1.0.0"
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Authentication Router
app.include_router(auth_router)

# Register routers (prefixes are handled inside the routers)
app.include_router(policy_router)
app.include_router(scheme_router)


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


