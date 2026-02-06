from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.engine import Engine
import os
from ..models.user import User
from ..models.task import Task
from ..models.conversation import Conversation
from ..models.message import Message

# Load environment variables only in development
if os.getenv("ENVIRONMENT") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# Adjust DATABASE_URL for PostgreSQL in production
if "postgres" in DATABASE_URL and "?sslmode=" not in DATABASE_URL:
    # For PostgreSQL, add sslmode parameter if not already present
    DATABASE_URL = f"{DATABASE_URL}?sslmode=require"

# Create engine with appropriate settings for production
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}  # Needed for SQLite

engine: Engine = create_engine(
    DATABASE_URL,
    echo=(os.getenv("ENVIRONMENT") != "production"),  # Only echo SQL in development
    connect_args=connect_args
)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session