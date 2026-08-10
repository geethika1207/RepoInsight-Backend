# RepoInsight

## An AI Repository Intelligence System for Automated Codebase Analysis

> **Why I'm building this:** Onboarding onto a new codebase takes hours of manual tracing. I am building RepoInsight as an active project to automate this process. It takes any public GitHub repository and generates a structured intelligence report covering architecture, security, database design, and contribution zones, without a developer having to read every file from scratch.

RepoInsight is an AI-powered repository analysis platform designed to bridge the gap between raw source code and actionable engineering understanding. Instead of manually tracing through files, the platform clones a repository, semantically indexes its contents, and generates a multi-section report that explains what the project does, how it's built, and where it can be improved.

To make this work, I built a Retrieval-Augmented Generation (RAG) pipeline that handles repository ingestion, sliding-window chunking, vector embedding generation, and similarity retrieval. This setup ensures that the LLM grounds its analysis strictly in real source-code files, keeping the generated reports evidence-based and free of hallucinations.

---

## 🛠️ Built With

![Python](https://img.shields.io/badge/Python-3.11+-blue)

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)

![pgvector](https://img.shields.io/badge/pgvector-Vector%20Search-6E56CF)

![Groq](https://img.shields.io/badge/Groq-Llama--3.3--70B-orange)

![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-Embeddings-yellow)

![Architecture](https://img.shields.io/badge/Architecture-RAG--Pipeline-ff6b35)

![License](https://img.shields.io/badge/License-MIT-yellow)

![Status](https://img.shields.io/badge/Status-Active-success)

![Analysis](https://img.shields.io/badge/Analysis-Repository--Wide-blueviolet)

---

## Technical Overview

| Category | Specification |
|-----------|---------------|
| Project Type | AI Repository Intelligence System |
| Primary Language | Python 3.11 |
| Backend Framework | FastAPI |
| Communication Protocol | REST API |
| Repository Ingestion | Git (subprocess-based cloning) |
| Embedding Model | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Storage | PostgreSQL + pgvector |
| Large Language Model | Groq API (Llama 3.3 70B Versatile) |
| Retrieval Strategy | Cosine-Similarity Chunk Retrieval |
| Concurrency Model | `asyncio.gather()` for parallel retrieval & LLM report generation |
| State Management | Per-Repository Chunk & Report Orchestration |
| Data Storage | PostgreSQL |
| Authentication | JWT Authentication |

---

## 🏗 System Architecture

RepoInsight is built on a **retrieval-augmented pipeline architecture** that separates repository ingestion, semantic indexing, context retrieval, and report generation into independent stages. Each stage is responsible for a single transformation — from raw source files to a fully structured, evidence-grounded report — resulting in a modular and extensible analysis pipeline.

```text
GitHub URL
    │
    ▼
Clone Repository (subprocess)
    │
    ▼
Extract Supported Files (filtered by extension)
    │
    ▼
Chunk Files (fixed size, overlapping windows)
    │
    ▼
Generate Embeddings (sentence-transformers)
    │
    ▼
Store Chunks + Embeddings (PostgreSQL / pgvector)
    │
    ▼
Retrieve Relevant Chunks (cosine similarity, per category)
    │
    ▼
Combine Chunks + Prompt Templates
    │
    ▼
LLM Report Generation (Groq Llama 3.3 70B)
    │
    ▼
Structured JSON Report
```

**Figure 1.** End-to-end retrieval-augmented pipeline powering repository analysis.

---

## ⚙️ Key Design Choices

- **Targeted Retrieval:** Category-scoped semantic lookups to isolate context.
- **Code Grounding:** Multi-file evidence matching to eliminate model fabrications.
- **Data Integrity:** Strict JSON-only schema outputs parsed programmatically by the backend.
- **Persistence:** Local per-repository vector storage for fast repeat indexing.

---

## 🧩 Core Components

| Layer | Responsibility |
|--------|----------------|
| 🗂 Repository Extractor | Clones and filters repository files by supported extension |
| ✂️ Chunking Service | Splits file content into overlapping, indexable chunks |
| 🧬 Embedding Service | Converts chunks and queries into vector representations |
| 🗄 pgvector Store | Persists chunks and embeddings scoped to each repository |
| 🔍 Retrieval Engine | Fetches top-k relevant chunks per analysis category via cosine distance |
| 🤖 Groq Llama 3.3 70B | Synthesizes each report section from retrieved context |
| 🛡 Auth Layer | Secures repository analysis behind JWT-authenticated users |

---

## 🔄 Repository Analysis Pipeline

RepoInsight processes every repository through a retrieval pipeline that continuously narrows raw source code down to only the context relevant to each report section, minimizing noise and keeping LLM reasoning grounded.

```text
Repository Chunks (pgvector)
    │
    ├── Summary + Tech Stack Query ──► Retrieved Chunks ──► LLM ──► Section
    ├── Architecture + Database Flow Query ──► Retrieved Chunks ──► LLM ──► Section
    ├── Architecture + Code Quality Query ──► Retrieved Chunks ──► LLM ──► Section
    ├── Production + Security Query ──► Retrieved Chunks ──► LLM ──► Section
    ├── Database Review Query ──► Retrieved Chunks ──► LLM ──► Section
    ├── Documentation Review Query ──► Retrieved Chunks ──► LLM ──► Section
    └── Contribution Opportunities Query ──► Retrieved Chunks ──► LLM ──► Section
```

**Figure 2.** Category-scoped retrieval and generation across all report sections.

---

## 🚀 Pipeline Characteristics

- ⚡ Semantic chunk retrieval per report category
- 🧠 Context-grounded LLM reasoning
- 🎯 Strict JSON-only output enforcement
- ⏱ Deduplicated chunk merging across related sections
- 🔄 Independent, parallel-friendly section generation
- 📄 Evidence-first summarization (no fabricated claims)

---

## Report Generation Flow

RepoInsight follows a deterministic multi-stage generation flow that guarantees every report section is produced from retrieved evidence rather than model assumption. This architecture prevents hallucinated technologies, invented architecture claims, and inconsistent reporting across sections.

```text
Retrieved Chunks + Section Prompt
        │
        ▼
Prompt Preprocessor (wraps context + task + JSON schema rules)
        │
        ▼
Groq LLM Completion
        │
        ▼
Response Cleanup (strip markdown / code fences)
        │
        ▼
JSON Parsing
        │
        ▼
Final Report Section
```

**Figure 3.** Internal flow governing how retrieved context becomes a validated report section.

---

## 🧠 Core Engineering Decisions

The RepoInsight platform is designed around a set of architectural decisions that prioritize **retrieval accuracy**, **evidence-grounded generation**, and **scalable multi-repository analysis**.

> ### ⚡ Retrieval-Augmented Generation
>
> RepoInsight follows a RAG architecture where every report section is generated only from repository chunks retrieved via semantic similarity. This design minimizes hallucination and ensures every claim in the report can be traced back to actual repository content.

---

> ### 🔄 Category-Scoped Query Design
>
> Instead of a single generic retrieval query, RepoInsight defines a dedicated retrieval query per analysis category — summary, tech stack, architecture, database, security, production, documentation, and contributions — so each section pulls the most relevant evidence for its specific purpose.

---

> ### 📈 Chunked, Overlapping Indexing
>
> Repository files are split into fixed-size, overlapping chunks before embedding. The overlap preserves context across chunk boundaries, preventing meaning from being lost mid-function or mid-explanation during retrieval.

---

> ### 🧬 Cosine-Similarity Retrieval
>
> Chunk retrieval is performed using cosine distance over pgvector-stored embeddings, scoped per repository, ensuring that only the most semantically relevant code and documentation is surfaced for each report section.

---

> ### 🔊 Prompt-Enforced JSON Contracts
>
> Every LLM call is wrapped in a strict prompt template requiring valid JSON output matching an exact schema, with no markdown, code fences, or explanatory text — enabling reliable downstream parsing without brittle post-processing.

---

> ### 🛡 Strict Context Grounding
>
> The LLM is explicitly instructed to answer only from retrieved repository context and to state when information is unavailable rather than inferring or inventing it, keeping generated reports honest about the limits of what was retrieved.

---

> ### ⚡ Concurrent Retrieval & Generation with `asyncio.gather()`
>
> Chunk retrieval and LLM report generation across all report sections are independent of one another, so RepoInsight runs them concurrently using `asyncio.gather()` instead of awaiting each section sequentially. This significantly reduces total report generation time compared to a sequential pipeline, since retrieval and Groq API calls for unrelated sections overlap rather than queue behind one another.

---

## 📂 Repository Architecture

RepoInsight adopts a modular architecture that separates authentication, repository ingestion, chunking, embedding, retrieval, and report generation into independent service layers.

```text
RepoInsight
│
├── app
│   ├── core          # Configuration & security (JWT, password hashing)
│   ├── db            # Database & ORM models (Repository, Chunk, User)
│   ├── routers        # REST API endpoints (auth, repository analysis)
│   ├── schemas        # Data validation models
│   └── service        # Ingestion, chunking, embedding, retrieval & LLM logic
│       ├── extract_repo_files.py
│       ├── create_repo_chunks.py
│       ├── generate_chunk_embeddings.py
│       ├── pgvector_queries.py
│       ├── build_report_query.py
│       ├── combine_chunks_prompts.py
│       ├── report_generation_prompts.py
│       ├── prompt_preprocessor.py
│       └── llm_service.py
│
├── README.md
└── requirements.txt
```

---

## ⚙️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | FastAPI | High-performance asynchronous API |
| **Repository Ingestion** | Git (subprocess) | Clones target repositories for analysis |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | Converts chunks and queries into vectors |
| **Vector Search** | pgvector | Stores and retrieves chunks by semantic similarity |
| **Large Language Model** | Groq API (Llama 3.3 70B Versatile) | Generates evidence-grounded report sections |
| **Authentication** | JWT | Secure user sessions |
| **Database** | PostgreSQL | Repository, chunk, and user persistence |
| **Version Control** | Git & GitHub | Collaborative software development |

---

## 📈 Retrieval & Report Category Design

RepoInsight generates each report section from a dedicated retrieval query rather than a single generic pass over the repository. This keeps context tightly scoped to what each section actually needs to evaluate.

### Category → Retrieval Priority

| Report Section | Retrieval Priority |
| -------------------------- | ------------------- |
| Repository Summary | README, docs, high-level source code |
| Technology Stack | Dependency files, config files, imports |
| Architecture Flow | Entry points, routers, services, middleware |
| Database Flow | ORM models, repositories, CRUD operations |
| Security Review | Auth logic, JWT handling, secrets, validation |
| Production Readiness | Deployment config, logging, error handling |
| Contribution Opportunities | TODOs, incomplete implementations, gaps |

---

## ⚙️ Engineering Challenges

Building a repository-wide RAG analysis system required solving multiple retrieval, grounding, and consistency challenges beyond typical CRUD applications.

| Challenge                    | Solution                                  |
| ---------------------------- | ----------------------------------------- |
| Irrelevant chunk retrieval | Category-specific retrieval queries per section |
| Duplicate context across related sections | Deduplicated chunk merging before prompting |
| LLM hallucination | Strict context-grounding instructions in every prompt |
| Inconsistent LLM output format | Enforced JSON-only schema with cleanup post-processing |
| Large repository scalability | Fixed-size overlapping chunking with vector indexing |
| Malformed or binary files | Extension filtering and safe error handling during extraction |
| Sequential LLM calls causing slow report generation | Parallelized retrieval & generation using `asyncio.gather()` |

---

## ⚡ Performance Considerations

RepoInsight is designed around targeted retrieval rather than exhaustive repository scanning. The architecture prioritizes scoped context windows, efficient vector search, and independent section generation to keep analysis accurate and reasonably fast even on larger codebases.

### Optimization Goals

| Objective                  | Approach                         |
| -------------------------- | -------------------------------- |
| Relevant context per section | Category-scoped semantic retrieval |
| Reduced token usage | Deduplicated, capped top-k chunk retrieval |
| Reliable structured output | Enforced JSON schema prompting |
| Consistent report quality | Evidence-only generation constraints |
| Scalable ingestion | Asynchronous FastAPI services with async DB sessions |
| Reduced total report latency | Concurrent chunk retrieval & LLM generation via `asyncio.gather()` |

---

## 📦 Installation & Local Deployment

### Prerequisites

- Python **3.11+**
- PostgreSQL with the **pgvector** extension enabled
- Git
- A Groq API key

---

### Clone Repository

```bash
git clone https://github.com/<your-username>/RepoInsight.git
cd RepoInsight
```

---

### Backend Setup

```bash
python -m venv venv

## Windows
venv\Scripts\activate

## Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

### Configure Environment

Create a `.env` file in the project root.

```env
API_KEY=your_groq_api_key
DATABASE_URL=your_database_url
SECRET_KEY=your_jwt_secret_key
```

---

### Run Application

```bash
uvicorn app.main:app --reload
```

| Component | URL |
|------------|------------------------|
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🔌 API Reference

RepoInsight exposes a lightweight REST API for authentication and repository analysis.

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/user` | Register user |
| POST | `/login` | User authentication |
| POST | `/repository_analysis` | Clone and analyze a GitHub repository, returning the full report |

---

### Authentication

```http
Authorization: Bearer <JWT_TOKEN>
```

---

### Sample Request

```json
{
  "url": "https://github.com/<owner>/<repo>"
}
```

### Sample Response (excerpt)

```json
{
  "repository_summary": {
    "overall_summary": "..."
  },
  "technology_stack": {
    "programming_language": "...",
    "backend_framework": "...",
    "database": "..."
  }
}
```

All endpoints communicate using **JSON** and are secured using **JWT-based authentication**.

---

## 💻 Local Setup & Execution

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd RepoInsight
   ```
2. Install the backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

Once running, open `http://127.0.0.1:8000/docs` to interact with the system via the native Swagger UI routes!

---

## Conclusion

RepoInsight demonstrates how retrieval-augmented generation can be engineered to turn an entire codebase into a structured, evidence-grounded intelligence report without requiring a developer to manually read through every file.

By integrating repository ingestion, semantic chunking, vector retrieval, and LLM-based synthesis into a unified pipeline, the project explores practical approaches for building scalable, trustworthy AI tooling for software understanding.

This repository reflects an end-to-end implementation of modern RAG system engineering — from repository ingestion and vector indexing to category-scoped retrieval and structured report generation.

---

**Developed by Geethika Tammineni**

Aspiring Software Engineer | Backend Development | AI Systems

If you found this project interesting, feel free to connect, contribute, or share feedback.
