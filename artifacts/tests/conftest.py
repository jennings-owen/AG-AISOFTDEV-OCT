# conftest.py

import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.main import app, Base, get_db, User

# ---- Test Database Fixture ----

@pytest.fixture
def test_db():
    # 1. Create a new in-memory SQLite engine and sessionmaker
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 2. Create all tables
    Base.metadata.create_all(bind=engine)

    # 3. Optionally, seed initial data
    # Example: create a test user
    with TestingSessionLocal() as session:
        user = User(email="seed@example.com", full_name="Seed User")
        session.add(user)
        session.commit()

    # 4. Provide a fresh session for each test
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # 5. Override the app's get_db dependency
    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal

    # 6. Teardown: Drop all tables and dispose engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    """
    Provides a FastAPI TestClient that uses the isolated test database.
    """
    with TestClient(app) as c:
        yield c