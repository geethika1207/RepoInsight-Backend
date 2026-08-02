REPOSITORY_SUMMARY_QUERY = """
Analyze this GitHub repository and generate a complete repository summary.

Focus on:
- The overall purpose of the project.
- The main problem it solves.
- The technologies and frameworks used.
- The overall project structure.
- The important modules and how they work together.
- The workflow of the application from start to finish.
- Any AI models, APIs, databases, caching systems, queues, or external services used.
- Overall architecture at a high level.

The summary should help someone understand the complete repository without reading every file.

Return a structured repository summary.
"""


TECHNOLOGY_STACK_QUERY = """
What technologies are used in this repository?

Identify the complete technology stack, including:

- Programming languages
- Backend frameworks
- Frontend frameworks
- Libraries and packages
- Databases
- ORMs
- AI / LLM models
- Embedding models
- Vector databases
- Cache systems
- Background job queues
- Authentication libraries
- SDKs
- Cloud services
- Deployment platforms
- External APIs or third-party services
- Testing frameworks
- DevOps tools

Retrieve the repository files that contain information about these technologies.
"""


ARCHITECTURE_FLOW_QUERY = """
Retrieve the code that explains the overall architecture of this repository.

Focus on:
- application entry points
- request flow
- routing
- services
- business logic
- utilities
- models
- database layer
- folder organization
- dependency relationships
- communication between components

The goal is to explain how data moves through the entire application from start to finish.
"""


ARCHITECTURE_REVIEW_QUERY = """
Retrieve the parts of the repository required to evaluate the software architecture.

Focus on:
- modularity
- separation of concerns
- scalability
- maintainability
- folder organization
- code organization
- dependency management
- project structure
- design decisions

The goal is to review the architecture and identify strengths, weaknesses, and possible improvements.
"""


DATABASE_FLOW_QUERY = """
Retrieve the code responsible for database operations.

Focus on:
- models
- schemas
- repositories
- CRUD operations
- database relationships
- migrations
- SQLAlchemy usage
- transactions
- queries
- how data is stored
- how data is retrieved
- how data moves through the application

The goal is to explain the complete database workflow.
"""


DATABASE_REVIEW_QUERY = """
Retrieve the database-related code required to evaluate the database design.

Focus on:
- schema design
- normalization
- relationships
- constraints
- indexes
- query efficiency
- ORM usage
- transaction handling
- scalability
- security

The goal is to review the database implementation and identify improvements.
"""


API_FLOW_QUERY = """
Retrieve the implementation related to APIs.

Focus on:
- routers
- endpoints
- request handling
- response handling
- dependency injection
- authentication
- middleware
- service calls
- validation
- business logic

The goal is to explain how API requests travel through the backend.
"""


API_REVIEW_QUERY = """
Retrieve the code required to evaluate the API implementation.

Focus on:
- endpoint design
- REST practices
- request validation
- response consistency
- status codes
- authentication
- authorization
- error handling
- scalability
- maintainability

The goal is to review the API quality and identify possible improvements.
"""


SECURITY_REVIEW_QUERY = """
Retrieve the implementation related to application security.

Focus on:
- authentication
- authorization
- JWT handling
- password hashing
- secrets management
- environment variables
- SQL injection prevention
- input validation
- API protection
- file handling
- sensitive data exposure

The goal is to evaluate the security practices used throughout the repository.
"""


PRODUCTION_REVIEW_QUERY = """
Retrieve the implementation that determines whether this project is production ready.

Focus on:
- logging
- exception handling
- configuration management
- deployment support
- Docker
- environment configuration
- scalability
- monitoring
- caching
- background jobs
- testing
- performance optimization

The goal is to evaluate how close the repository is to production deployment.
"""


DOCUMENTATION_REVIEW_QUERY = """
Retrieve documentation related to this repository.

Focus primarily on README.md.

Only retrieve other documentation files if README.md does not contain sufficient information.

Evaluate:
- installation instructions
- project overview
- usage examples
- API documentation
- setup guide
- project structure explanation
- contribution guide
- completeness
- clarity

Ignore normal source code unless it is necessary to understand missing documentation.
"""


CODE_QUALITY_REVIEW_QUERY = """
Retrieve the implementation required to evaluate overall code quality.

Focus on:
- readability
- naming conventions
- code organization
- duplication
- maintainability
- function complexity
- class design
- consistency
- best practices
- comments
- modularity

The goal is to review the overall quality of the codebase.
"""


IMPROVEMENT_QUERY = """
Retrieve the repository implementation that can help identify improvements.

Focus on:
- missing features
- incomplete modules
- scalability issues
- maintainability
- performance
- security
- documentation
- architecture
- API improvements
- database improvements

The goal is to generate practical improvement suggestions for the project.
"""


CONTRIBUTION_QUERY = """
Retrieve the implementation required to identify possible contribution opportunities.

Focus on:
- unfinished modules
- TODOs
- repetitive code
- missing documentation
- missing tests
- feature gaps
- refactoring opportunities
- optimization opportunities

The goal is to generate contribution ideas for:
- Beginner developers
- Intermediate developers
- Advanced developers
"""