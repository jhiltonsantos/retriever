# Retriever API

Backend FastAPI do assistente de estudos **Retriever** — RAG para Programação e Inglês, com banco vetorial local.

Este submodule faz parte do monorepo [retriever](https://github.com/jhiltonsantos/retriever), onde vive a documentação completa.

## Pré-requisitos

- Python 3.11 ou superior
- [Ollama](https://ollama.com/download) rodando — obrigatório, os embeddings são sempre locais
- Modelo de embeddings baixado

```shell
ollama pull nomic-embed-text
```

O `llama3` só é necessário para quem for usar o LLM local em vez de uma API remota.

## Como rodar

```shell
source .venv/bin/activate      # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Estrutura

```
retriever-api/
├── main.py                 # bootstrap: create_app()
├── desktop_entry.py        # entrypoint do executavel empacotado
├── app/
│   ├── factory.py          # FastAPI, CORS, routers
│   ├── config.py           # variaveis de ambiente e constantes
│   ├── dependencies.py     # ponto unico de wiring
│   ├── routers/            # health, upload, ask
│   ├── services/           # pdf, ingest, rag
│   └── prompts/            # system prompt do tutor
├── chroma_data/            # persistencia ChromaDB, fora do versionamento
└── tmp_uploads/            # PDFs temporarios, fora do versionamento
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Health check |
| POST | `/upload` | Ingestão de PDF no ChromaDB via LangChain |
| POST | `/ask` | Pergunta com retrieval e geração |

### Respostas

**POST /upload**

```json
{
  "message": "PDF indexado com sucesso.",
  "filename": "guia-python.pdf",
  "chunks_indexed": 42
}
```

**POST /ask**

```json
{
  "answer": "Resposta contextual gerada pelo tutor..."
}
```

O contrato completo, incluindo a evolução planejada, está em `docs/api-contract.md` no monorepo.
