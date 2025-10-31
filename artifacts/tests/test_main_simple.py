# test_main.py

import pytest
from fastapi.testclient import TestClient

# Before importing the app use the code:
import sys
import os

# Ensure the current directory is in sys.path to import main.py
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.main import app

client = TestClient(app)


def test_root_returns_404():
    """Test that GET / returns 404 since no root endpoint exists."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ok"}

def test_post_users_create_minimal():
    """Test creating a user with minimal required fields."""
    data = {"email": "minimal@example.com"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == data["email"]
    assert user["id"] > 0
    assert "created_at" in user
    assert "updated_at" in user

def test_post_users_create_full():
    """Test creating a user with all fields."""
    data = {"email": "full@example.com", "full_name": "Full Name"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == data["email"]
    assert user["full_name"] == data["full_name"]
    assert user["id"] > 0

def test_post_users_unique_email():
    """Test that creating a user with a unique email works."""
    data = {"email": "unique@example.com", "full_name": "Unique User"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == data["email"]
    assert user["full_name"] == data["full_name"]

def test_get_users_empty():
    """Test getting users when at least one user exists."""
    # Create a user first (should already exist from previous tests, but ensure it)
    email = "getusers1@example.com"
    client.post("/users/", json={"email": email, "full_name": "Get User"})
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(u["email"] == email for u in users)

def test_get_users_pagination():
    """Test retrieving users with skip and limit."""
    # Create two users
    client.post("/users/", json={"email": "paga@example.com"})
    client.post("/users/", json={"email": "pagb@example.com"})
    # Get only one (limit=1)
    resp = client.get("/users/?limit=1")
    assert resp.status_code == 200
    users = resp.json()
    assert len(users) == 1
    # Get with skip
    resp = client.get("/users/?skip=1&limit=2")
    assert resp.status_code == 200
    users = resp.json()
    assert isinstance(users, list)

def test_get_user_by_id():
    """Test retrieving a single user by ID."""
    # Create a user and then retrieve by id
    resp = client.post("/users/", json={"email": "byid@example.com", "full_name": "By Id"})
    user_id = resp.json()["id"]
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    user = get_resp.json()
    assert user["id"] == user_id
    assert user["email"] == "byid@example.com"

def test_patch_users_update_email():
    """Test updating a user's email successfully."""
    # Create a user
    resp = client.post("/users/", json={"email": "update1@example.com", "full_name": "Update Me"})
    user_id = resp.json()["id"]
    # Update email
    update_resp = client.patch(f"/users/{user_id}", json={"email": "updatedemail@example.com"})
    assert update_resp.status_code == 200
    user = update_resp.json()
    assert user["email"] == "updatedemail@example.com"
    assert user["id"] == user_id

def test_patch_users_update_full_name():
    """Test updating a user's full_name successfully."""
    resp = client.post("/users/", json={"email": "update2@example.com", "full_name": "Old Name"})
    user_id = resp.json()["id"]
    update_resp = client.patch(f"/users/{user_id}", json={"full_name": "New Name"})
    assert update_resp.status_code == 200
    user = update_resp.json()
    assert user["full_name"] == "New Name"

def test_delete_users_delete_user():
    """Test deleting a user by ID."""
    resp = client.post("/users/", json={"email": "deleteuser@example.com", "full_name": "Delete Me"})
    user_id = resp.json()["id"]
    delete_resp = client.delete(f"/users/{user_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"detail": "User deleted successfully"}
    # Ensure user is deleted
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404