# Retriever API

FastAPI backend for the **Retriever** study assistant, implementing Agentic RAG with LangChain/LangGraph, ChromaDB vector database, and flexible LLM provider support.

## Overview

This is the core of the Retriever system. It provides:

- **Agentic RAG pipeline** with planner, evaluator, and re-retrieval loop
- **Document ingestion** (PDF and text) with automatic chunking and embedding
- **Conversational AI** with context-aware responses and source citations
- **Local-first architecture** with optional remote LLM support
- **SQLite persistence** for conversations, materials catalog, and user profile

## Architecture

### Core Components

- **FastAPI** — REST API framework
- **LangChain/LangGraph** — Agentic RAG orchestration
- **ChromaDB** — Local vector database for document embeddings
- **Ollama** — Local embeddings (always) and LLM (optional)
- **OpenRouter** — Remote LLM provider (optional)

### Agentic RAG Pipeline

The `/ask` endpoint uses a LangGraph-based agent with these nodes:

1. **Planner** — Decides if retrieval is needed, rewrites the question using conversation history
2. **Retrieve** — Calls `vector_search` tool to fetch relevant chunks from ChromaDB
3. **Evaluator** — Scores the retrieved context (0-1 scale)
4. **Re-retrieval loop** — If score < threshold, retrieves again (up to `MAX_RETRIEVAL_LOOPS`)
5. **Augment** — Builds final prompt with context
6. **Generate** — Calls LLM to produce the answer

The pipeline always terminates (fallback after max loops) and returns `agent_steps[]` showing which nodes executed.

### Module Structure

```
retriever-api/
├── main.py                    # Bootstrap: create_app()
├── desktop_entry.py           # Entry point for packaged executable
├── app/
│   ├── factory.py             # FastAPI app, CORS, routers
│   ├── config.py              # Environment variables and constants
│   ├── dependencies.py        # Single wiring point for LangChain/Ollama/Chroma
│   ├── db.py                  # SQLite connection and schema
│   ├── settings_store.py      # LLM provider settings persistence
│   ├── routers/               # HTTP endpoints
│   │   ├── health.py          # GET /health
│   │   ├── upload.py          # POST /upload (PDF)
│   │   ├── ask.py             # POST /ask (chat with RAG)
│   │   ├── ingest.py          # POST /ingest/text, GET /documents
│   │   ├── settings.py        # GET/PUT /settings/llm
│   │   ├── conversations.py   # CRUD /conversations
│   │   ├── materials.py       # GET/DELETE /materials
│   │   └── profile.py         # GET/PUT /profile
│   ├── services/              # Business logic
│   │   ├── rag.py             # Agentic RAG orchestration
│   │   ├── ingest.py          # Document ingestion (PDF + text)
│   │   ├── pdf.py             # PDF processing
│   │   ├── memory.py          # History normalization and truncation
│   │   ├── settings.py        # LLM settings management
│   │   ├── conversations.py   # Conversation persistence
│   │   ├── materials.py       # Materials catalog
│   │   └── profile.py         # User profile
│   ├── agents/                # LangGraph agents
│   │   ├── planner.py         # Question analysis and rewriting
│   │   └── evaluator.py       # Context scoring
│   ├── graph/                 # LangGraph workflow
│   │   └── rag_agent.py       # Full RAG agent graph
│   ├── prompts/               # System prompts
│   │   ├── tutor.py           # Main tutor prompt
│   │   ├── planner.py         # Planner prompt
│   │   └── evaluator.py       # Evaluator prompt
│   ├── providers/             # LLM provider abstraction
│   │   ├── base.py            # Provider protocol
│   │   ├── registry.py        # Provider resolution
│   │   ├── ollama.py          # Ollama implementation
│   │   └── openrouter.py      # OpenRouter implementation
│   └── tools/                 # LangChain tools
│       ├── vector_search.py   # Search ChromaDB
│       ├── list_documents.py  # List indexed documents
│       └── summarize_chunks.py# Summarize chunks
├── chroma_data/               # ChromaDB persistence (gitignored)
├── tmp_uploads/               # Temporary PDF uploads (gitignored)
└── user_data/                 # SQLite database (gitignored)
```

## Prerequisites

- **Python 3.11+**
- **Ollama** running with embedding model:
  ```bash
  ollama pull nomic-embed-text
  ```

For local LLM (optional):
```bash
ollama pull llama3.1
```

**Important:** Use `llama3.1` (with `.1`), not `llama3`. The base model doesn't support tool calling.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
```

## Configuration

Edit `.env` to configure the LLM provider:

### Option 1: 100% Local (Ollama)

```bash
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
```

No API key needed. Embeddings and LLM both run locally.

### Option 2: Remote LLM (OpenRouter)

```bash
LLM_PROVIDER=openrouter
LLM_MODEL=deepseek/deepseek-v4-flash-0731
LLM_API_KEY=your-api-key-here
LLM_API_BASE_URL=https://openrouter.ai/api/v1
```

Embeddings still run locally via Ollama. Only the LLM is remote.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | `ollama` or `openrouter` | `openrouter` |
| `LLM_MODEL` | Model identifier | Provider-specific |
| `LLM_API_KEY` | API key (for OpenRouter) | — |
| `LLM_API_BASE_URL` | API base URL | Provider-specific |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `EMBED_MODEL` | Embedding model | `nomic-embed-text` |
| `CHUNK_SIZE` | Text chunk size | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap | `200` |
| `RETRIEVER_K` | Number of chunks to retrieve | `4` |
| `MAX_RETRIEVAL_LOOPS` | Max re-retrieval attempts | `2` |
| `EVALUATOR_MIN_SCORE` | Minimum context score (0-1) | `0.6` |
| `MAX_HISTORY_MESSAGES` | Max messages in conversation history | `10` |
| `API_PORT` | API server port | `8000` |
| `DESKTOP_MODE` | Enable desktop CORS (`1` = enabled) | `0` |

## Running the API

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Interactive API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload and index PDF |
| `POST` | `/ingest/text` | Index text content |
| `POST` | `/ask` | Ask a question (Agentic RAG) |
| `GET` | `/documents` | List indexed documents (from ChromaDB) |

### Persistence Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/conversations` | List all conversations |
| `POST` | `/conversations` | Create new conversation |
| `GET` | `/conversations/{id}` | Get conversation with messages |
| `PUT` | `/conversations/{id}` | Update conversation title |
| `DELETE` | `/conversations/{id}` | Delete conversation |
| `POST` | `/conversations/{id}/messages` | Add message to conversation |
| `GET` | `/materials` | List materials catalog (SQLite) |
| `DELETE` | `/materials/{id}` | Delete material from catalog |
| `GET` | `/profile` | Get user profile |
| `PUT` | `/profile` | Update user profile |

### Settings Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/settings/llm` | Get LLM settings (key masked) |
| `PUT` | `/settings/llm` | Update LLM settings |
| `GET` | `/settings/llm/models` | List available models |
| `POST` | `/settings/llm/test` | Test LLM connection |

## Example Usage

### Upload a PDF

```bash
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@document.pdf"
```

Response:
```json
{
  "message": "PDF indexed successfully",
  "filename": "document.pdf",
  "chunks_indexed": 42
}
```

### Index text

```bash
curl -X POST http://127.0.0.1:8000/ingest/text \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Notes",
    "text": "Content to index..."
  }'
```

### Ask a question

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "history": [],
    "conversation_id": "optional-conversation-id"
  }'
```

Response:
```json
{
  "answer": "The main topic is...",
  "sources": [
    {
      "source": "document.pdf",
      "type": "pdf",
      "page": 3,
      "snippet": "Relevant excerpt..."
    }
  ],
  "agent_steps": [
    {"step": "plan", "loop": 0, "detail": "Requires retrieval"},
    {"step": "retrieve", "loop": 0, "detail": "Found 4 chunks"},
    {"step": "evaluate", "loop": 0, "detail": "Score 0.85"},
    {"step": "generate", "loop": 0, "detail": "Answer generated"}
  ]
}
```

### Create a conversation

```bash
curl -X POST http://127.0.0.1:8000/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "Study Session 1"}'
```

## Key Features

### Agentic RAG

Unlike simple RAG (retrieve → augment → generate), the Agentic RAG pipeline:

- **Plans** whether retrieval is needed (some questions don't need documents)
- **Evaluates** retrieved context quality
- **Re-retrieves** if context is insufficient (up to `MAX_RETRIEVAL_LOOPS`)
- **Falls back** gracefully if max loops reached
- **Exposes** all steps in `agent_steps[]` for transparency

### Tool Calling

The LLM has access to tools:

- `vector_search(query, k)` — Search ChromaDB for relevant chunks
- `list_documents()` — List all indexed documents
- `summarize_chunks(chunks)` — Summarize a list of chunks

Tools are defined in `app/tools/` and registered in `app/dependencies.py`.

### Conversation Persistence

Conversations are stored in SQLite (`user_data/retriever.db`):

- Multiple conversations supported
- Messages include sources and agent steps
- Conversation history sent to planner for context-aware follow-ups

### Materials Catalog

Indexed documents are tracked in SQLite with metadata:

- Source filename/title
- Type (pdf/text)
- Chunk count
- Ingestion timestamp

### Provider Abstraction

The provider system (`app/providers/`) abstracts LLM differences:

- `OllamaProvider` — Local Ollama
- `OpenRouterProvider` — Remote OpenRouter API
- Easy to add new providers

## Error Handling

| Status | Meaning |
|--------|---------|
| `400` | Validation error (invalid input) |
| `409` | Provider selected without API key |
| `502` | Remote provider failed (auth, quota, timeout) |
| `503` | Ollama unreachable (embeddings require local Ollama) |

API keys are **never** logged or returned in error messages.

## Desktop Mode

Set `DESKTOP_MODE=1` to enable desktop CORS (allows all origins). Used by the Electron wrapper.

## Development

### Adding a new tool

1. Create tool in `app/tools/` using `@tool` decorator
2. Register in `app/tools/__init__.py`
3. Tool will be available to the LLM automatically

### Adding a new provider

1. Implement `LlmProvider` protocol in `app/providers/`
2. Register in `app/providers/registry.py`
3. Add to `KNOWN_PROVIDERS` in `app/services/settings.py`

### Testing

No test suite configured. Manual testing:

```bash
# Start the API
uvicorn main:app --reload

# Test health
curl http://127.0.0.1:8000/health

# Test with a question
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

## License

To be defined.
