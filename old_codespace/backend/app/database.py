"""
Database setup and session management.
Using SQLAlchemy with async support.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Check if using SQLite (default and only supported DB now)
db_url = settings.DATABASE_URL
if not db_url.startswith("sqlite"):
    print(f"WARNING: Postgres config detected ({db_url}) but not supported. Falling back to SQLite.")
    db_url = "sqlite:///./flirtnet.db"

# SQLite setup
engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Use this in FastAPI route dependencies.
    
    Example:
        @app.get("/users/")
        def read_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    Call this when starting the app.
    """
    # Import all models here so they are registered with Base
    from app.models import user, profile, chat, connection, post, message, random_chat_history
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
