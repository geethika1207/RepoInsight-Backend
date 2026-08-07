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
Retrieve repository files that explicitly declare technologies used by the project.

Highest priority:

- requirements.txt
- pyproject.toml
- package.json
- poetry.lock
- Pipfile
- Dockerfile
- docker-compose.yml
- render.yaml
- vercel.json
- README.md
- environment configuration
- import statements
- initialization files

Retrieve evidence for:

- programming language
- frameworks
- libraries
- databases
- ORMs
- authentication
- cache
- queues
- AI models
- embedding models
- vector databases
- deployment platforms
- external APIs
- development tools
- testing frameworks

Only retrieve files that directly prove the technology exists.
"""

ARCHITECTURE_FLOW_QUERY = """
Retrieve the repository files required to reconstruct the application's actual execution flow.

Prioritize files that contain the application's runtime flow, including:

- application entry point
- startup logic
- routers
- endpoints
- controllers
- services
- business logic
- middleware
- dependency injection
- authentication flow
- AI pipeline
- database interactions
- cache usage
- background workers
- utilities invoked during request execution

Retrieve enough connected code so the complete execution path can be reconstructed from the first incoming request until the final response.

Avoid retrieving isolated utility files that are never used during execution.
"""

ARCHITECTURE_REVIEW_QUERY = """
Retrieve repository content that best represents the overall software architecture.

Prioritize:

- folder structure
- module organization
- routers
- services
- controllers
- dependency injection
- middleware
- project layout
- architectural patterns
- reusable modules
- business logic organization

Retrieve enough evidence to evaluate architectural decisions rather than individual functions.

Avoid retrieving unrelated utility implementations unless they illustrate architectural organization.
"""

DATABASE_FLOW_QUERY = """
Retrieve repository files that describe how application data moves through the database during execution.

Prioritize:

- ORM models
- schema definitions
- repositories
- CRUD services
- interview creation flow
- user creation flow
- response storage
- analysis generation
- history retrieval
- update operations

Retrieve the complete lifecycle of data:

creation
↓

storage

↓

updates

↓

retrieval

↓

final usage

The goal is to reconstruct the application's database workflow rather than explaining ORM usage.
"""

DATABASE_REVIEW_QUERY = """
Retrieve repository content required to evaluate the database implementation.

Prioritize:

- ORM models
- database schema
- relationships
- repositories
- CRUD implementations
- migrations
- query implementations
- transaction handling
- indexes
- constraints

Retrieve enough evidence to review:

- schema organization
- data modeling
- entity relationships
- maintainability
- consistency
- database design quality

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
Retrieve repository documentation for evaluating documentation quality.

Highest priority:

- README.md

Then retrieve:

- docs/
- CONTRIBUTING.md
- INSTALL.md
- SETUP.md
- API documentation
- architecture documentation
- deployment documentation

Retrieve documentation describing:

- project overview
- installation
- setup
- usage
- configuration
- API usage
- contribution process
- project structure

Avoid retrieving implementation code unless documentation references it directly.
"""

CODE_QUALITY_REVIEW_QUERY = """
Retrieve representative source code from across the repository for evaluating overall code quality.

Prioritize code that represents:

- routers
- services
- business logic
- models
- utilities
- authentication
- database access
- AI modules

Retrieve enough code to evaluate:

- organization
- consistency
- naming
- modularity
- duplication
- maintainability
- complexity
- reuse

The retrieved code should represent the repository as a whole rather than isolated files.
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