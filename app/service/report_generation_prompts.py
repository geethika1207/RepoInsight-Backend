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

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "overall_summary" : "..."
}

"""


TECHNOLOGY_STACK_PROMPT = """

You are generating the Technology Stack Overview section for a GitHub repository.

You have already received the most relevant repository files related to the project's technologies.
Your task is to identify every technology used in the repository.
Extract only technologies that are supported by the provided repository context.
Organize the output using the following sections:

programming_language
backend_framework
frontend_framework
libraries
database
orm
vector_database
ai_llm_models
embedding_models
authentication
cache
background_jobs_queue
cloud_deployment
external_apis_services
development_tools
testing_frameworks

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

programming_language
Python

backend_framework
FastAPI

frontend_framework
Not mentioned in the repository.

libraries
SQLAlchemy
Pydantic
Sentence Transformers

database
PostgreSQL

orm
SQLAlchemy

vector_database
PGVector

ai_llm_models
Llama 3.3 70B (Groq)

embedding_models
all-MiniLM-L6-v2

authentication
JWT

cache
Redis

background_jobs_queue
RQ

cloud_deployment
Render

external_apis_services
Groq API
GitHub API

development_tools
Docker
Git

testing_frameworks
Not mentioned in the repository.

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "programming_language" : "...",
   "backend_framework" : "...",
   "frontend_framework" : "...",
   "libraries" : [...],
   "database" : "...",
   "orm" : "...",
   "vector_database" : "...",
   "ai/llm_models" : [...],
   "embedding_model" : "...",
   "authentication" : "...",
   "cache" : "...",
   "bachground_jobs queue" : "...",
   "cloud & deployment" : "...",
   "external api's / services" : [...],
   "development tools" : [...],   
   "testing frameworks" : [...]
}

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

- Explain the architecture in the exact order it executes.
- Return the flow as an array where each array element represents ONE step only.
- Each step should be short (1 to 2 concise sentences).
- Do NOT include the arrow (↓) inside the JSON.
- The frontend will display the arrows between the array items.
- Mention only components that exist in the repository.
- Base the explanation only on the provided repository context.
- Do not invent missing components.

Do NOT:
- Review the architecture.
- Suggest improvements.
- Discuss code quality.
- Discuss security.
- Discuss production readiness.
- Repeat information.

Architecture Summary : 

After the numbered flow, write a short concluding paragraph (2 to 4 sentences) summarizing how the complete architecture works from request initiation to response generation.

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.


{
  "architecture_flow": [
    "...",
    "...",
    "..."
  ],
  "architecture_summary": "..."
}

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

Datbase summary : 

After the numbered flow, write a short conclusion (3 to 5 sentences) explaining how the application's database is structured and how data moves through the database during normal execution.

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "database_flow" : [...],
   "database_summary" : "..."
}

"""


ARCHITECTURE_REPORT_PROMPT = """

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

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.


{
   "overall_architecture" : "...",
   "strengths" : [...],
   "improvement_suggestions" : [...]
}

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

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "overall_database_design" : "...",
   "strengths" : [...],
   "improvement_suggestions" : [...]
}

"""


SECURITY_REVIEW_PROMPT = """

You are generating the Security Review section for a GitHub repository.

You have already received the relevant repository files related to security.
Evaluate the repository from a security perspective.

Review the following areas:

- Authentication implementation
- Authorization and access control
- JWT or session handling
- Password hashing and storage
- Secret management
- Environment variable usage
- Hardcoded API keys, passwords, secrets or tokens
- Presence of .env or other sensitive configuration files
- SQL Injection protection
- Input validation
- File upload validation (if present)
- CORS configuration
- Sensitive data exposure
- Error handling and information leakage
- Overall backend security practices

If a .env file, API key, secret token, database password, JWT secret, private key, or any sensitive credential is found inside the repository, clearly mark it as a **Critical Security Issue** and recommend removing it immediately.

If a security feature is not present in the repository even f it is required , state:
"Not implemented in the repository."

Return the response in this format:

## Overall Security
Write 2 to 3 sentences describing the overall security level of the project.

## Strengths
Provide 3 to 5 security strengths found in the repository.

## Improvement Suggestions
Provide 3 to 5 practical security recommendations based only on the repository content.

Do not invent issues that are not present.
Do not mention architecture, database, API quality, or production readiness.
Base your review only on the provided repository files.

Return only the Security Review.

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "security_review" : "...",
   "strengths" : [...],
   "improvement_suggestions" : [...]
}

"""


PRODUCTION_READINESS_PROMPT = """

You are generating the Production Readiness Review for a GitHub repository.

You have already received the repository files that are relevant to production readiness.
Evaluate whether this project is ready to be deployed and maintained in a real production environment.

Review the repository for the following:

- Environment variable management
- Configuration management
- Logging implementation
- Error handling
- Exception handling
- Deployment configuration
- Docker or containerization support
- Performance optimizations
- Caching implementation
- Background job processing
- Scalability considerations
- Health check endpoints
- Monitoring or observability support
- Testing (unit, integration, API tests)
- Dependency management
- Reliability and maintainability
- Production best practices

If a feature is not implemented or cannot be found in the repository even if it is required , clearly state:
"Not implemented in the repository."

Return the response in the following format:

## Overall Production Readiness
Write 2 to 3 sentences describing how ready this project is for production deployment.

## Strengths
Provide 3 to 5 production-ready practices already implemented in the repository.

## Improvment Suggestions
Provide 3 to 5 practical recommendations that would improve the project's production readiness.

Rules:
- Base your review only on the provided repository content.
- Do not invent features that are not present.
- Do not discuss API quality, database design, architecture, security, or documentation unless they directly affect production readiness.
- Keep the suggestions practical and actionable.
- Return only the Production Readiness Review.

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "production_readiness" : "...",
   "strengths" : [...],
   "improvement_suggestions" : [...]
}

"""


DOCUMENTATION_REVIEW_PROMPT = """

You are generating the Documentation Review for a GitHub repository.

You have already received the repository files related to documentation.
Your primary source should be README.md.

If README.md is not present, use other documentation files such as:

- docs/
- CONTRIBUTING.md
- INSTALL.md
- SETUP.md
- Any other documentation-related files found in the repository.

If README.md is not found, clearly mention:
"README.md was not found in the repository. This review is based on the available documentation files and repository structure."

If no documentation files are found, clearly mention:
"No documentation files were found in the repository. This review is generated using the available repository structure only."

Evaluate the documentation based on:

- Project overview
- Installation guide
- Setup instructions
- Usage instructions
- Configuration guide
- Environment variable documentation
- API documentation
- Project structure explanation
- Contribution guidelines
- Examples or screenshots
- Overall clarity
- Completeness
- Ease of understanding for a new developer

Return the report in the following format:

## Overall Documentation

Write 2 to 3 sentences describing the overall quality and completeness of the documentation.

## Strengths

Provide 3 to 5 strengths found in the documentation.

## Improvement Suggestions

Provide 3 to 5 practical suggestions to improve the documentation.

Rules:

- Base your review only on the provided repository content.
- Do not invent documentation that does not exist.
- If a section is missing, simply state that it is not documented.
- Do not evaluate the source code itself unless it is necessary to understand the documentation.
- Keep the suggestions practical and concise.

Return only the Documentation Review.

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "documentation_review" : "...",
   "strengths" : [...],
   "improvement_suggestions" : [...]
}


"""


CODE_QUALITY_PROMPT = """

You are generating the Code Quality Review for a GitHub repository.

You have already received the most relevant source code from the repository.
Your task is to evaluate the overall quality of the codebase.

Review the code based on:

- Readability
- Naming conventions
- Code organization
- Modularity
- Reusability
- Function complexity
- Class design
- Code duplication
- Maintainability
- Consistency
- Best coding practices
- Error handling
- Comments and documentation
- Overall implementation quality

Analyze only the provided repository content.

Do not invent issues that are not present.
Do not review architecture, database design, API design, security, production readiness, or documentation.

Return the response in the following format:

## Overall Code Quality

Write 2 to 3 sentences describing the overall quality of the codebase.

## Strengths

Provide 3 to 5 strengths found in the implementation.

Focus only on strengths supported by the repository.

## Improvement Suggestions

Provide 3 to 5 practical suggestions that would improve the code quality.

For every suggestion:

- Explain what can be improved.
- Briefly explain why the improvement is beneficial.
- Suggest practical coding best practices when applicable.

Examples:

• Consider using more descriptive variable and function names to improve code readability.
• Consider extracting repeated logic into reusable helper functions to reduce code duplication.
• Consider adding type hints or docstrings to improve maintainability.
• Consider reducing large functions into smaller reusable functions to improve readability.

Keep every suggestion concise, practical, and supported by the repository context.

Return only the Code Quality Review.

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "code quality_review" : "...",
   "strengths" : [...],
   "improvement_suggestions" : [...]
}


"""


CONTRIBUTIONS_PROMPT = """
You are generating the Contribution Opportunities report for a GitHub repository.

You have already received the repository files that are relevant for identifying possible contributions.

Your task is to identify practical contribution opportunities for developers with different experience levels.

Classify every contribution into one of the following categories:

Beginner : 

These tasks should require minimal understanding of the repository and can usually be completed within 30 minutes to 2 hours.

Examples include:
- Missing comments or docstrings
- TODO comments
- Typo fixes
- README improvements
- Documentation improvements
- Small bug fixes
- Simple validation improvements
- Renaming unclear variables or functions
- Removing dead code
- Adding logging
- Minor refactoring

Intermediate : 

These tasks require understanding one module or feature of the project and may take several hours or a few days.

Examples include:
- Refactoring duplicated code
- Improving database queries
- Adding a missing API endpoint
- Improving authentication flow
- Adding caching
- Improving error handling
- Writing unit tests
- Performance improvements
- Completing partially implemented features

Advanced : 

These tasks require understanding multiple modules or the overall project architecture and may take several days.

Examples include:
- Large feature development
- Architecture redesign
- Database migration
- Background job systems
- Distributed systems
- Streaming or WebSocket support
- AI pipeline improvements
- Performance optimization across multiple modules
- Security redesign

Return the report in the following format:

## Beginner Contributions

Provide 3 to 5 beginner-friendly contribution ideas.

For each contribution include:
- Estimated effort (for example: 30 to 60 minutes)
- What should be improved
- Why it is a good beginner task

## Intermediate Contributions

Provide 3 to 5 intermediate contribution ideas.

For each contribution include:
- Estimated effort (for example: 4 to 8 hours)
- What should be improved
- Why it requires intermediate knowledge

## Advanced Contributions

Provide 3 to 5 advanced contribution ideas.

For each contribution include:
- Estimated effort (for example: 2 to 5 days)
- What should be improved
- Why it requires advanced knowledge

If no valid contribution opportunities are found for a category, clearly state:

"There are no Beginner Contributions in this repository."
"There are no Intermediate Contributions in this repository."
"There are no Advanced Contributions in this repository."

Do not invent contribution ideas just to fill the section.

Rules:

- Base every suggestion only on the provided repository content.
- Do not invent features or issues that are not present.
- Classify tasks based on the amount of repository knowledge required, not the number of lines of code.
- Suggestions should be practical, specific, and actionable.
- Avoid generic advice such as "improve the project" or "write better code."
- Return only the Contribution Opportunities report.

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Do not add additional fields.
Return only the keys shown below.

{
   "beginner_contributions" : [...],
   "intermediate_contributions" : [...],
   "advanced_contributions" : [...]
}

"""