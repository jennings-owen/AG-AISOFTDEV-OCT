# main.py

import os
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# --- SQLAlchemy Setup ---

# Use an in-memory SQLite database for this example.
# For production, you would replace this with your database URL.
# The check_same_thread argument is needed only for SQLite.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- SQLAlchemy DB Model ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- Pydantic API Models ---

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # Pydantic V2 Config for ORM mode
    model_config = ConfigDict(from_attributes=True)


# --- Chat Endpoint Models & Mock Agent ---
class ChatRequest(BaseModel):
    """Request body for stateless chat endpoint."""
    question: str

class StatefulChatRequest(BaseModel):
    """Request body for stateful chat endpoint with session support."""
    question: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Response body for chat endpoints."""
    answer: str
    session_id: Optional[str] = None

class MockCompiledAgent:
    """Mock of a compiled LangGraph agent with an invoke interface.

    In production, replace this with the real compiled graph, e.g.:
        from my_graph import compiled_graph
        agent = compiled_graph
    The .invoke method should accept an input (dict or str) and return a mapping
    that includes an 'answer' key.
    
    This mock implementation includes basic conversation memory simulation.
    """
    def __init__(self):
        # Simple in-memory storage for conversation history
        # In production, this would be handled by LangGraph's built-in memory
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
    
    def invoke(self, question: str, config: Optional[Dict[str, Any]] = None):
        """Invoke the agent with optional configuration for stateful conversations."""
        if config and "configurable" in config:
            session_id = config["configurable"].get("session_id")
            if session_id:
                # Handle stateful conversation
                return self._invoke_stateful(question, session_id)
        
        # Simple stateless response
        return {"answer": f"You asked: {question}"}
    
    def _invoke_stateful(self, question: str, session_id: str):
        """Handle stateful conversation with memory."""
        # Initialize conversation history for new sessions
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        # Get conversation context
        history = self.conversation_history[session_id]
        
        # Generate response based on context
        if not history:
            # First message in session
            answer = f"Hello! You asked: {question}"
        else:
            # Follow-up message - show some context awareness
            prev_messages = len(history)
            last_q = history[-1]["question"] if history else ""
            
            if "more about that" in question.lower() or "tell me more" in question.lower():
                answer = f"Certainly! Building on your previous question '{last_q}', here's more detail about: {question}"
            elif "what did i ask" in question.lower() or "previous question" in question.lower():
                if history:
                    answer = f"Your previous question was: '{last_q}'"
                else:
                    answer = "You haven't asked any previous questions in this session."
            else:
                answer = f"You asked: {question} (This is message #{prev_messages + 1} in our conversation)"
        
        # Store this exchange in history
        self.conversation_history[session_id].append({
            "question": question,
            "answer": answer
        })
        
        return {"answer": answer}

# Instantiate the mock agent (replace with real compiled agent when available)
agent = MockCompiledAgent()


# --- FastAPI App Initialization ---

app = FastAPI(
    title="User Management API",
    description="A simple API to manage users with a database backend.",
    version="1.0.0",
)

# Create database tables on startup
# Drop all tables first to ensure clean schema (for development only)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# --- Database Session Dependency ---

def get_db():
    """
    Dependency function to get a database session.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---
@app.get("/")
def root():
    """
    Root endpoint that returns a simple OK message.
    """
    return {"message": "Ok"}

@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    - Checks for email uniqueness.
    - Adds the new user to the database.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new SQLAlchemy User instance
    new_user = User(**user.model_dump())
    
    # Add, commit, and refresh
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.get("/users/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of users with pagination.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by their ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user's details.
    - Allows partial updates for email and full_name.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Get update data, excluding fields that were not set in the request
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Use setattr to update the model instance
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.delete("/users/{user_id}", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(db_user)
    db.commit()
    
    return {"detail": "User deleted successfully"}


@app.post("/chat")
def chat_endpoint(payload: ChatRequest):
    """Stateless chat endpoint.

    Accepts a user's question and returns the agent's answer. No memory or history
    is retained between requests.
    """
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty")

    # Invoke the (mock) compiled LangGraph agent
    response = agent.invoke(question)

    # Defensive extraction of answer
    answer = response.get("answer") if isinstance(response, dict) else None
    if answer is None:
        raise HTTPException(status_code=500, detail="Agent did not return an answer")
    return {"answer": answer}


@app.post("/stateful_chat", response_model=ChatResponse)
def stateful_chat_endpoint(payload: StatefulChatRequest):
    """Stateful chat endpoint with conversation memory.

    Accepts a user's question and optional session_id. If no session_id is provided,
    a new one is generated. The agent maintains conversation context across requests
    within the same session.
    """
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty")

    # Generate session_id if not provided
    session_id = payload.session_id or str(uuid.uuid4())

    # Prepare configuration for LangGraph with session_id
    config = {
        "configurable": {
            "session_id": session_id
        }
    }

    # Invoke the (mock) compiled LangGraph agent with config
    response = agent.invoke(question, config=config)

    # Defensive extraction of answer
    answer = response.get("answer") if isinstance(response, dict) else None
    if answer is None:
        raise HTTPException(status_code=500, detail="Agent did not return an answer")
    
    return ChatResponse(answer=answer, session_id=session_id)





# Not used by docker deployment, but useful for local development
# if __name__ == "__main__":
#     import uvicorn
    
#     # Run the server with auto-reload for development
#     uvicorn.run(
#         "main:app",
#         host="127.0.0.1",
#         port=3000,
#         reload=True,
#         reload_dirs=["./"]
#     )