### SQLAlchemy Models ###
from __future__ import annotations

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
    text,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

# Base class for declarative models
Base = declarative_base()


class Department(Base):
    """Represents a department within the organization."""
    __tablename__ = "departments"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )

    # Relationships
    roles: Mapped[list["Role"]] = relationship("Role", back_populates="department")


class Role(Base):
    """Represents a job role, which belongs to a department."""
    __tablename__ = "roles"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )

    # Relationships
    department: Mapped["Department"] = relationship("Department", back_populates="roles")
    users: Mapped[list["User"]] = relationship("User", back_populates="role")
    onboarding_tasks: Mapped[list["OnboardingTask"]] = relationship("OnboardingTask", back_populates="role")

    # Indexes
    __table_args__ = (Index("idx_roles_department_id", "department_id"),)


class User(Base):
    """Represents a user, who can be a new hire, manager, mentor, or HR specialist."""
    __tablename__ = "users"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    user_type: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    mentor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    start_date: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )

    # Relationships
    role: Mapped["Role | None"] = relationship("Role", back_populates="users")
    user_tasks: Mapped[list["UserTask"]] = relationship("UserTask", back_populates="user")
    
    # Self-referential relationships for manager/reports hierarchy
    manager: Mapped["User | None"] = relationship("User", remote_side=[id], back_populates="reports")
    reports: Mapped[list["User"]] = relationship("User", back_populates="manager")
    
    # Self-referential relationships for mentor/mentees
    mentor: Mapped["User | None"] = relationship("User", remote_side=[id], back_populates="mentees")
    mentees: Mapped[list["User"]] = relationship("User", back_populates="mentor")

    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint(user_type.in_(['new_hire', 'hr_specialist', 'manager']), name="user_type_check"),
        Index("idx_users_email", "email"),
        Index("idx_users_role_id", "role_id"),
        Index("idx_users_manager_id", "manager_id"),
        Index("idx_users_mentor_id", "mentor_id"),
    )


class OnboardingTask(Base):
    """Represents a default onboarding task template, often tied to a specific role."""
    __tablename__ = "onboarding_tasks"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    task_type: Mapped[str] = mapped_column(String, nullable=False)
    default_due_days: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )

    # Relationships
    role: Mapped["Role | None"] = relationship("Role", back_populates="onboarding_tasks")
    user_assignments: Mapped[list["UserTask"]] = relationship("UserTask", back_populates="onboarding_task")

    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint(task_type.in_(['learning_module', 'hr_form', 'simulated_project']), name="task_type_check"),
        Index("idx_onboarding_tasks_role_id", "role_id"),
    )


class UserTask(Base):
    """Join table assigning an onboarding task to a specific user with its status."""
    __tablename__ = "user_tasks"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("onboarding_tasks.id"), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=text("'pending'"))
    due_date: Mapped[str | None] = mapped_column(String)
    completed_at: Mapped[str | None] = mapped_column(String)
    submission_url: Mapped[str | None] = mapped_column(String)
    feedback: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="user_tasks")
    onboarding_task: Mapped["OnboardingTask"] = relationship("OnboardingTask", back_populates="user_assignments")

    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint("user_id", "task_id", name="uq_user_tasks_user_id_task_id"),
        CheckConstraint(status.in_(['pending', 'in_progress', 'completed', 'overdue']), name="status_check"),
        Index("idx_user_tasks_user_id", "user_id"),
        Index("idx_user_tasks_task_id", "task_id"),
        Index("idx_user_tasks_status", "status"),
    )


class Resource(Base):
    """Represents a generic resource like a document, link, or tool."""
    __tablename__ = "resources"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    resource_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("strftime('%Y-%m-%dT%H:%M:%fZ', 'now')")
    )

    # Indexes
    __table_args__ = (Index("idx_resources_category", "category"),)

### END MODELS ###
### Database Session Setup ###
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the database URL for a local SQLite file.
# The file will be created in the current directory if it doesn't exist.
DATABASE_URL = "sqlite:///./onboarding.db"

# Create the SQLAlchemy engine.
# `connect_args` is needed only for SQLite to enforce foreign key constraints.
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create a sessionmaker to generate new Session objects.
# These settings are typical for FastAPI applications to ensure sessions
# are handled correctly per request.
SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False, 
    expire_on_commit=False
)

def get_db():
    """
    FastAPI dependency to get a database session.
    This generator function yields a database session for a single request
    and ensures it's closed afterward, even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### END SESSION SETUP ###