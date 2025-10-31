# ADR-001: Database Selection for Vector Search and Relational Data

- **Date**: `2023-10-30`
- **Author(s)**: `Staff Software Engineer`
- **Stakeholders**: `Engineering Lead, Product Manager, DevOps Team, Security Team`

## Status

`Accepted`

*This decision has been approved and should be followed.*

## Context

**Problem Statement:**
The Ascend Onboarding Platform requires a database solution that can manage both highly structured, relational data (users, learning paths, progress) and support vector similarity search. This dual requirement is driven by the need for a robust transactional backend and new AI-powered features, starting with a "searchable resource library" (Story 1.4), which relies on semantic search over document embeddings. The challenge is to select an architecture that fulfills both needs without introducing unnecessary complexity or cost.

**Driving Forces & Constraints:**
- **Dual Data Model Requirement:** The system must efficiently store and query both traditional relational data and high-dimensional vector embeddings.
- **Data Integrity and Security:** As the system will handle sensitive employee and HR data (Story 1.5), ACID compliance, transactional integrity, and a mature security model are non-negotiable requirements.
- **Performance at Scale:** The solution must provide sub-second query latency for both relational lookups and vector searches for a projected scale of 5,000 annual users and 500 concurrent sessions.
- **Operational Simplicity:** To maintain development velocity and control costs, the chosen architecture should minimize operational overhead related to deployment, monitoring, backups, and maintenance.
- **Developer Experience:** The solution should be easy for the development team to adopt and use, ideally leveraging existing skills (like SQL) and simplifying application logic.

## Decision

We will adopt **PostgreSQL with the `pgvector` extension** as the single, primary database for the Ascend Onboarding Platform.

**Justification:**
This decision was made after a detailed comparison with a dual-database approach (a relational database plus a specialized vector database). PostgreSQL with `pgvector` is the superior choice for our current and foreseeable needs for the following reasons:

1.  **Unified Architecture:** It eliminates the significant architectural and operational complexity of managing two separate database systems. This simplifies development, deployment, monitoring, backups, and security, directly addressing our constraint for operational simplicity.
2.  **Simplified & Powerful Queries:** It allows us to combine relational filters and vector similarity searches within a single, atomic SQL query. For example, we can filter search results based on a user's role or department (stored in a relational table) in one efficient operation. This avoids the latency and complexity of a two-step query process required by a dual-database setup.
3.  **Cost-Effectiveness:** Consolidating into a single managed PostgreSQL instance results in a significantly lower Total Cost of Ownership (TCO) by reducing infrastructure hosting costs and the engineering hours required for maintenance.
4.  **Maturity and Reliability:** We gain the full benefits of PostgreSQL's decades of development, including robust ACID compliance, transactional integrity, and a world-class security model. This is critical for the core functionality of the platform and for handling sensitive HR data.
5.  **Sufficient Performance and Scalability:** The research findings confirm that `pgvector` provides excellent performance for our projected scale (thousands to low millions of vectors), meeting our sub-second query requirements. PostgreSQL's well-established scaling patterns (vertical scaling, read replicas) provide a clear path for future growth.

**Implementation Details:**
- **Hosting:** We will use a managed PostgreSQL service (e.g., AWS RDS, Google Cloud SQL) to offload administrative overhead.
- **Extension:** The `pgvector` extension will be enabled on the database instance.
- **Schema:** Vector data will be stored in a `vector(n)` column, where `n` is the dimensionality of the model's embeddings.
- **Indexing:** We will use an HNSW (Hierarchical Navigable Small World) index on vector columns to ensure fast and efficient approximate nearest neighbor (ANN) searches.

## Consequences

**Positive Consequences:**
- **Reduced Complexity:** A single data store simplifies the application's data access layer and reduces the cognitive load on developers.
- **Faster Development:** Teams can move faster as they do not need to build or maintain data synchronization logic between two different databases.
- **Lower TCO:** Infrastructure and operational costs will be significantly lower compared to running and managing two database systems.
- **Enhanced Data Integrity:** Keeping all related data in a single transactional system eliminates the risk of data drift or inconsistency between a relational and vector database.

**Negative Consequences & Trade-offs:**
- **Potential Resource Contention:** Intensive vector operations (like index building) could potentially impact the performance of standard transactional queries. This risk will be mitigated through proper instance sizing, resource monitoring, and scheduling intensive operations during off-peak hours.
- **Team Upskilling:** The development team will require training on the specific features of `pgvector` and best practices for vector indexing and querying.
- **Not Hyper-Specialized:** While performant, `pgvector` may not match the raw query-per-second (QPS) of a specialized vector database at extreme scales (billions of vectors). This is an acceptable trade-off, as our current and projected scale is well within `pgvector`'s capabilities.

**Future Implications:**
- Our database monitoring strategy must be enhanced to include metrics specific to vector index health and search query performance.
- This decision establishes PostgreSQL as the central data platform. Future features requiring new data types will be evaluated for their compatibility with the PostgreSQL ecosystem first.
- We should plan to review this decision if the vector data grows exponentially beyond millions of records or if vector search performance becomes a system-wide bottleneck, at which point a hybrid or specialized solution could be reconsidered.