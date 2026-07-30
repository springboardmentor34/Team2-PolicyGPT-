from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine
from app.database.base import Base
from app.models.user import User
from app.routers.auth import router as auth_router

from app.database.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.policy import Policy
from app.models.scheme import Scheme

# Import routers
from app.routers.policy import router as policy_router
from app.routers.scheme import router as scheme_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PolicyGPT API",
    description="Government Policy & Public Scheme Intelligence Platform",
    version="1.0.0"
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Include Authentication Router
app.include_router(auth_router)


@app.get("/")
def home():
<<<<<<< Updated upstream
    return {
        "message": "Welcome to PolicyGPT API"
    }

# Register routers
app.include_router(policy_router)
app.include_router(scheme_router)
# Register routers with clear prefixes and tags
app.include_router(policy_router, prefix="/policies", tags=["Policies"])
app.include_router(scheme_router, prefix="/schemes", tags=["Government Schemes"])
=======
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "message": "Database Connected Successfully!"
        }

    except Exception as e:
        return {
            "error": str(e)
        }
>>>>>>> Stashed changes
