"""
Database configuration and session management for the application.

This module owns the responsibility of:
- creating the SQLAlchemy engine
- creating the database sessions
- exposing the declarative base for model definitions

Other parts of the application should import database resources from here instead of creating independent instances.
"""
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

"""
The SQLAlchemy engine is responsible for managing database connections.

pool_pre_ping helps recover stale connections automatically.
"""

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

"""
SessionLocal creates independent database sessions for each request.

Each API request should use its own session instance.
"""
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)

"""
Base is the parent class all ORM models will inherit from.
"""
Base = declarative_base()