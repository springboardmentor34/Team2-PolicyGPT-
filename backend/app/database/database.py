import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env
load_dotenv()

# Read DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if DATABASE_URL exists
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set in environment variables or .env file"
    )

# Configure SQLite-specific connection arguments
# (Ignored for PostgreSQL)
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

# Create SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# Create Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

<<<<<<< Updated upstream
# Base class for all SQLAlchemy models
Base = declarative_base()


# Dependency to get DB session
=======
# Dependency
>>>>>>> Stashed changes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
<<<<<<< Updated upstream
        db.close()
=======
        db.close()


>>>>>>> Stashed changes
