from pydantic import BaseModel, Field
from typing import List, Optional

# --- Helper Models for Structured Sections ---

class UserPersona(BaseModel):
    """Represents a user persona affected by the problem statement."""
    name: str = Field(..., description="Name of the user persona (e.g., 'The New Hire').")
    scenario: str = Field(..., description="A typical scenario they face that highlights the problem.")

class GoalMetric(BaseModel):
    """Represents a project goal with its Key Performance Indicator (KPI) and target."""
    goal: str = Field(..., description="The objective to be achieved.")
    kpi: str = Field(..., alias="Key Performance Indicator (KPI)",
                     description="A quantifiable measure used to evaluate the success of the goal.")
    target: str = Field(..., description="The specific, measurable outcome expected for the KPI.")

class AcceptanceCriterion(BaseModel):
    """Represents a single acceptance criterion in a Gherkin-like (Given/When/Then) format."""
    given: str = Field(..., description="The initial context or state.")
    when: str = Field(..., description="The action performed by the user or system.")
    then: str = Field(..., description="The expected outcome or result.")

class UserStory(BaseModel):
    """Represents an Agile user story."""
    id: Optional[str] = Field(None, description="Optional identifier for the story (e.g., 'Story 1.1').")
    description: str = Field(..., description="The user story text (e.g., 'As a [user], I want to [action], so that I can [benefit].').")
    acceptance_criteria: List[AcceptanceCriterion] = Field(default_factory=list,
                                                            description="List of acceptance criteria that define when the story is complete.")

class Epic(BaseModel):
    """Represents an Epic, a collection of related user stories."""
    title: str = Field(..., description="Title of the Epic (e.g., 'User Authentication').")
    stories: List[UserStory] = Field(default_factory=list, description="List of user stories belonging to this Epic.")

class ReleaseMilestone(BaseModel):
    """Represents a release version with its target date and description."""
    version: str = Field(..., description="Version identifier (e.g., '1.0 (MVP)').")
    target_date: str = Field(..., description="Target date for the release (e.g., 'YYYY-MM-DD').")
    description: str = Field(..., description="Description of core features or objectives for this release.")

# --- Main ProductRequirementsDocument Model ---

class ProductRequirementsDocument(BaseModel):
    """
    Pydantic model for a Product Requirements Document (PRD), structuring
    information according to a predefined template.
    """

    # --- Header / Metadata ---
    product_name: str = Field(..., alias="Product Name", description="The official name of the product.")
    status: str = Field("Draft", description="Current status of the document (e.g., 'Draft', 'Approved', 'Final').")
    author: str = Field(..., description="The author or team responsible for creating the document.")
    version: str = Field("1.0", description="Version number of the PRD document itself.")
    last_updated: str = Field(..., description="Date when the document was last updated (e.g., 'YYYY-MM-DD').")

    # --- 1. Executive Summary & Vision ---
    executive_summary_vision: str = Field(..., alias="Executive Summary & Vision",
                                          description="A high-level overview for stakeholders, covering the product's "
                                                      "purpose, core problem it solves, target users, and ultimate vision.")

    # --- 2. The Problem ---
    class ProblemSection(BaseModel):
        """Details the pain points this product will solve, justifying its existence."""
        problem_statement: str = Field(..., description="A clear and concise description of the primary problem the product addresses.")
        user_personas_scenarios: List[UserPersona] = Field(default_factory=list,
                                                            description="Summaries of key user personas affected by the problem "
                                                                        "and typical scenarios highlighting their pain points.")
    the_problem: ProblemSection = Field(..., alias="The Problem")

    # --- 3. Goals & Success Metrics ---
    goals_success_metrics: List[GoalMetric] = Field(default_factory=list, alias="Goals & Success Metrics",
                                                     description="Defines specific, measurable outcomes and how success will be measured.")

    # --- 4. Functional Requirements & User Stories ---
    functional_requirements_user_stories: List[Epic] = Field(default_factory=list,
                                                              alias="Functional Requirements & User Stories",
                                                              description="The core of the PRD, detailing what the product must do, "
                                                                          "broken down into actionable user stories grouped by Epics.")

    # --- 5. Non-Functional Requirements (NFRs) ---
    non_functional_requirements: List[str] = Field(default_factory=list, alias="Non-Functional Requirements (NFRs)",
                                                   description="Qualities of the system, such as performance, security, accessibility, and scalability.")

    # --- 6. Release Plan & Milestones ---
    release_plan_milestones: List[ReleaseMilestone] = Field(default_factory=list, alias="Release Plan & Milestones",
                                                             description="A high-level timeline for product delivery, outlining key versions and their scope.")

    # --- 7. Out of Scope & Future Considerations ---
    class OutOfScopeFutureConsiderations(BaseModel):
        """Defines what is not included in the current scope and potential future plans."""
        out_of_scope_v1: List[str] = Field(default_factory=list, alias="Out of Scope for V1.0",
                                           description="Features or functionalities explicitly excluded from the first version of the product.")
        future_work: List[str] = Field(default_factory=list, alias="Future Work",
                                       description="Potential features, integrations, or enhancements planned for future versions.")

    out_of_scope_future_considerations: OutOfScopeFutureConsiderations = Field(..., alias="Out of Scope & Future Considerations")

    # --- 8. Appendix & Open Questions ---
    class AppendixOpenQuestions(BaseModel):
        """A section for tracking dependencies, assumptions, and open questions."""
        open_questions: List[str] = Field(default_factory=list,
                                           description="Questions that require answers or decisions before proceeding.")
        dependencies_assumptions: List[str] = Field(default_factory=list, alias="Dependencies & Assumptions",
                                                     description="External dependencies (e.g., other teams, systems) or "
                                                                 "underlying assumptions critical to the project's success.")

    appendix_open_questions: AppendixOpenQuestions = Field(..., alias="Appendix & Open Questions")