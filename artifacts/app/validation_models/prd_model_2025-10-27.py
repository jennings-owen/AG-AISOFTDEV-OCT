import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

# --- Nested Models for PRD Sections ---

class UserPersona(BaseModel):
    """Represents a user persona affected by the problem."""
    name: str = Field(..., description="Name of the user persona (e.g., The New Hire)")
    scenario: str = Field(..., description="A typical scenario highlighting the problem for this persona.")

class ProblemSection(BaseModel):
    """Details the problem this product aims to solve."""
    problem_statement: str = Field(..., description="Clear and concise description of the primary problem.")
    user_personas_scenarios: List[UserPersona] = Field(
        ..., description="List of key user personas and their typical scenarios affected by the problem."
    )

class GoalMetric(BaseModel):
    """Defines a goal with its corresponding KPI and target."""
    goal: str = Field(..., description="The objective to achieve (e.g., Improve New Hire Efficiency).")
    kpi: str = Field(..., description="Key Performance Indicator (e.g., Reduce time-to-first-contribution).")
    target: str = Field(..., description="The measurable target for the KPI (e.g., Decrease by 20% in Q1).")

class UserStory(BaseModel):
    """Represents an Agile user story with acceptance criteria."""
    story: str = Field(..., description="The user story in 'As a [role], I want to [action], so that [benefit]' format.")
    acceptance_criteria: List[str] = Field(
        ..., description="List of acceptance criteria for the user story (Given/When/Then format)."
    )

class FunctionalRequirementEpic(BaseModel):
    """Groups related user stories under an Epic."""
    epic_name: str = Field(..., description="Name of the epic (e.g., User Authentication).")
    stories: List[UserStory] = Field(..., description="List of user stories belonging to this epic.")

class ReleaseMilestone(BaseModel):
    """Defines a specific release version and its target features."""
    version: str = Field(..., description="Version number (e.g., 1.0 (MVP)).")
    target_date: str = Field(..., description="Target date for this release (e.g., [Target Date]).")
    features: str = Field(..., description="Description of core features included in this release.")

# --- Main ProductRequirementsDocument Model ---

class ProductRequirementsDocument(BaseModel):
    """
    Pydantic model for a Product Requirements Document (PRD).
    This model captures all sections defined in the provided PRD template.
    """

    # Header Section
    product_name: str = Field(..., description="Name of the product (e.g., New Hire Onboarding Platform).")
    status: str = Field("Draft", description="Current status of the document (e.g., Draft, Approved).")
    author: str = Field(..., description="Author or team responsible for the document.")
    version: str = Field("1.0", description="Version number of the PRD.")
    last_updated: str = Field(
        default_factory=lambda: datetime.date.today().isoformat(),
        description="Date when the document was last updated (YYYY-MM-DD)."
    )

    # 1. Executive Summary & Vision
    executive_summary_vision: str = Field(
        ...,
        description=(
            "A high-level overview for stakeholders. "
            "What is this product, why are we building it, and what is the ultimate vision for its success?"
        )
    )

    # 2. The Problem
    the_problem: ProblemSection = Field(
        ..., description="A detailed look at the pain points this product will solve."
    )

    # 3. Goals & Success Metrics
    goals_success_metrics: List[GoalMetric] = Field(
        ..., description="How success will be measured, defining specific, measurable outcomes."
    )

    # 4. Functional Requirements & User Stories
    functional_requirements_user_stories: List[FunctionalRequirementEpic] = Field(
        ..., description="The core of the PRD, detailing what the product must do, broken into epics and user stories."
    )

    # 5. Non-Functional Requirements (NFRs)
    non_functional_requirements: List[str] = Field(
        ..., description="Qualities of the system (e.g., Performance, Security, Accessibility, Scalability)."
    )

    # 6. Release Plan & Milestones
    release_plan_milestones: List[ReleaseMilestone] = Field(
        ..., description="A high-level timeline for delivery, with key milestones."
    )

    # 7. Out of Scope & Future Considerations
    out_of_scope_v1: List[str] = Field(
        ..., description="Features or functionalities explicitly out of scope for Version 1.0."
    )
    future_work: List[str] = Field(
        ..., description="Potential features or considerations for future versions beyond V1.0."
    )

    # 8. Appendix & Open Questions
    open_questions: List[str] = Field(
        ..., description="Questions that need answers or decisions (e.g., 'Which team will...')."
    )
    dependencies: List[str] = Field(
        ..., description="External dependencies required for the project (e.g., 'Final UI design...')."
    )


# Example Usage (optional, for demonstration)
if __name__ == "__main__":
    example_prd = ProductRequirementsDocument(
        product_name="New Hire Onboarding Platform",
        status="Draft",
        author="Acme Inc. Product Team",
        version="1.0",
        last_updated="2023-10-27",
        executive_summary_vision=(
            "The New Hire Onboarding Platform is designed to streamline the onboarding experience for new employees, "
            "ensuring a smooth transition and rapid integration into the company culture. "
            "Our vision is to create an engaging, self-service portal that significantly reduces "
            "time-to-productivity and enhances overall job satisfaction from day one."
        ),
        the_problem=ProblemSection(
            problem_statement=(
                "New hires currently face a fragmented and overwhelming onboarding experience, "
                "leading to decreased initial productivity and a high volume of repetitive questions to HR and managers."
            ),
            user_personas_scenarios=[
                UserPersona(
                    name="The New Hire",
                    scenario=(
                        "Receives disparate emails with tasks, struggles to find necessary documents, "
                        "and feels lost on their first few weeks."
                    ),
                ),
                UserPersona(
                    name="The Hiring Manager",
                    scenario=(
                        "Spends significant time answering basic questions, tracking onboarding progress manually, "
                        "and ensuring all team-specific tasks are completed."
                    ),
                ),
            ],
        ),
        goals_success_metrics=[
            GoalMetric(
                goal="Improve New Hire Efficiency",
                kpi="Reduce time-to-first-contribution",
                target="Decrease by 20% in Q1",
            ),
            GoalMetric(
                goal="Reduce Support Load",
                kpi="Decrease repetitive questions to HR",
                target="30% reduction in support tickets",
            ),
        ],
        functional_requirements_user_stories=[
            FunctionalRequirementEpic(
                epic_name="User Authentication",
                stories=[
                    UserStory(
                        story="As a New Hire, I want to log in with my company credentials, so that I can access the onboarding platform securely.",
                        acceptance_criteria=[
                            "Given I am on the login page, when I enter my valid SSO credentials, then I am redirected to my personal dashboard.",
                            "Given I am on the login page, when I enter invalid credentials, then I see a clear error message.",
                        ],
                    ),
                    UserStory(
                        story="As an HR Admin, I want to reset a new hire's password, so that they can regain access if locked out.",
                        acceptance_criteria=[
                            "Given I am logged in as an HR Admin, when I search for a new hire and select 'Reset Password', then their password is reset and a temporary one is sent.",
                        ],
                    ),
                ],
            ),
            FunctionalRequirementEpic(
                epic_name="Task Management",
                stories=[
                    UserStory(
                        story="As a New Hire, I want to see a checklist of all my pending onboarding tasks, so that I know what I need to complete.",
                        acceptance_criteria=[
                            "Given I am on my dashboard, when I view the 'My Tasks' section, then I see a list of all assigned tasks with their status (To Do, In Progress, Done).",
                            "Given I have completed a task, when I mark it as 'Done', then its status updates and it appears in the 'Completed Tasks' list.",
                        ],
                    ),
                ],
            )
        ],
        non_functional_requirements=[
            "The application must load in under 3 seconds on a standard corporate network connection.",
            "All data must be encrypted in transit and at rest.",
            "The system must comply with company SSO policies.",
            "The user interface must be compliant with WCAG 2.1 AA standards.",
            "The system must support up to 500 concurrent users during peak onboarding seasons.",
        ],
        release_plan_milestones=[
            ReleaseMilestone(
                version="Version 1.0 (MVP)",
                target_date="2024-01-15",
                features="Core features including user login, task checklist, and document repository.",
            ),
            ReleaseMilestone(
                version="Version 1.1",
                target_date="2024-03-01",
                features="Mentorship connection and team introduction features.",
            ),
        ],
        out_of_scope_v1=[
            "Direct integration with third-party HR payroll systems.",
            "A native mobile application (the web app will be mobile-responsive).",
            "Advanced analytics dashboard for managers.",
        ],
        future_work=[
            "Integration with the corporate Learning Management System (LMS).",
            "AI-powered personalized learning paths for new hires.",
        ],
        open_questions=[
            "Which team will be responsible for maintaining the content in the document repository?",
            "What are the specific legal compliance requirements for document storage?",
        ],
        dependencies=[
            "The final UI design mockups are required from the Design team by 2023-11-15.",
            "Access to the corporate SSO authentication API is required by 2023-12-01.",
        ],
    )

    print(example_prd.model_dump_json(indent=2))

    # You can also access individual fields
    print(f"\nProduct Name: {example_prd.product_name}")
    print(f"Author: {example_prd.author}")
    print(f"Problem Statement: {example_prd.the_problem.problem_statement}")
    print(f"First User Story: {example_prd.functional_requirements_user_stories[0].stories[0].story}")