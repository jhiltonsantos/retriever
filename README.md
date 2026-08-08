# retriever

Índice público dos pacotes do **Retriever**, um assistente de estudos com Agentic RAG, banco vetorial local e escolha de provedor de LLM.

Este repositório não contém código próprio — é um agregador fino que reúne os dois pacotes públicos do projeto como submódulos, para quem quiser explorá-los sem precisar de acesso ao repositório de trabalho privado.

## Pacotes

| Submódulo | Repositório | Descrição |
|-----------|-------------|-----------|
| [`packages/retriever-api`](packages/retriever-api) | [jhiltonsantos/retriever-api](https://github.com/jhiltonsantos/retriever-api) | Backend FastAPI — RAG, LangChain/LangGraph, ChromaDB |
| [`packages/retriever-web`](packages/retriever-web) | [jhiltonsantos/retriever-web](https://github.com/jhiltonsantos/retriever-web) | Frontend SvelteKit 5 + Electron |

## Clonar

```shell
git clone --recurse-submodules https://github.com/jhiltonsantos/retriever.git
```

Se os submódulos vierem vazios:

```shell
git submodule update --init --recursive
```
