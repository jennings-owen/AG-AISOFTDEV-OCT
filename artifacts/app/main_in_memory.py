# main_in_memory.py

"""
A self-contained FastAPI script providing a thread-safe, in-memory CRUD API 
for a 'users' resource, based on a provided SQL schema.
"""

import threading
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Annotated

from fastapi import FastAPI, HTTPException, Path, Response, status
from pydantic import BaseModel, EmailStr, Field

# --- 1. In-memory Storage and Thread Safety ---

# A simple list of dictionaries to act as our in-memory database table.
users_db: List[Dict[str, Any]] = []

# A counter to simulate auto-incrementing primary keys.
next_id: int = 1

# A re-entrant lock to ensure thread safety for database mutations.
# This prevents race conditions if multiple requests try to modify the data
# simultaneously.
db_lock = threading.RLock()


# --- 2. Pydantic Models ---

# Pydantic models define the data shape and validation for our API.
# They are used for request bodies and response models.

class UserType(str, Enum):
    """Enumeration for the allowed user types."""
    NEW_HIRE = "new_hire"
    HR_SPECIALIST = "hr_specialist"
    MANAGER = "manager"


class UserBase(BaseModel):
    """
    Base model with common user fields, used for creation and reading.
    Fields are derived from the 'users' table in the SQL schema.
    """
    full_name: str = Field(..., min_length=2, max_length=100,
                           description="User's full name.")
    email: EmailStr = Field(..., description="User's unique email address.")
    user_type: UserType = Field(..., description="The type of the user.")
    role_id: Optional[int] = Field(None, description="Foreign key to the roles table.")
    manager_id: Optional[int] = Field(None, description="Self-referencing foreign key for the user's manager.")
    mentor_id: Optional[int] = Field(None, description="Self-referencing foreign key for the user's mentor.")
    start_date: Optional[date] = Field(None, description="User's start date.")


class UserCreate(UserBase):
    """
    Model for creating a new user. Inherits all fields from UserBase.
    This model represents the data expected in a POST request body.
    """
    pass


class UserUpdate(BaseModel):
    """
    Model for updating an existing user. All fields are optional to allow
    for partial updates (PATCH-like behavior with PUT).
    """
    full_name: Optional[str] = Field(None, min_length=2, max_length=100,
                                     description="User's full name.")
    email: Optional[EmailStr] = Field(None, description="User's unique email address.")
    user_type: Optional[UserType] = Field(None, description="The type of the user.")
    role_id: Optional[int] = Field(None, description="Foreign key to the roles table.")
    manager_id: Optional[int] = Field(None, description="Self-referencing foreign key for the user's manager.")
    mentor_id: Optional[int] = Field(None, description="Self-referencing foreign key for the user's mentor.")
    start_date: Optional[date] = Field(None, description="User's start date.")


class User(UserBase):
    """
    Full user model for API responses. Includes read-only fields like
    id and timestamps. This is used as the `response_model`.
    """
    id: int = Field(..., description="Primary key for the user.")
    created_at: datetime = Field(..., description="Timestamp of user creation (UTC).")
    updated_at: datetime = Field(..., description="Timestamp of last user update (UTC).")


# --- 3. FastAPI Application Setup ---

app = FastAPI(
    title="In-Memory User CRUD API",
    description="A demonstration of a FastAPI backend with in-memory storage.",
    version="1.0.0",
)


# --- 4. Helper Functions ---

def find_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Finds a user in the database by their ID."""
    with db_lock:
        for user in users_db:
            if user["id"] == user_id:
                return user
    return None


def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Finds a user in the database by their email."""
    with db_lock:
        for user in users_db:
            if user["email"] == email:
                return user
    return None


def get_user_or_404(user_id: int) -> Dict[str, Any]:
    """
    Dependency-like helper to retrieve a user by ID or raise an
    HTTP 404 Not Found error.
    """
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


# --- 5. API Endpoints ---

@app.post(
    "/users/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    tags=["Users"],
)
def create_user(user_in: UserCreate) -> Dict[str, Any]:
    """
    Creates a new user record in the in-memory database.

    - Validates that the email is unique.
    - Assigns a new ID and timestamps.
    - Returns the created user object.
    """
    global next_id
    with db_lock:
        if find_user_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

        now = datetime.now(timezone.utc)
        new_user = user_in.model_dump()
        new_user.update({
            "id": next_id,
            "created_at": now,
            "updated_at": now,
        })
        users_db.append(new_user)
        next_id += 1
        return new_user


@app.get(
    "/users/",
    response_model=List[User],
    summary="List all users",
    tags=["Users"],
)
def list_users() -> List[Dict[str, Any]]:
    """
    Retrieves a list of all user records.
    """
    with db_lock:
        # Return a copy to prevent modification of the original data
        return list(users_db)


@app.get(
    "/users/{user_id}",
    response_model=User,
    summary="Get a single user by ID",
    tags=["Users"],
)
def get_user(
    user_id: Annotated[int, Path(title="The ID of the user to retrieve.", gt=0)]
) -> Dict[str, Any]:
    """
    Retrieves a single user by their unique ID.
    Returns a 404 error if the user does not exist.
    """
    return get_user_or_404(user_id)


@app.put(
    "/users/{user_id}",
    response_model=User,
    summary="Update a user",
    tags=["Users"],
)
def update_user(
    user_update: UserUpdate,
    user_id: Annotated[int, Path(title="The ID of the user to update.", gt=0)],
) -> Dict[str, Any]:
    """
    Updates an existing user's information.

    - Uses PUT with merge semantics: only provided fields are updated.
    - Validates email uniqueness if the email is being changed.
    - Updates the `updated_at` timestamp.
    - Returns a 404 error if the user does not exist.
    """
    with db_lock:
        user_to_update = get_user_or_404(user_id)
        
        # Check for email collision before updating
        if user_update.email and user_update.email != user_to_update["email"]:
            existing_user = find_user_by_email(user_update.email)
            if existing_user and existing_user["id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered by another user."
                )

        # Get update data, excluding fields that were not set in the request
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Update the user dictionary
        user_to_update.update(update_data)
        user_to_update["updated_at"] = datetime.now(timezone.utc)

        return user_to_update


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    tags=["Users"],
)
def delete_user(
    user_id: Annotated[int, Path(title="The ID of the user to delete.", gt=0)]
) -> Response:
    """
    Deletes a user from the in-memory database.

    - Idempotent: returns a successful response even if the user
      was already deleted.
    - Returns a 204 No Content response on success.
    """
    with db_lock:
        user_to_delete = find_user_by_id(user_id)
        if user_to_delete:
            users_db.remove(user_to_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- 6. Main Guard ---

if __name__ == "__main__":
    import uvicorn
    print("--- To run this application, use the command: ---")
    print("--- uvicorn main_in_memory:app --reload ---")
    # uvicorn.run("main_in_memory:app", host="127.0.0.1", port=8000, reload=True)