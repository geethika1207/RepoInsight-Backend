REPOSITORY_SUMMARY_PROMPT = """

You are generating the Repository Summary section for a GitHub repository.
You have already received the most relevant code and documentation from the repository.
Your task is to write a concise, high-level summary that helps a developer understand the project without reading the entire repository.

Focus only on:
- What the repository implements.
- What problem it solves.
- What the application does.
- Who or what it is built for.
- The overall purpose of the project.

Do NOT explain:
- Architecture
- API design
- Database implementation
- Security
- Code quality
- Documentation quality
- Production readiness
- Improvement suggestions

Those topics are covered in separate reports.

Requirements:
- Write exactly one paragraph.
- Keep the summary between 4 to 6 sentences.
- Use clear, professional language.
- Avoid repeating information.
- Do not assume or invent features that are not supported by the retrieved repository context.
- Do not mention implementation details unless they are essential to understanding the project's purpose.
- Base the summary only on the provided repository content.

Return only the repository summary paragraph.

"""


TECHNOLOGY_STACK_PROMPT = """

You are generating the Technology Stack Overview section for a GitHub repository.

You have already received the most relevant repository files related to the project's technologies.
Your task is to identify every technology used in the repository.
Extract only technologies that are supported by the provided repository context.
Organize the output using the following sections:

- Programming Language
- Backend Framework
- Frontend Framework
- Libraries
- Database
- ORM
- Vector Database
- AI / LLM Models
- Embedding Models
- Authentication
- Cache
- Background Jobs / Queue
- Cloud & Deployment
- External APIs / Services
- Development Tools
- Testing Frameworks

Requirements:
- Return only the technology name for each category.
- Do NOT write explanations or complete sentences.
- Do NOT describe how a technology works.
- Do NOT explain why it is used.
- Do NOT invent technologies that are not present in the repository.
- If a category is not mentioned in the repository, write:
  "Not mentioned in the repository."
- Keep the output clean, short, and easy to scan.
- Base the answer only on the provided repository context.

Example Format:

Programming Language
Python

Backend Framework
FastAPI

Frontend Framework
Not mentioned in the repository.

Libraries
SQLAlchemy
Pydantic
Sentence Transformers

Database
PostgreSQL

ORM
SQLAlchemy

Vector Database
PGVector

AI / LLM Models
Llama 3.3 70B (Groq)

Embedding Models
all-MiniLM-L6-v2

Authentication
JWT

Cache
Redis

Background Jobs / Queue
RQ

Cloud & Deployment
Render

External APIs / Services
Groq API
GitHub API

Development Tools
Docker
Git

Testing Frameworks
Not mentioned in the repository.

"""


ARCHITECTURE_FLOW_PROMPT = """

You are generating the Architecture Flow section for a GitHub repository.
You have already received the most relevant source code and documentation related to the application's architecture.
Your task is to explain how the application works internally by describing the flow of the system from beginning to end.

Focus on:

- Where the application starts.
- How requests enter the application.
- How different layers communicate with each other.
- The execution flow through routers, services, models, utilities, databases, AI models, caching systems, queues, or external services if they exist.
- How data moves through the application until the final response is returned.

Requirements:

- Explain the architecture in the order the flow actually happens.
- Use numbered steps.
- Connect each step using a downward arrow (↓) to make the flow easy to understand.
- Each step should contain 1 to 2 concise sentences explaining its responsibility.
- Keep the explanation clear and easy for developers to understand.
- If a component does not exist in the repository, do not mention it.
- Base the flow only on the retrieved repository content.
- Do not invent missing components.

Do NOT:
- Review the architecture.
- Suggest improvements.
- Discuss code quality.
- Discuss security.
- Discuss production readiness.
- Repeat information.

Return the output in the following format:

Architecture Flow

1. First step
   ↓

2. Second step
   ↓

3. Third step
   ↓

...

After the numbered flow, write a short concluding paragraph (2 to 4 sentences) summarizing how the complete architecture works from request initiation to response generation.

"""


DATABASE_FLOW_PROMPT = """

You are generating the Database Flow section for a GitHub repository.

You have already received the most relevant database-related code and configuration from the repository.
Your task is to explain how data is stored, organized, and retrieved throughout the application.
Focus only on the database layer.

Include:

- The database(s) used.
- The main tables or collections.
- What each table is responsible for storing.
- Relationships between tables, if present.
- How new data is inserted.
- How existing data is updated.
- How data is retrieved.
- How embeddings or vector data are stored, if applicable.
- How semantic search or vector search works, if applicable.
- The complete data storage and retrieval flow from beginning to end.

Requirements:

- Explain the flow in the exact order it happens.
- Use numbered steps.
- Connect every step using a downward arrow (↓).
- Keep each step short and easy to understand.
- Mention only components that actually exist in the repository.
- Do not invent database tables or relationships.
- Base the explanation only on the provided repository context.

Do NOT include:

- Architecture review
- API flow
- Request flow
- Security review
- Code quality review
- Improvement suggestions
- Production readiness

After the numbered flow, write a short conclusion (3 to 5 sentences) explaining how the application's database is structured and how data moves through the database during normal execution.

Return only the Database Flow report.

"""


ARCHUTECTURE_REPORT_PROMPT = """

You are reviewing the software architecture of a GitHub repository.

You have already received the most relevant architecture-related code and documentation from the repository.
Your task is to evaluate the overall software architecture.

Review the architecture based on:

- Project structure
- Separation of concerns
- Layered architecture
- Modularity
- Scalability
- Maintainability
- Dependency management
- Code organization
- Reusability
- Extensibility
- Overall design decisions

Analyze only the provided repository context.

Do not invent missing components.
Do not assume something is wrong simply because it is not implemented.
Only make observations that are supported by the provided repository content.

Return the report in the following format:

## Overall Architecture
Write a concise overview in 2 to 3 sentences describing the overall architecture and design of the project.

## Strengths
Provide 3 to 5 points describing what has been implemented well.
Focus on practical engineering strengths supported by the repository.

## Improvement Suggestions

Provide 3 t0 5 constructive suggestions.
Do not criticize the project unnecessarily.
Only suggest improvements when there is clear evidence from the repository.
For every suggestion, briefly explain why the improvement would be beneficial.

Example style:

• Consider separating business logic from router functions to improve maintainability.
• Consider introducing a service abstraction for database operations to reduce code coupling.
• Consider adding dependency injection for easier testing and scalability.

Keep every suggestion constructive, practical, and supported by the repository context.

Return only the Architecture Review.

"""


DATABASE_REVIEW_PROMPT = """

You are reviewing the database design of a GitHub repository.

You have already received the most relevant database-related code and documentation from the repository.
Your task is to evaluate the overall database implementation.
Review the database based on:

- Database schema design
- Table or collection organization
- Relationships between entities
- Data modeling
- SQLAlchemy or ORM implementation
- Query organization
- CRUD implementation
- Transaction handling
- Database normalization
- Index usage (if present)
- Performance considerations
- Scalability
- Maintainability
- Vector database implementation (if present)
- Embedding storage workflow (if present)

Analyze only the provided repository context.
Do not invent tables, fields, relationships, or database features that are not present.
Do not assume something is incorrect simply because it is missing.
Only make observations supported by the provided repository content.

Return the report in the following format:

## Overall Database Design

Write a concise overview in 2 to 3 sentences describing the overall database design and implementation.

## Strengths

Provide 3 to 5 points describing the strengths of the database implementation.

Focus on practical engineering strengths supported by the repository.

## Improvement Suggestions

Provide 3 to 5 constructive suggestions.

Do not criticize the project unnecessarily.

Only suggest improvements when there is clear evidence from the repository.

For every suggestion, briefly explain why the improvement would be beneficial.

Example style:

• Consider adding indexes to frequently queried columns to improve query performance.
• Consider separating database operations into a dedicated repository layer for better maintainability.
• Consider using transactions for multi-step database operations to improve consistency.
• Consider adding database constraints where appropriate to improve data integrity.

Keep every suggestion practical, concise, and supported by the repository context.

Return only the Database Review.

"""