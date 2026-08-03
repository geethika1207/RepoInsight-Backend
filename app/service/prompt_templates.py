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
Retrieve the repository content required to understand the overall architecture and application flow.

Focus on:
- application entry points
- request flow
- routing
- controllers
- services
- business logic
- utilities
- models
- database layer
- folder structure
- dependency relationships
- communication between components
- application startup
- data flow between modules

The goal is to retrieve the repository content needed to explain how the application works from start to finish.
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
Retrieve the code related to the database layer of this repository.

Focus on:
- database models
- schemas
- tables or collections
- relationships between tables
- SQLAlchemy or ORM implementation
- CRUD operations
- how data is inserted
- how data is updated
- how data is retrieved
- query execution
- transactions
- migrations
- vector database usage (if present)
- embedding storage (if present)
- semantic search workflow (if present)

The goal is to explain how data is stored, organized, and retrieved inside the database from beginning to end.
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
Retrieve the repository documentation required to evaluate the project documentation.

Focus primarily on:
- README.md

Also retrieve other documentation files when available, including:
- docs/
- CONTRIBUTING.md
- INSTALL.md
- SETUP.md
- Any other documentation-related files

Focus on documentation related to:

- project overview
- installation instructions
- setup guide
- usage examples
- API documentation
- project structure explanation
- environment configuration
- contribution guide
- completeness
- clarity

Avoid retrieving normal source code unless it is directly required to understand the documentation.
"""


CODE_QUALITY_REVIEW_QUERY = """
Retrieve the repository implementation required to evaluate the overall code quality.

Focus on:
- readability
- naming conventions
- code organization
- modularity
- reusability
- code duplication
- maintainability
- function complexity
- class design
- consistency
- error handling
- comments
- coding best practices

The goal is to retrieve the repository content required to evaluate how well the code is written and implemented.
"""


CONTRIBUTION_QUERY = """
Retrieve the repository implementation required to identify contribution opportunities.

Focus on:
- unfinished modules
- TODO comments
- FIXME comments
- missing features
- feature gaps
- repetitive code
- duplicated logic
- refactoring opportunities
- optimization opportunities
- missing documentation
- missing comments or docstrings
- missing unit or integration tests
- placeholder implementations
- partially implemented functionality
- code marked for future improvements
- technical debt

The goal is to retrieve the repository content required to identify contribution opportunities suitable for:
- Beginner developers
- Intermediate developers
- Advanced developers

"""