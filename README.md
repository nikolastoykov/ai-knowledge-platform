# AI Knowledge Platform

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge)
![pgvector](https://img.shields.io/badge/pgvector-336791?style=for-the-badge)

An asynchronous FastAPI backend for document ingestion, hybrid search, retrieval-augmented generation (RAG), and agents that call tools. It combines PostgreSQL and pgvector with OpenAI embeddings and language models, with a separate managed RAG workflow using hosted vector stores.

## Features

- **Knowledge ingestion:** split documents into overlapping, sentence-aware chunks, generate embeddings, and replace documents and their chunks transactionally.
- **Hybrid retrieval:** combine vector similarity and PostgreSQL full-text search with reciprocal rank fusion.
- **Reranking:** score search candidates with a language model and filter them by relevance.
- **Grounded answers:** return answers alongside retrieved source chunks, with a fallback when no relevant sources remain.
- **Managed RAG:** upload files to hosted vector stores, search them, and answer questions with file search.
- **AI utilities:** summarize text, rewrite tone, classify support tickets, generate embeddings, and compare text similarity.
- **Tool-calling agents:** look up demo customers and orders through reusable tool definitions.
- **RAG evaluations:** measure retrieval accuracy and answer quality, including model-based correctness and grounding checks.

## Technology Stack

| Technology | Role |
| --- | --- |
| Python | Async application and service logic |
| FastAPI + Uvicorn | HTTP API and ASGI server |
| OpenAI Python SDK | Language models, embeddings, structured outputs, tool calling, and managed file search |
| PostgreSQL + pgvector | Document storage, vector search, HNSW indexes, and full-text search |
| SQLAlchemy + asyncpg | Async database access |
| Alembic | Database schema migrations |
| Pydantic + pydantic-settings | Request validation, structured model outputs, and environment configuration |

## Architecture

```mermaid
flowchart TD
    API[FastAPI routes] --> Services[Application services]
    Services --> Providers[AI provider interfaces]
    Providers --> OpenAI[OpenAI API]
    Services --> Retrieval[Semantic and keyword retrieval]
    Retrieval --> DB[(PostgreSQL + pgvector)]
    Retrieval --> Fusion[Reciprocal rank fusion]
    Fusion --> Reranker[LLM reranking]
    Reranker --> Answer[Answer with source chunks]
    Services --> Tools[Customer and order demo tools]
    Services --> Managed[Managed RAG service]
    Managed --> Hosted[Hosted vector stores and file search]
```

The API, service, provider, and repository layers keep HTTP handling separate from AI calls and persistence. Local retrieval uses cosine similarity and a GIN-indexed full-text search vector; the managed workflow delegates retrieval to hosted vector stores.

## Getting Started

Use Python 3.12 and a PostgreSQL database with the `vector` extension available. The existing migrations use **1,536-dimensional embeddings**, so keep `EMBEDDING_DIMENSIONS=1536` unless you also update the schema.

### 1. Clone and install

```bash
git clone https://github.com/nikolastoykov/ai-knowledge-platform.git
cd ai-knowledge-platform
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure the environment

```bash
cp .env.example .env
```

Edit `.env` with your API key, a text model available to your account, and your database connection string. The text model must support structured outputs and function calling; managed RAG also needs file search support. Use the `postgresql+asyncpg://` URL scheme for the async database driver.

| Variable | Purpose | Example / default |
| --- | --- | --- |
| `OPENAI_API_KEY` | API authentication | Your API key |
| `OPENAI_MODEL` | Text generation, reranking, and agents | Set a model available to your account |
| `OPENAI_EMBEDDING_MODEL` | Embedding generation | `text-embedding-3-small` |
| `EMBEDDING_DIMENSIONS` | Vector size matching the database schema | `1536` |
| `DATABASE_URL` | Async PostgreSQL connection | `postgresql+asyncpg://user:password@localhost:5432/ai_knowledge` |
| `RAG_MIN_SIMILARITY` | Minimum semantic similarity in the RAG pipeline | `0.3` |
| `RAG_MIN_RELEVANCE` | Minimum reranker relevance score | `0.5` |

### 3. Prepare the database

Create the database and enable pgvector before running migrations. For a local PostgreSQL installation:

```bash
createdb -U postgres ai_knowledge
psql -U postgres -d ai_knowledge -c 'CREATE EXTENSION IF NOT EXISTS vector;'
alembic upgrade head
```

Use connection arguments that match your PostgreSQL installation and `.env` configuration.

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation at [localhost:8000/docs](http://localhost:8000/docs) or ReDoc at [localhost:8000/redoc](http://localhost:8000/redoc).

## API Examples

### Ingest a document

```bash
curl -X POST http://localhost:8000/knowledge/documents \
  -H 'Content-Type: application/json' \
  -d '{"id":"shipping-policy","text":"Standard delivery usually takes five business days. During holidays or periods of high demand, delivery may be delayed. Check your tracking information for updates."}'
```

### Search the knowledge base

```bash
curl -X POST http://localhost:8000/knowledge/search/hybrid \
  -H 'Content-Type: application/json' \
  -d '{"query":"When will my package arrive?","limit":5}'
```

Use `/knowledge/search/reranked` with the same body to apply model-based relevance scoring.

### Ask a grounded question

```bash
curl -X POST http://localhost:8000/rag/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"When will my package arrive?","limit":5}'
```

The response contains an `answer` and `sources`, including each source document ID, chunk index, text, and relevance score.

### Run an agent

```bash
curl -X POST http://localhost:8000/agent/run \
  -H 'Content-Type: application/json' \
  -d '{"task":"Find order 123 and tell me its status and the customer name."}'
```

Customer and order tools use in-memory demo records in `app/tools/`.

## API Routes

All routes below use `POST`. Request schemas are available in the interactive API documentation.

| Area | Routes |
| --- | --- |
| Knowledge | `/knowledge/documents`, `/knowledge/search/hybrid`, `/knowledge/search/reranked` |
| RAG | `/rag/ask` |
| Managed RAG | `/managed-rag/ingest`, `/managed-rag/search`, `/managed-rag/answer` |
| Semantic search | `/search/documents`, `/search/documents/batch`, `/search/query` |
| Embeddings | `/ai/embed`, `/ai/similarity` |
| Text utilities | `/ai/summarize`, `/ai/rewrite`, `/ai/classify-ticket` |
| Assistants | `/ai/order-assistant`, `/agent/run` |
| Evaluations | `/evals/rag-retrieval`, `/evals/rag-answers` |

For managed ingestion, `file_path` refers to a file accessible to the API server. The sample file `app/managed_demo.txt` can be used with `/managed-rag/ingest`.

The prototype also includes `/ai/generate`; that route still uses an older provider call signature and needs updating before use.

## Evaluations

The evaluation endpoints call live AI services and use the current knowledge database. Before running them, ingest policy documents with the IDs `shipping-policy`, `refund-policy-long`, `account-security`, and `product-care`, with content matching the cases in `app/evals/`.

```bash
curl -X POST http://localhost:8000/evals/rag-retrieval
curl -X POST http://localhost:8000/evals/rag-answers
```

Retrieval evaluation reports top-result and exact-source-set accuracy. Answer evaluation reports phrase checks, correctness, grounding, and average judge score.

## Project Structure

```text
app/
├── ai/          # Provider interfaces, OpenAI integration, embeddings, tool-call models
├── api/         # FastAPI routes and request/response schemas
├── db/          # SQLAlchemy models and async database sessions
├── domain/      # Search, ticket, reranking, and evaluation types
├── evals/       # Retrieval and answer evaluation cases and runners
├── rag/         # Chunking, knowledge repository, and reciprocal rank fusion
├── search/      # Vector stores and similarity helpers
├── services/    # Ingestion, retrieval, RAG, agents, and AI utilities
├── tools/       # Demo customer and order tools
└── main.py      # Application entry point
migrations/     # Alembic schema migrations
alembic.ini     # Migration configuration
.env.example    # Environment configuration template
requirements.txt
```
