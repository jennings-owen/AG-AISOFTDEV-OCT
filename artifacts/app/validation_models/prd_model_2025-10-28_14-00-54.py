from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Optional

# --- Helper Models for Structured Sections ---

class Persona(BaseModel):
    """Represents a user persona affected by the problem."""
    name: str = Field(..., description="The name of the user persona (e.g., 'The New Hire').")
    description: str = Field(..., description="A typical scenario or summary describing the persona's interaction with the problem.")

class GoalMetric(BaseModel):
    """Represents a product goal with its key performance indicator and target."""
    goal: str = Field(..., description="A specific goal for the product (e.g., 'Improve New Hire Efficiency').")
    kpi: str = Field(..., description="The Key Performance Indicator used to measure the goal (e.g., 'Reduce time-to-first-contribution').")
    target: str = Field(..., description="The measurable target for the KPI (e.g., 'Decrease by 20% in Q1').")

class AcceptanceCriterion(BaseModel):
    """Represents a single acceptance criterion for a user story."""
    criterion: str = Field(..., description="A clear, testable statement describing a condition that must be met for the user story to be complete (e.g., 'Given I am on the login page, when I enter my valid SSO credentials, then I am redirected to my personal dashboard.').")

class UserStory(BaseModel):
    """Represents an Agile user story with its description and acceptance criteria."""
    story: str = Field(..., description="The user story, typically in the format: 'As a [user], I want [action], so that [value].'")
    acceptance_criteria: List[AcceptanceCriterion] = Field(default_factory=list, description="A list of acceptance criteria that define when the user story is complete.")

class Epic(BaseModel):
    """Represents a larger body of work, comprising multiple related user stories."""
    epic_name: str = Field(..., description="The name of the epic (e.g., 'User Authentication').")
    user_stories: List[UserStory] = Field(default_factory=list, description="A list of user stories associated with this epic.")

class ReleaseMilestone(BaseModel):
    """Represents a planned release version with its target date and description."""
    version: str = Field(..., description="The version number of the release (e.g., '1.0 (MVP)').")
    target_date: str = Field(..., description="The target date for this release (e.g., 'Q1 2024' or '2024-03-31').")
    description: str = Field(..., description="A brief description of the core features or focus of this release.")

# --- Main Product Requirements Document Model ---

class ProductRequirementsDocument(BaseModel):
    """
    Pydantic model for a Product Requirements Document (PRD).

    This model structures the key sections of a PRD, allowing for
    programmatic creation, validation, and manipulation of product requirements.
    """

    # --- Header/Metadata ---
    product_name: str = Field(..., description="The official name of the product being documented.")
    status: Literal["Draft", "In Review", "Approved", "Archived"] = Field("Draft", description="The current lifecycle status of the PRD.")
    author: str = Field(..., description="The name of the individual or team responsible for authoring the PRD.")
    version: str = Field("1.0", description="The version number of this PRD document.")
    last_updated: str = Field(..., description="The date when the PRD was last updated (e.g., 'YYYY-MM-DD').")

    # --- 1. Executive Summary & Vision ---
    executive_summary_vision: str = Field(..., description="A high-level overview for stakeholders, summarizing the product's purpose, core problem, target users, and ultimate vision for success.")

    # --- 2. The Problem ---
    problem_statement: str = Field(..., description="A clear and concise description of the primary pain points or challenges this product aims to solve.")
    user_personas_scenarios: List[Persona] = Field(default_factory=list, description="A summary of key user personas affected by the problem, along with typical scenarios highlighting their pain points.")

    # --- 3. Goals & Success Metrics ---
    goals_success_metrics: List[GoalMetric] = Field(default_factory=list, description="A list of specific, measurable goals for the product, each with its Key Performance Indicator (KPI) and target.")

    # --- 4. Functional Requirements & User Stories ---
    functional_requirements_user_stories: List[Epic] = Field(default_factory=list, description="The core functional requirements detailed as epics, each containing actionable user stories with acceptance criteria.")

    # --- 5. Non-Functional Requirements (NFRs) ---
    non_functional_requirements: Dict[str, str] = Field(default_factory=dict, description="Key qualities of the system, such as performance, security, accessibility, and scalability requirements.")

    # --- 6. Release Plan & Milestones ---
    release_plan_milestones: List[ReleaseMilestone] = Field(default_factory=list, description="A high-level timeline outlining planned releases, versions, and their core features or focus areas.")

    # --- 7. Out of Scope & Future Considerations ---
    out_of_scope_v1: List[str] = Field(default_factory=list, description="Items or features that are explicitly not included in the initial version (V1.0) to manage scope.")
    future_work: List[str] = Field(default_factory=list, description="Ideas, features, or integrations planned for future iterations beyond the current scope.")

    # --- 8. Appendix & Open Questions ---
    open_questions: List[str] = Field(default_factory=list, description="A list of unresolved questions or decisions that need to be addressed.")
    dependencies: List[str] = Field(default_factory=list, description="External dependencies (e.g., other teams, third-party services) required for the project's success.")