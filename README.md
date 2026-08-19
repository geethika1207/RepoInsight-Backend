# RepoInsight

## An AI Repository Intelligence System for Automated Codebase Analysis

> **Why I'm building this:** Onboarding onto an unfamiliar codebase takes hours of manual tracing, and standard AI assistants often just summarize basic architecture flows. I built RepoInsight to go beyond simple summaries by delivering deep, actionable engineering reviews. It takes any public GitHub repository and conducts comprehensive Security, Architecture, Production, and Database reviews directly from the source code. Instead of just telling you what the code is, it critically evaluates how it is built and actively identifies where new contributions and improvements can be made. This provides senior-level codebase intelligence instantly, without a developer having to read every file from scratch.

**RepoInsight** is an AI-driven codebase intelligence platform engineered to bridge the gap between raw source code and deep architectural understanding. Instead of spending hours manually tracing unfamiliar files, the system clones a repository, semantically indexes its structure, and generates comprehensive, evidence-grounded engineering reviews—critically evaluating system design, security posture, database flows, and high-impact contribution zones.

To achieve this, I engineered a production-grade **Retrieval-Augmented Generation (RAG)** pipeline featuring **Parent-Child Chunking**, asynchronous vector indexing with pgvector, and category-scoped semantic retrieval. Paired with **O(1) Context Deduplication** and **strict Anti-Meta Guardrails**, this architecture guarantees that the LLM evaluates real source-code evidence with full structural context—delivering deterministic, hallucination-free engineering reviews.


---


## 🌍 Live Deployments

Test the active platform live:

* **Frontend UI (Streamlit):** [https://repoinsight.streamlit.app](https://repoinsight.streamlit.app)
* **Backend API (FastAPI Docs):** [https://repoinsight-backend-1.onrender.com/docs](https://repoinsight-backend-1.onrender.com/docs)


---


## 🛠️ Built With

![Python](https://img.shields.io/badge/Python-3.11+-blue)

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)

![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)

![pgvector](https://img.shields.io/badge/pgvector-Vector%20Search-6E56CF)

![Cohere](https://img.shields.io/badge/Cohere-Command--R-orange)

![Cohere Embed](https://img.shields.io/badge/Cohere-Embed--V3-yellow)

![Architecture](https://img.shields.io/badge/Architecture-RAG--Pipeline-ff6b35)

![License](https://img.shields.io/badge/License-MIT-yellow)

![Status](https://img.shields.io/badge/Status-Active-success)

![Analysis](https://img.shields.io/badge/Analysis-Repository--Wide-blueviolet)


---


## 🛠️ Technical Overview

| Category | Specification |
|-----------|---------------|
| Project Type | AI Repository Intelligence System |
| Primary Language | Python 3.11 |
| Backend Framework | FastAPI |
| Frontend Framework | Streamlit |
| Communication Protocol | REST API |
| Repository Ingestion | Git (subprocess-based cloning) |
| Embedding Model | Cohere Embed V3 |
| Vector Storage | PostgreSQL + `pgvector` |
| Large Language Model | Cohere API (`command-r`) |
| Retrieval Strategy | Cosine-Similarity with Parent-Child Context Preservation |
| Concurrency Model | `asyncio.gather()` for parallel retrieval & LLM generation |
| Optimization | O(1) Hash-map Deduplication |
| Data Storage | PostgreSQL |
| Authentication | JWT Authentication |


---


## 🏗 System Architecture

RepoInsight is built on a retrieval-augmented pipeline architecture that separates repository ingestion, hierarchical indexing, and context retrieval into highly optimized, independent stages. By transforming raw source code through Parent-Child chunking and concurrent asynchronous generation, the pipeline seamlessly converts complex repositories into structured, evidence-grounded engineering reviews—resulting in a system that is both deeply accurate and highly extensible.

```text
GitHub URL
    │
    ▼
Clone Repository (subprocess)
    │
    ▼
Extract Supported Files & Apply Parent-Child Chunking
    │
    ▼
Generate Embeddings (Cohere Embed V3)
    │
    ▼
Store Chunks + Embeddings (PostgreSQL / pgvector)
    │
    ▼
Retrieve Relevant Chunks (Cosine Similarity, per category)
    │
    ▼
O(1) Hash-map Deduplication & Context Merging
    │
    ▼
Prompt Preprocessing (Enforcing Anti-Meta Guardrails)
    │
    ▼
LLM Review Generation (Cohere Command-R via asyncio.gather)
    │
    ▼
Structured JSON Output & Streamlit UI Render
```


---


## ⚙️ Key Design Choices

- **Hierarchical Context Preservation:** Implemented **Parent-Child Chunking** to map granular semantic searches directly back to their full file structures, ensuring the LLM never loses architectural scope during retrieval.
- **Asynchronous Orchestration:** Refactored the core execution pipeline from sequential blocking calls to concurrent execution using **asyncio.gather()**, slashing end-to-end report generation latency.
- **O(1) Context Deduplication:** Engineered a hash-map pipeline (`dict.fromkeys()`) to instantly strip overlapping chunks retrieved across related categories, preventing context-window bloat and saving precious tokens.
- **Deterministic Grounding:** Enforced strict framework-specific syntax queries and explicit **Anti-Meta Guardrails**. If architectural evidence is missing, the LLM is forced to explicitly state so rather than hallucinating filler content.
- **Strict Data Integrity:** Bound the LLM to rigid JSON-only schemas that are programmatically validated by the **FastAPI** backend before being safely rendered on the decoupled **Streamlit** client.
- **Stateful Persistence:** Utilized local, per-repository vector storage via PostgreSQL and **pgvector** for rapid re-indexing and isolated semantic lookups.


---


## 🧩 Core Components

| Layer | Responsibility |
|--------|----------------|
| 🗂 **Repository Extractor** | Clones and filters repository files by supported extensions before processing. |
| ✂️ **Chunking Service** | Implements **Parent-Child Chunking** to map granular semantic snippets back to their full file structures. |
| 🧬 **Embedding Service** | Generates high-accuracy vector representations using **Cohere Embed V3**. |
| 🗄 **pgvector Store** | Persists chunks and embeddings scoped to each repository using asynchronous **`SQLAlchemy**. |
| 🔍 **Retrieval Engine** | Fetches top-k chunks via cosine distance and applies **O(1) Deduplication** to prevent context bloat. |
| 🤖 **Cohere Command-R** | Synthesizes engineering reviews concurrently via **asyncio.gather()** while enforcing strict **Anti-Meta Guardrails**. |
| 🛡 **Auth Layer** | Secures **FastAPI** endpoints and manages user sessions via native **JWT Authentication**. |
| 🎨 **Streamlit Client** | Provides a decoupled, state-managed frontend for repository submission and structured review rendering. |


---


## 🔄 Repository Analysis Pipeline

**RepoInsight** processes every repository through a highly optimized retrieval pipeline that continuously narrows raw source code down to precise, section-specific context. By integrating **Parent-Child Chunking** and concurrent execution via **asyncio.gather()**, the system minimizes noise and latency while keeping the LLM reasoning strictly grounded in verified evidence.

```text
Parent-Child Context Index (pgvector)
    │
    ├── [Concurrent Execution via asyncio.gather()]
    │
    ├── Summary & Tech Stack ────► Cosine Search ──► O(1) Dedup ──► Cohere LLM ──► Section
    ├── Architecture Flow ───────► Cosine Search ──► O(1) Dedup ──► Cohere LLM ──► Section
    ├── Code Quality & Design ───► Cosine Search ──► O(1) Dedup ──► Cohere LLM ──► Section
    ├── Security & Auth ─────────► Cosine Search ──► O(1) Dedup ──► Cohere LLM ──► Section
    ├── Database Operations ─────► Cosine Search ──► O(1) Dedup ──► Cohere LLM ──► Section
    ├── Production Readiness ────► Cosine Search ──► O(1) Dedup ──► Cohere LLM ──► Section
    └── Contribution Zones ──────► Cosine Search ──► O(1) Dedup ──► Cohere LLM ──► Section
    │
    ▼
Structured JSON Assembly & Streamlit UI Render
```


---


## 🚀 Pipeline Characteristics

- ⚡ **Parent-Child Context:** Granular semantic chunk retrieval powered by **`Cohere Embed V3`** that preserves the broader architectural scope of the original file.
- 🧠 **Zero-Hallucination Reasoning:** Enforced **Anti-Meta Guardrails** that strictly bound the LLM to verified codebase evidence rather than system prompt assumptions.
- 🎯 **Strict Data Contracts :** Rigid JSON-only output schemas programmatically validated by the **FastAPI** backend.
- ⏱ **O(1) Deduplication:** Hash-map based chunk merging across related query categories prevents token bloat and optimizes LLM context injection.
- 🔄 **Ultra-Low Latency:** Independent, concurrent engineering review generation orchestrated asynchronously via **asyncio.gather()**.
- 📄 **Evidence-First Reviews:** Powered by **Cohere Command-R**, ensuring absolute transparency—if architectural data is missing, the system explicitly reports it via strict "Escape Hatches" rather than fabricating claims.


---


## ⚙️ Review Generation Flow

**RepoInsight** follows a deterministic, multi-stage generation flow that guarantees every review section is produced exclusively from retrieved evidence rather than model assumption. By enforcing strict **Anti-Meta Guardrails** and utilizing **Cohere Command-R**, this architecture prevents hallucinated technologies, invented architecture claims, and inconsistent reporting across concurrent sections.

```text
O(1) Deduplicated Context + Syntax-Targeted Prompt
        │
        ▼
Prompt Preprocessor (Enforces Anti-Meta Rules & Escape Hatches)
        │
        ▼
Cohere Command-R Completion (RAG-Optimized Generation)
        │
        ▼
Response Sanitization (Strips Formatting & Code Fences)
        │
        ▼
Strict JSON Parsing & Validation
        │
        ▼
Final Engineering Review Section
```


---


## 🧠 Core Engineering Decisions

The **RepoInsight** platform is designed around a set of architectural decisions that prioritize **retrieval accuracy**, **evidence-grounded generation**, and solving severe production bottlenecks—specifically tackling context loss, latency timeouts, and LLM hallucinations.

> ### ⚡ Production-Grade RAG & Actionable Reviews
>
> **RepoInsight** abandons generic summarization for a custom RAG architecture powered by **Cohere Command-R**. Every engineering review section is synthesized exclusively from retrieved codebase evidence, ensuring claims are strictly rooted in veritas rather than model assumption.

---

> ### 📈 Hierarchical Context via `Parent-Child Chunking`
>
> Standard sliding-window chunking destroys complex codebase logic. To solve this, repository files are mapped using **Parent-Child Chunking**. Granular semantic snippets (children) are embedded for precise retrieval, but are linked directly back to their full file structures (parents), ensuring the LLM never loses the broader architectural scope.

---

> ### 🧮 O(1) Context Deduplication & Vector Search
>
> Vector search is executed using cosine distance over **pgvector** and **Cohere Embed V3**. To combat context-window bloat and token waste from overlapping category queries, an **O(1) Deduplication** hash-map pipeline (dict.fromkeys()) instantly strips duplicate codebase evidence before LLM injection.

---

> ### 🛡️ Anti-Meta Guardrails & Zero Hallucinations
>
> To prevent the LLM from entering recursive prompt loops or hallucinating architectural claims, the system employs strict **Anti-Meta Guardrails**. Retrieval shifts to framework-specific syntax (e.g., @router.post), and explicit "Escape Hatches" force the model to explicitly state when evidence is missing rather than inventing filler content.

---

> ### ⚡ Slashing Latency with `asyncio.gather()`
>
> Cloud server timeouts originally bottlenecked report generation. To solve this, the entire backend execution pipeline was refactored from blocking sequential calls to asynchronous orchestration via **asyncio.gather()**. Independent review sections run completely in parallel, reducing end-to-end latency to under 45 seconds.

---

> ### 🔊 Prompt-Enforced JSON Data Contracts
>
> Every LLM call is bound to a strict prompt template requiring valid JSON output matching an exact programmatic schema. This guarantees reliable downstream validation by the **FastAPI** backend before seamless rendering on the decoupled **Streamlit** client.


---


## 📂 Repository Architecture

RepoInsight adopts a modular architecture that separates authentication, repository ingestion, chunking, embedding, retrieval, and report generation into independent service layers.

```text

**RepoInsight** adopts a modular, monorepo architecture that cleanly separates the heavy **FastAPI** backend AI pipeline from the lightweight **Streamlit** client.

```text
RepoInsight/
├── app/                   # FastAPI backend application
│   ├── core/              # Configuration & security (JWT, password hashing)
│   ├── db/                # PostgreSQL & SQLAlchemy async models (Repository, Chunk, User)
│   ├── routers/           # REST API endpoints (Auth, Repo Analysis)
│   ├── schemas/           # Pydantic strict data validation contracts
│   └── service/           # RAG pipeline, Cohere integration, async logic
│       ├── extract_repo_files.py        # Subprocess cloning & file filtering
│       ├── create_repo_chunks.py        # Parent-Child Chunking implementation
│       ├── generate_chunk_embeddings.py # Cohere Embed V3 integration
│       ├── pgvector_queries.py          # Cosine similarity search & O(1) deduplication
│       ├── build_report_query.py        # Category-scoped query mapping
│       ├── combine_chunks_prompts.py    # Context merging logic
│       ├── report_generation_prompts.py # System prompts & JSON schemas
│       ├── prompt_preprocessor.py       # Enforces Anti-Meta rules and Escape Hatches
│       └── llm_service.py               # Cohere Command-R asyncio.gather execution
│
├── frontend/              # Streamlit user interface
│   ├── streamlit_app.py   # Native UI, JWT state management, and report rendering
│   └── requirements.txt   # Lightweight UI dependencies
│
├── requirements.txt       # Heavy backend dependencies (FastAPI, pgvector, cohere, etc.)
├── .env                   # Environment configuration
└── README.md
```


---


## ⚙️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | **FastAPI** | High-performance asynchronous API orchestration. |
| **Frontend** | **Streamlit** | Decoupled, state-managed UI and engineering review rendering. |
| **Repository Ingestion** | **Git (subprocess)** | Clones and processes target repositories for analysis. |
| **Embeddings** | **Cohere Embed V3** | High-accuracy vector representation of hierarchical code chunks. |
| **Vector Search** | **pgvector** | Stores and retrieves chunks via cosine semantic similarity. |
| **Large Language Model** | **Cohere Command-R** | Generates RAG-optimized, evidence-grounded engineering reviews. |
| **Authentication** | **JWT** | Secure native user sessions and API endpoint protection. |
| **Database** | **PostgreSQL** | Asynchronous ORM persistence for users, repositories, and vectors. |


---


## 📈 Retrieval & Review Category Design

**RepoInsight** generates each engineering review section from a dedicated, syntax-targeted retrieval query rather than a single generic pass over the repository. This keeps the vector search tightly scoped to what each section actually needs to evaluate, preventing context dilution.

### Category → Retrieval Priority

| Review Section | Retrieval Priority & Targeting |
| -------------------------- | ------------------- |
| **Repository Summary** | High-level source code, READMEs, and core documentation |
| **Technology Stack** | Dependency files, `requirements.txt`, `package.json`, global imports |
| **Architecture Flow** | Application entry points, API routers (`@router`), middleware, service layers |
| **Database Flow** | ORM models (`__tablename__`), repository patterns, CRUD implementations |
| **Security Review** | Authentication logic, JWT implementations, secret handling, input validation |
| **Production Readiness** | Dockerfiles, deployment configs, centralized logging, global exception handling |
| **Contribution Zones** | `TODO` comments, incomplete implementations, structural architecture gaps |


---


## ⚙️ Engineering Challenges

Building a production-grade repository analysis system required solving severe bottlenecks around context loss, cloud timeouts, and LLM hallucinations—moving far beyond standard CRUD operations.

> | **⚙️ Challenge** | **🚀 Engineering Solution** |
> | :--- | :--- |
> | **Context Loss via Standard Chunking** <br> *Sliding windows destroyed the broader architectural scope of the code.* | Engineered **Parent-Child Chunking** to map granular, searchable semantic snippets directly back to their full file structures. |
> | **Cloud Server Timeouts & Latency** <br> *Sequential processing caused 5+ minute wait times and deployment crashes.* | Refactored the core execution pipeline from blocking calls to fully concurrent asynchronous orchestration using **`asyncio.gather()`**, dropping latency to under 45 seconds. |
> | **Context Window Bloat** <br> *Related queries retrieved overlapping chunks, wasting tokens and confusing the LLM.* | Implemented an **O(1) Hash-map Deduplication** pipeline (`dict.fromkeys()`) to instantly merge and strip duplicate codebase evidence across categories. |
> | **LLM Hallucinations & Meta-Loops** <br> *The model invented filler content when files were missing or summarized its own prompt.* | Designed strict **Anti-Meta Guardrails**. Shifted retrieval to framework-specific syntax and forced explicit "Escape Hatches" (making the LLM state when data is missing). |
> | **Brittle Downstream UI Rendering** <br> *Inconsistent markdown or code fences from the LLM broke the frontend.* | Bound the **Cohere Command-R** model to rigid, prompt-enforced JSON data contracts, validated by the **FastAPI** backend before reaching **Streamlit**. |
> | **Malformed & Binary File Crashes** <br> *Ingesting raw repos caused encoding errors on non-text files.* | Built an extraction filtering layer with safe error handling to isolate and process only supported architectural extensions. |


---


## ⚡ Performance Considerations

**RepoInsight** is designed around targeted retrieval rather than exhaustive repository scanning. The architecture prioritizes **hierarchical context preservation**, **O(1) vector deduplication**, and **fully concurrent asynchronous execution** to keep codebase analysis deterministic and blazingly fast, even on enterprise-scale repositories.

### Optimization Goals

> | **🎯 Optimization Objective** | **🛠️ Engineering Approach** |
> | :--- | :--- |
> | **Deep Context per Section** | Category-scoped semantic retrieval mapped via **Parent-Child Chunking**. |
> | **Reduced Token Bloat** | **O(1) Hash-map Deduplication** bounding top-k chunk retrieval. |
> | **Reliable Structured Output** | Strict JSON schema prompting enforced by the **FastAPI** backend before rendering on **Streamlit**. |
> | **Zero-Hallucination Quality** | Evidence-only generation constrained by syntax-targeting and **Anti-Meta Guardrails**. |
> | **Scalable Ingestion** | Fully asynchronous **FastAPI** services integrated with async **SQLAlchemy** database sessions. |
> | **Sub-Minute Review Latency** | Concurrent codebase retrieval and **Cohere Command-R** LLM generation orchestrated via **asyncio.gather()**. |


---


## 🌍 Live Deployments

Skip the local setup and test the active platform live:

* **Frontend UI (Streamlit):** [https://repoinsight.streamlit.app](https://repoinsight.streamlit.app)
* **Backend API (FastAPI Docs):** [https://repoinsight-backend-1.onrender.com/docs](https://repoinsight-backend-1.onrender.com/docs)

---

## 📦 Installation & Local Deployment

### Prerequisites

* Python **3.11+**
* PostgreSQL with the **pgvector** extension enabled
* Git
* A **Cohere API Key**

---

### Clone Repository

```bash
git clone [https://github.com/](https://github.com/)<your-username>/RepoInsight.git
cd RepoInsight

```

---

### Backend Setup

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

---

### Configure Environment

Create a `.env` file in the project root.

```env
COHERE_API_KEY=your_cohere_api_key
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/repoinsight
SECRET_KEY=your_jwt_secret_key
```

---

### Run Backend Application

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

## 🎯 Conclusion

**RepoInsight** demonstrates how advanced retrieval-augmented generation can be engineered to transform an entire codebase into structured, evidence-grounded intelligence without requiring hours of manual code tracing.

By unifying **Parent-Child Chunking**, high-speed vector retrieval via **pgvector**, and concurrent LLM synthesis using **Cohere Command-R**, this platform moves beyond basic AI summarization to deliver highly actionable engineering reviews. 

From zero-hallucination guardrails to fully asynchronous pipeline orchestration, this repository serves as a complete, end-to-end blueprint for building scalable, trustworthy AI tooling for complex software environments.

---

**Developed by Geethika Tammineni**

Aspiring Software Engineer | Backend Development | AI Systems

If you found this project interesting, feel free to connect, contribute, or share feedback.
