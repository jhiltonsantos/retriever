# SpeechCode API

Backend FastAPI do assistente de estudos **speech-code** — RAG local para Programação e Inglês.

## Pré-requisitos

- Python 3.10+ (3.11+ recomendado)
- [Ollama](https://ollama.com/download) rodando na bandeja do sistema
- Modelos baixados: `llama3` e `nomic-embed-text`
- Ambiente virtual em `.venv/` (já criado neste diretório)

```powershell
ollama pull llama3
ollama pull nomic-embed-text
```

## Como rodar

```shell
cd speech-code-api
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Estrutura (Fase 2)

```
speech-code-api/
├── main.py                 # Bootstrap: create_app()
├── app/
│   ├── factory.py          # FastAPI + CORS + routers
│   ├── config.py           # Ollama, ChromaDB, paths
│   ├── dependencies.py     # Singletons LangChain
│   ├── routers/            # health, upload, ask
│   ├── services/           # pdf, ingest, rag
│   └── prompts/            # system prompt do tutor
├── chroma_data/            # persistência ChromaDB (gitignored)
└── tmp_uploads/            # PDFs temporários (gitignored)
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Health check |
| POST | `/upload` | Ingestão de PDF → ChromaDB via LangChain |
| POST | `/ask` | Pergunta com retrieval + `llama3` via Ollama |

### Respostas

**POST /upload** (sucesso):

```json
{
  "message": "PDF indexado com sucesso.",
  "filename": "guia-python.pdf",
  "chunks_indexed": 42
}
```

**POST /ask** (sucesso):

```json
{
  "answer": "Resposta contextual gerada pelo tutor..."
}
```

## Critérios de aceite (Fase 2)

- [x] Ollama rodando com `llama3` e `nomic-embed-text`
- [x] `POST /upload` com PDF retorna `chunks_indexed > 0`
- [x] `POST /ask` responde com contexto do PDF enviado
- [x] Dados persistem em `chroma_data/` após reiniciar a API
- [x] `/docs` e CORS para `localhost:5173` funcionando

## Próximos passos

Na **Fase 3**, criar a UI SvelteKit em `speech-code-web/`. Consulte [../docs/roadmap.md](../docs/roadmap.md).
