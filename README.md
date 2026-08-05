# Retriever Web

Frontend SvelteKit do assistente de estudos **Retriever** — interface conectada ao RAG (FastAPI, LangChain, ChromaDB e Ollama).

Este submodule faz parte do monorepo [retriever](https://github.com/jhiltonsantos/retriever), onde vive a documentação completa.

## Stack de UI

- [Tailwind CSS v4](https://tailwindcss.com/) — utilitários no markup
- [daisyUI 5](https://daisyui.com/) — componentes (`card`, `btn`, `alert`, `chat`, `badge`)
- Tema escuro customizado **`retriever`** definido em `src/app.css`

## Pré-requisitos

- Node.js 20 ou superior
- API rodando em [retriever-api](../retriever-api/) na porta 8000
- Ollama ativo com `nomic-embed-text` — os embeddings são sempre locais

## Configuração

```shell
cp .env.example .env
npm install
```

Opcional — altere a URL da API em `.env`:

```
PUBLIC_API_URL=http://127.0.0.1:8000
```

## Como rodar

Terminal 1 — API:

```shell
cd ../retriever-api
source .venv/bin/activate      # Windows: .\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 — Frontend:

```shell
npm run dev
```

Abra [http://localhost:5173](http://localhost:5173).

## Rotas

| Rota | Descrição |
|------|-----------|
| `/` | Home com dois cards — upload de PDF e chat com o tutor |
| `/upload` | Envio e indexação de PDF no ChromaDB |
| `/chat` | Conversa com thread de mensagens e histórico persistido |

## Estrutura

```
retriever-web/
├── src/
│   ├── app.css               # Tailwind, DaisyUI e tema retriever
│   ├── app.d.ts              # tipagem de window.retriever
│   ├── lib/
│   │   ├── api/              # config, types, ask, upload
│   │   ├── chat/             # types e localStorage do historico
│   │   └── components/       # ActionCard, ChatPanel, PdfUpload, etc.
│   └── routes/
│       ├── +page.svelte      # home com cards de navegacao
│       ├── upload/+page.svelte
│       └── chat/+page.svelte
├── electron/                 # main, preload, paths, api-manager
└── .env.example
```

## Aplicação estática

O build usa `adapter-static` com `fallback: index.html`, produzindo uma SPA pura — é o que permite carregá-la dentro do Electron sem servidor Node.

Consequência permanente: **não existem `+page.server.ts`, `+server.ts` nem form actions**. Toda chamada ao backend é `fetch` client-side através de `src/lib/api/`.

## Fluxo de integração

| Ação | Onde | Como chama a API |
|------|------|------------------|
| Upload de PDF | `/upload` com `PdfUpload.svelte` | `fetch` client-side para `POST /upload` |
| Pergunta | `/chat` com `ChatPanel.svelte` | `fetch` client-side via `src/lib/api/ask.ts` |

## Histórico de conversas

O chat mantém a thread de mensagens em **localStorage**, na chave `retriever:chat-history`.

| Comportamento | Detalhe |
|---------------|---------|
| Persistência | Mesmo navegador e dispositivo; sobrevive ao recarregar |
| Limpar | O botão "Limpar" remove as mensagens e apaga o storage |
| Erros da API | Não entram no histórico — aparecem como alerta temporário |
| Follow-up contextual | A API ainda recebe só a pergunta atual; memória de conversa está no roadmap |

## Scripts

| Comando | Descrição |
|---------|-----------|
| `npm run dev` | Servidor de desenvolvimento na porta 5173 |
| `npm run build` | Build de produção |
| `npm run preview` | Serve o build localmente |
| `npm run check` | Verificação de tipos com `svelte-check` |
| `npm run dev:electron` | Janela Electron com a API em subprocesso |
| `npm run build:desktop` | Instalador Windows, exige PowerShell |

`npm run check` é a única verificação automática — não há suíte de testes nem linter configurados.
