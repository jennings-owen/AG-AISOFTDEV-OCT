from datetime import date
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, HttpUrl

# --- Sub-models for complex sections ---

class Header(BaseModel):
    """Model for the PRD document header metadata."""
    product_name: str = Field(..., description="The name of the product.")
    status: str = Field("Draft", description="Current status of the PRD (e.g., Draft, In Review, Approved).")
    author: str = Field(..., description="The author or team responsible for the PRD.")
    version: str = Field("1.0", description="Version number of the PRD.")
    last_updated: date = Field(..., description="The date the PRD was last updated.")

class Persona(BaseModel):
    """Model for a user persona."""
    name: str = Field(..., description="The name of the user persona (e.g., The New Hire).")
    scenario: str = Field(..., description="A typical scenario highlighting the problem for this persona.")

class GoalMetric(BaseModel):
    """Model for a single goal and its success metrics."""
    goal: str = Field(..., description="A specific goal for the product.")
    kpi: str = Field(..., description="Key Performance Indicator to measure progress towards the goal.")
    target: str = Field(..., description="The measurable target for the KPI.")

class UserStory(BaseModel):
    """Model for an Agile user story."""
    description: str = Field(..., description="The 'As a <user>, I want <action>, so that <benefit>' statement.")
    acceptance_criteria: List[str] = Field(..., description="List of conditions that must be met for the story to be considered complete.")

class Epic(BaseModel):
    """Model for an Epic, containing multiple related user stories."""
    title: str = Field(..., description="Title of the epic (e.g., User Authentication).")
    stories: List[UserStory] = Field(..., description="List of user stories under this epic.")

class ReleaseMilestone(BaseModel):
    """Model for a release plan milestone."""
    version: str = Field(..., description="Version number for the release (e.g., 1.0, MVP).")
    target_date: date = Field(..., description="Target date for this release.")
    description: str = Field(..., description="Description of the core features included in this release.")

# --- Main ProductRequirementsDocument Model ---

class ProductRequirementsDocument(BaseModel):
    """
    Pydantic model representing a Product Requirements Document (PRD).
    """

    # Header section
    header: Header = Field(..., description="Metadata for the PRD document.")

    # 1. Executive Summary & Vision
    executive_summary_and_vision: str = Field(
        ...,
        description="A high-level overview for stakeholders, including product purpose, problem solved, target users, and vision.",
    )

    # 2. The Problem
    problem_statement: str = Field(
        ...,
        description="A clear and concise description of the primary problem the product solves.",
    )
    user_personas_and_scenarios: List[Persona] = Field(
        ...,
        description="Summaries of key user personas affected by the problem, with typical scenarios.",
    )

    # 3. Goals & Success Metrics
    goals_and_success_metrics: List[GoalMetric] = Field(
        ...,
        description="Specific, measurable outcomes expected from the product, with KPIs and targets.",
    )

    # 4. Functional Requirements & User Stories
    functional_requirements_and_user_stories: List[Epic] = Field(
        ...,
        description="Detailed functional requirements broken down into epics and user stories with acceptance criteria.",
    )

    # 5. Non-Functional Requirements (NFRs)
    non_functional_requirements: Dict[str, str] = Field(
        ...,
        description="Qualities of the system (e.g., Performance, Security, Accessibility, Scalability). "
                    "Keys are NFR categories, values are their descriptions.",
        examples=[
            {"Performance": "The application must load in under 3 seconds on a standard corporate network connection."},
            {"Security": "All data must be encrypted in transit and at rest. The system must comply with company SSO policies."}
        ]
    )

    # 6. Release Plan & Milestones
    release_plan_and_milestones: List[ReleaseMilestone] = Field(
        ...,
        description="A high-level timeline for delivery, outlining key versions and their features.",
    )

    # 7. Out of Scope & Future Considerations
    out_of_scope_v1: List[str] = Field(
        ...,
        description="Features or functionalities explicitly excluded from the initial version (V1.0).",
    )
    future_work: List[str] = Field(
        ...,
        description="Ideas or features planned for subsequent versions or future consideration.",
    )

    # 8. Appendix & Open Questions
    open_questions: List[str] = Field(
        default_factory=list,
        description="Questions that need answers or decisions from stakeholders.",
    )
    dependencies: List[str] = Field(
        default_factory=list,
        description="External dependencies or required inputs from other teams/systems.",
    )

# --- Example Usage (Optional, for demonstration) ---

if __name__ == "__main__":
    today = date.today()

    example_prd_data = {
        "header": {
            "product_name": "New Hire Onboarding Platform",
            "status": "Draft",
            "author": "Product Team Alpha",
            "version": "1.0",
            "last_updated": today.isoformat(),
        },
        "executive_summary_and_vision": (
            "This product is an interactive web-based platform designed to streamline the onboarding "
            "experience for new hires. It aims to reduce administrative burden on HR, "
            "accelerate time-to-productivity for new employees, and foster a strong sense of belonging "
            "from day one. The ultimate vision is a fully integrated, personalized onboarding journey."
        ),
        "problem_statement": (
            "New hires currently face a fragmented and overwhelming onboarding experience, "
            "leading to decreased initial productivity and a high volume of repetitive questions to HR and managers."
        ),
        "user_personas_and_scenarios": [
            {
                "name": "The New Hire",
                "scenario": "A new hire struggles to find all necessary documents, training materials, "
                            "and team introductions across multiple disparate systems, feeling lost and overwhelmed."
            },
            {
                "name": "The HR Coordinator",
                "scenario": "An HR Coordinator spends significant time manually sending out documents, "
                            "answering repetitive questions, and tracking onboarding progress for each new employee."
            }
        ],
        "goals_and_success_metrics": [
            {
                "goal": "Improve New Hire Efficiency",
                "kpi": "Reduce time-to-first-contribution",
                "target": "Decrease by 20% in Q1"
            },
            {
                "goal": "Reduce Support Load",
                "kpi": "Decrease repetitive questions to HR",
                "target": "30% reduction in support tickets"
            }
        ],
        "functional_requirements_and_user_stories": [
            {
                "title": "User Authentication",
                "stories": [
                    {
                        "description": "As a New Hire, I want to log in with my company credentials, "
                                       "so that I can access the onboarding platform securely.",
                        "acceptance_criteria": [
                            "Given I am on the login page, when I enter my valid SSO credentials, "
                            "then I am redirected to my personal dashboard.",
                            "Given I am on the login page, when I enter invalid credentials, "
                            "then I see a clear error message."
                        ]
                    },
                    {
                        "description": "As a System Admin, I want to manage user accounts, "
                                       "so that I can ensure proper access control.",
                        "acceptance_criteria": [
                            "Given I am logged in as an admin, when I search for a user, "
                            "then I can view their profile and permissions."
                        ]
                    }
                ]
            },
            {
                "title": "Task Management",
                "stories": [
                    {
                        "description": "As a New Hire, I want to see a checklist of my onboarding tasks, "
                                       "so that I know what I need to complete.",
                        "acceptance_criteria": [
                            "Given I am on my dashboard, when I view the tasks section, "
                            "then I see a list of assigned onboarding tasks with their status."
                        ]
                    }
                ]
            }
        ],
        "non_functional_requirements": {
            "Performance": "The application must load in under 3 seconds on a standard corporate network connection.",
            "Security": "All data must be encrypted in transit and at rest. The system must comply with company SSO policies.",
            "Accessibility": "The user interface must be compliant with WCAG 2.1 AA standards.",
            "Scalability": "The system must support up to 500 concurrent users during peak onboarding seasons."
        },
        "release_plan_and_milestones": [
            {
                "version": "1.0 (MVP)",
                "target_date": date(2023, 12, 15).isoformat(),
                "description": "Core features including user login, task checklist, and document repository."
            },
            {
                "version": "1.1",
                "target_date": date(2024, 2, 28).isoformat(),
                "description": "Mentorship connection and team introduction features."
            }
        ],
        "out_of_scope_v1": [
            "Direct integration with third-party HR payroll systems.",
            "A native mobile application (the web app will be mobile-responsive).",
            "Advanced analytics dashboard for managers."
        ],
        "future_work": [
            "Integration with the corporate Learning Management System (LMS).",
            "AI-powered personalized learning paths for new hires."
        ],
        "open_questions": [
            "Which team will be responsible for maintaining the content in the document repository?",
            "What is the budget for third-party integrations in Q2?"
        ],
        "dependencies": [
            "The final UI design mockups are required from the Design team by 2023-11-30.",
            "Access to corporate SSO API for authentication integration."
        ]
    }

    try:
        prd = ProductRequirementsDocument(**example_prd_data)
        print("Pydantic model successfully created for the PRD!")
        print(f"\nProduct Name: {prd.header.product_name}")
        print(f"Version: {prd.header.version}")
        print(f"First User Story: {prd.functional_requirements_and_user_stories[0].stories[0].description}")
        print(f"Non-Functional Requirement (Security): {prd.non_functional_requirements['Security']}")
        # print(prd.model_dump_json(indent=2)) # For Pydantic v2
        # print(prd.json(indent=2)) # For Pydantic v1
    except Exception as e:
        print(f"Error creating Pydantic model: {e}")