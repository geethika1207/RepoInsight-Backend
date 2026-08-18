REPOSITORY_SUMMARY_QUERY = """
Retrieve the repository content that best explains what this project is.

Highest priority:
- README.md
- Project overview
- Introduction
- Repository description
- Documentation explaining the purpose of the project

If those are unavailable, retrieve source code that clearly reveals:

- the application's primary purpose
- the main workflow
- who the application is built for
- the problem it solves
- the major capabilities exposed by the repository

Prioritize high-level descriptions over implementation details.

The goal is to retrieve enough context to understand the project without reading the entire repository.
"""

TECHNOLOGY_STACK_QUERY = """
# Technology Stack and Dependencies

## Built With / Technical Overview
This project is built using the following core technologies, frameworks, and libraries:

| Category | Specification |
|---|---|
| Programming Language | Core language used for development |
| Backend Framework | Primary server and API framework |
| Frontend Framework | User interface and client framework |
| Database | Main relational or NoSQL data storage |
| Vector Database | Semantic search and embedding storage |
| ORM | Object-relational mapping library |
| AI Models | Large language models and APIs |
| Embedding Model | Text vectorization model |
| Authentication | Security, JWT, and user login handling |
| Deployment | Cloud hosting and containerization platform |

<!-- Badges and Shields -->
![Language](https://img.shields.io/badge/language-blue)
![Framework](https://img.shields.io/badge/framework-green)
![Database](https://img.shields.io/badge/database-purple)

## Dependencies (requirements.txt / package.json / pyproject.toml / Dockerfile)
List of imported libraries, caching layers, job queues, external APIs, and testing frameworks required to run the application environment.
"""


ARCHITECTURE_FLOW_QUERY = """
Retrieve the repository files required to reconstruct the application's actual execution flow.

Prioritize files that contain the application's runtime flow, including:
- application entry point
- startup logic
- routers and API endpoints
- controllers and services
- core business logic and workflows
- middleware and dependency injection
- authentication and authorization flow
- database interactions and data pipelines
- background workers and asynchronous tasks

Retrieve enough connected code so the complete execution path can be reconstructed from the first incoming request until the final response.

Avoid retrieving isolated utility files that are never used during execution.
"""


ARCHITECTURE_REVIEW_QUERY = """
Retrieve repository content that best represents the overall software architecture.

Prioritize:
- folder structure and project layout
- module and feature organization
- separation of concerns
- routers, services, and controllers
- dependency injection and middleware
- architectural patterns
- reusable modules and abstractions
- business logic organization

Retrieve enough evidence to evaluate architectural decisions rather than individual functions.

Avoid retrieving unrelated utility implementations unless they illustrate architectural organization.
"""


DATABASE_FLOW_QUERY = """
Retrieve repository files that describe how application data moves through the database during execution.

Prioritize:
- ORM models and entity classes
- schema definitions
- repositories and data access layers
- CRUD services and state management
- core business entity creation workflows
- data update and deletion operations
- data retrieval and reporting logic

Retrieve the complete lifecycle of data:
creation -> storage -> updates -> retrieval -> final usage.

The goal is to reconstruct the application's business data workflow rather than explaining ORM usage.
"""


DATABASE_REVIEW_QUERY = """
Retrieve repository content required to evaluate the database implementation.

Prioritize:
- ORM models and entity definitions
- database schema and migrations
- relationships (One-to-Many, Many-to-Many)
- repositories and data access logic
- CRUD implementations
- complex query implementations
- transaction handling
- indexes and constraints

Retrieve enough evidence to review:
- schema organization and data modeling
- entity relationships and consistency
- maintainability and database design quality
- separation of the persistence layer from business logic

Avoid retrieving unrelated application logic.
"""


SECURITY_REVIEW_QUERY = """
Retrieve repository content related to implemented security mechanisms.

Prioritize:

- authentication implementation
- authorization
- JWT handling
- password hashing
- login flow
- middleware
- dependency injection
- environment variables
- configuration
- CORS
- secret management
- permission checks
- protected endpoints
- input validation
- upload validation
- exception handling
- API key usage

Retrieve code that demonstrates security implementation, potential vulnerabilities, or missing protections.

Avoid retrieving unrelated business logic.
"""

PRODUCTION_REVIEW_QUERY = """
Retrieve repository content related to production deployment and operational readiness.

Prioritize:

- deployment configuration
- Docker
- Render
- Vercel
- startup configuration
- logging
- exception handling
- environment configuration
- configuration management
- health endpoints
- worker processes
- background jobs
- caching
- monitoring
- scalability
- production settings

Retrieve implementation that directly impacts deploying or operating the application in production.

Avoid generic application code.
"""

DOCUMENTATION_REVIEW_QUERY = """
Retrieve the project's documentation files and configuration guides required to understand, install, and run the application.

Prioritize finding:
- README.md and high-level project overviews
- Installation, setup, and deployment instructions
- Technology stack and requirements definitions
- API documentation and usage guides
- Environment variable configurations
- Contribution guidelines
- Markdown tables summarizing project features, endpoints, or dependencies
- Project badges and shields (e.g., build status, tech stack, versions)

Retrieve evidence that explains:
- What the project does
- How to start the application locally
- How the project is structured
- How a new developer should interact with the codebase

If standard text explanations are sparse or unavailable, explicitly retrieve markdown tables and badge links that visually convey the project's technology stack and status.

Avoid retrieving backend source code unless it contains massive docstrings explaining the overall project setup.
"""


CONTRIBUTION_QUERY = """
Retrieve repository content that reveals realistic contribution opportunities.

Prioritize evidence such as:

- TODO
- FIXME
- placeholder implementations
- NotImplemented
- pass statements
- incomplete modules
- duplicated logic
- repeated code
- feature gaps
- commented-out functionality
- missing validation
- missing error handling
- partially implemented workflows
- unimplemented endpoints
- inconsistent implementations
- technical debt
- areas marked for future work

Also retrieve implementation where architectural reviews, database reviews, security reviews, production reviews, or code quality reviews indicate concrete improvement opportunities.

The goal is to retrieve repository evidence that can be transformed into beginner, intermediate, and advanced contribution ideas.

Do not retrieve generic project files that contain no actionable improvement opportunities.
"""