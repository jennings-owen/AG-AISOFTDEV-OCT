# test_main.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.main import app, get_db, Base


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    """
    Pytest fixture that sets up the database for testing.
    It creates all tables before each test and drops them afterwards.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user_success(db):
    response = client.post("/users/", json={"email": "test@example.com", "full_name": "Test User"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data

def test_create_user_duplicate_email(db):
    client.post("/users/", json={"email": "test@example.com", "full_name": "Test User"})
    response = client.post("/users/", json={"email": "test@example.com", "full_name": "Another User"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email already registered"

def test_get_users_success(db):
    # Create two users
    client.post("/users/", json={"email": "user1@example.com", "full_name": "User One"})
    client.post("/users/", json={"email": "user2@example.com", "full_name": "User Two"})
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "user1@example.com"
    assert data[1]["email"] == "user2@example.com"

def test_get_user_success(db):
    # Create a user
    response = client.post("/users/", json={"email": "test@example.com", "full_name": "Test User"})
    user_id = response.json()["id"]
    
    # Retrieve the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"

def test_update_user_success(db):
    # Create a user
    response = client.post("/users/", json={"email": "test@example.com", "full_name": "Test User"})
    user_id = response.json()["id"]
    
    # Update the user's full_name
    response = client.patch(f"/users/{user_id}", json={"full_name": "Updated User"})
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated User"

def test_delete_user_success(db):
    # Create a user
    response = client.post("/users/", json={"email": "test@example.com", "full_name": "Test User"})
    user_id = response.json()["id"]
    
    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "User deleted successfully"

def test_get_users_with_pagination(db):
    # Create multiple users
    for i in range(10):
        client.post("/users/", json={"email": f"user{i}@example.com", "full_name": f"User {i}"})
    
    response = client.get("/users/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["email"] == "user5@example.com"

def test_update_user_email_success(db):
    # Create a user
    response = client.post("/users/", json={"email": "test@example.com", "full_name": "Test User"})
    user_id = response.json()["id"]
    
    # Update the user's email
    response = client.patch(f"/users/{user_id}", json={"email": "updated@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"

def test_delete_non_existent_user(db):
    response = client.delete("/users/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_get_non_existent_user(db):
    response = client.get("/users/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"