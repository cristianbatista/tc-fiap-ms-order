import os
# Ensure the application reads the test database URL and test environment before importing app modules
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
# Mark environment as test to avoid hitting external resources during unit tests
os.environ.setdefault("ENVIRONMENT", "test")
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base, get_db
from app.main import app

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client"""
    yield TestClient(app)
    app.dependency_overrides.clear()
