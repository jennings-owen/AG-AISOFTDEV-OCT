# ADR-[Number]: [Brief Decision Description]

- **Date**: `[YYYY-MM-DD]`
- **Author(s)**: `[List of authors, e.g., Jane Doe, John Smith]`
- **Stakeholders**: `[List of stakeholders, e.g., Engineering Lead, Product Manager, Security Team]`

## Status

`[Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-XXX]`

*This section should be updated as the ADR moves through its lifecycle. Definitions:*
- *`Proposed`: This decision is under review.*
- *`Accepted`: This decision has been approved and should be followed.*
- *`Rejected`: This decision was proposed but not approved.*
- *`Deprecated`: This decision was once accepted but is no longer recommended.*
- *`Superseded by ADR-XXX`: This decision has been replaced by a new one. Link to the new ADR.*

## Context

*This section describes the problem, technical and business forces, constraints, and requirements that led to this decision. It should set the stage and explain the "why" behind it.*

**Problem Statement:**
[Describe the issue that needs to be addressed or the goal to be achieved. What is the problem we are trying to solve? For example, "Our current authentication system does not support multi-factor authentication, which is a new security requirement."]

**Driving Forces & Constraints:**
- **[Force/Constraint 1]:** [e.g., A business requirement for 99.9% uptime.]
- **[Force/Constraint 2]:** [e.g., The team's existing expertise in a particular technology stack.]
- **[Force/Constraint 3]:** [e.g., A project deadline or budget constraint.]
- **[Force/Constraint 4]:** [e.g., A non-functional requirement like system performance or security compliance.]

## Decision

*This section clearly and concisely states the final decision. This is the "what" of the ADR.*

We will adopt **[Chosen Option or Technology]** to solve the problem.

**Justification:**
[Explain why this option was chosen over others. Reference the context and constraints mentioned above. Be specific. For example, "This option was chosen because it fully supports our security requirements, has a strong open-source community, and integrates well with our existing infrastructure, despite a slightly steeper learning curve."]

**Implementation Details:**
- **[Key Detail 1]:** [e.g., We will use version X.Y.Z of the library.]
- **[Key Detail 2]:** [e.g., The service will be configured with the following specific settings.]
- **[Key Detail 3]:** [e.g., This pattern will be applied to all new microservices handling user authentication.]

## Consequences

*This section describes the resulting context after the decision is implemented. It should include both positive and negative outcomes, trade-offs, and any future implications.*

**Positive Consequences:**
- **[Benefit 1]:** [e.g., Improved system performance by an estimated 20%.]
- **[Benefit 2]:** [e.g., Faster development cycles for new features due to a simpler API.]
- **[Benefit 3]:** [e.g., Alignment with the company's long-term technology strategy.]

**Negative Consequences & Trade-offs:**
- **[Drawback 1]:** [e.g., Increased operational complexity and a new system to monitor.]
- **[Drawback 2]:** [e.g., Requires a one-time training effort for the development team.]
- **[Drawback 3]:** [e.g., Introduces a new dependency, which carries a licensing cost or a security risk.]

**Future Implications:**
- [Describe any follow-up work, potential future decisions this decision influences, or how this decision might need to be revisited. For example, "This decision will require us to update our CI/CD pipeline and monitoring dashboards. We should plan to review the performance and cost implications in 6 months."]