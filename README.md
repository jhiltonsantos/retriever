# Retriever Web

SvelteKit 5 frontend for the **Retriever** study assistant, providing a chat interface for Agentic RAG conversations and material indexing.

## Overview

This is the user interface for Retriever. It provides:

- **Chat interface** for conversing with the AI tutor
- **Material indexing** for PDFs and text content
- **Conversation management** with persistent history
- **Settings panel** for LLM provider configuration
- **Material catalog** to view and manage indexed documents
- **Desktop app** via Electron (optional)

## Tech Stack

- **SvelteKit 5** — Full-stack framework (used as SPA only)
- **Svelte 5** — UI components with runes (`$state`, `$derived`, `$effect`)
- **Tailwind CSS v4** — Utility-first styling
- **daisyUI 5** — Component library
- **TypeScript** — Type safety
- **Electron** — Desktop wrapper (optional)

## Design

View the UI prototype and design system on Figma:

[Retriever Design on Figma](https://www.figma.com/design/RtK5mim16aWxxAXAnqudkN/Retriever?m=auto&t=SKNgaiJiXt5qUVHZ-1)

## Prerequisites

- **Node.js 20+**
- **Retriever API** running on port 8000 ([see setup](../retriever-api/README.md))
- **Ollama** running with `nomic-embed-text` (required for embeddings)

## Installation

```bash
npm install
```

Optional: Configure API URL in `.env`:

```bash
PUBLIC_API_URL=http://127.0.0.1:8000
```

## Running the App

### Development

Start the API first (in another terminal):

```bash
cd ../retriever-api
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Then start the frontend:

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Production Build

```bash
npm run build
npm run preview  # Test the build locally
```

The build output is in `build/` — a static SPA that can be deployed anywhere or wrapped in Electron.

### Desktop App (Electron)

```bash
npm run dev:electron
```

This launches the Electron wrapper with the API as a subprocess.

To build the Windows installer:

```bash
npm run build:desktop  # Requires Windows + PowerShell
```

## Features

### Chat Interface

- **Conversational AI** — Ask questions about your indexed materials
- **Source citations** — See which documents were used in each answer
- **Agent steps** — Transparent view of the RAG pipeline (plan, retrieve, evaluate, generate)
- **Conversation history** — Persistent across sessions (stored in SQLite via API)
- **Multiple conversations** — Create, switch, and manage conversations
- **Follow-up questions** — Context-aware responses using conversation history

### Material Indexing

- **PDF upload** — Drag-and-drop or file picker
- **Text input** — Paste text directly
- **Automatic chunking** — Documents split into semantic chunks
- **Local embeddings** — All processing happens on your machine

### Material Catalog

- **View indexed materials** — See all PDFs and texts
- **Metadata display** — Source, type, chunk count, ingestion date
- **Delete materials** — Remove from catalog (note: doesn't remove from vector database)

### Settings

- **LLM provider selection** — Switch between Ollama (local) and OpenRouter (remote)
- **Model selection** — Choose from available models
- **API key management** — Securely store OpenRouter API key
- **Connection testing** — Verify LLM connection before saving

### User Profile

- **Display name** — Personalize your experience
- **Persistent settings** — Stored in SQLite via API

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page with quick actions |
| `/chat` | Chat interface (opens conversation or creates new one) |
| `/chat?conv={id}` | Open specific conversation |
| `/ingest` | Index materials (PDF upload or text input) |
| `/library` | View indexed materials catalog |
| `/history` | Browse and manage conversation history |
| `/settings` | Configure LLM provider and view profile |
| `/info` | About Retriever |

All routes except `/` and `/chat` open as modals over the main content.

## Project Structure

```
retriever-web/
├── src/
│   ├── app.css                    # Tailwind + daisyUI + custom theme
│   ├── app.d.ts                   # TypeScript declarations (window.retriever)
│   ├── app.html                   # HTML template
│   ├── lib/
│   │   ├── api/                   # API client wrappers
│   │   │   ├── config.ts          # API base URL configuration
│   │   │   ├── types.ts           # TypeScript types for API responses
│   │   │   ├── ask.ts             # POST /ask
│   │   │   ├── upload.ts          # POST /upload
│   │   │   ├── ingest.ts          # POST /ingest/text, GET /documents
│   │   │   ├── conversations.ts   # Conversations CRUD
│   │   │   ├── materials.ts       # Materials catalog
│   │   │   ├── profile.ts         # User profile
│   │   │   └── settings.ts        # LLM settings
│   │   ├── chat/                  # Chat logic
│   │   │   ├── types.ts           # Chat message types
│   │   │   ├── conversations.ts   # Reactive conversation store
│   │   │   └── storage.ts         # Legacy localStorage (no longer used)
│   │   ├── components/            # Svelte components
│   │   │   ├── ChatPanel.svelte   # Main chat interface
│   │   │   ├── ChatMessage.svelte # Individual message
│   │   │   ├── ChatComposer.svelte# Input area
│   │   │   ├── ChatSources.svelte # Source citations
│   │   │   ├── AgentSteps.svelte  # Agent pipeline steps
│   │   │   ├── SideNav.svelte     # Sidebar navigation
│   │   │   ├── TopBar.svelte      # Top bar with theme toggle
│   │   │   ├── RouteModal.svelte  # Modal wrapper for routes
│   │   │   ├── HomeCanvas.svelte  # Home background
│   │   │   ├── ChatCanvas.svelte  # Chat background
│   │   │   ├── PdfUpload.svelte   # PDF upload component
│   │   │   ├── TextIngest.svelte  # Text input component
│   │   │   ├── LlmSettingsCard.svelte # LLM settings form
│   │   │   ├── ProfileCard.svelte # User profile form
│   │   │   ├── AboutCard.svelte   # About information
│   │   │   └── OllamaStatus.svelte# Ollama connection status
│   │   ├── nav/                   # Navigation logic
│   │   │   └── background.svelte.ts # Modal route management
│   │   ├── theme.svelte.ts        # Theme toggle logic
│   │   └── alerts.svelte.ts       # Alert/confirm dialogs
│   └── routes/                    # SvelteKit routes
│       ├── +layout.svelte         # Root layout (sidebar + modals)
│       ├── +page.svelte           # Home page
│       ├── chat/
│       │   └── +page.svelte       # Chat interface
│       ├── ingest/
│       │   └── +page.svelte       # Material indexing
│       ├── library/
│       │   └── +page.svelte       # Materials catalog
│       ├── history/
│       │   └── +page.svelte       # Conversation history
│       ├── settings/
│       │   └── +page.svelte       # Settings panel
│       └── info/
│           └── +page.svelte       # About page
├── electron/                      # Electron wrapper
│   ├── main.ts                    # Main process
│   ├── preload.ts                 # Preload script (context bridge)
│   ├── paths.ts                   # Path resolution
│   └── api-manager.ts             # API subprocess management
├── static/                        # Static assets
├── svelte.config.js               # SvelteKit configuration
├── tailwind.config.js             # Tailwind configuration
├── vite.config.ts                 # Vite configuration
└── package.json                   # Dependencies and scripts
```

## Key Concepts

### Static SPA

The app uses `@sveltejs/adapter-static` with `fallback: 'index.html'`, producing a pure SPA:

- **No server-side rendering** — All rendering happens in the browser
- **No `+page.server.ts`** — No server-side logic
- **No `+server.ts`** — No API routes
- **No form actions** — All forms use `fetch`

This allows the app to be:
- Deployed as static files
- Wrapped in Electron without a Node server
- Served from any static host

### DaisyUI + Tailwind

Styling uses **daisyUI components** with **Tailwind utilities**:

```svelte
<button class="btn btn-primary">Click me</button>
<div class="card bg-base-200">Content</div>
```

**No custom CSS** — All styling via utility classes in markup.

### Svelte 5 Runes

The app uses Svelte 5's new reactivity system:

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
  
  function increment() {
    count++;
  }
</script>
```

No `export let` — Use `$props()` instead:

```svelte
<script lang="ts">
  let { message }: { message: string } = $props();
</script>
```

### Theme System

Two themes available:

- `retriever` — Light theme (default)
- `retriever-dark` — Dark theme

Toggle via the sun/moon icon in the top bar. Theme preference persists in `localStorage`.

### Conversation Management

Conversations are managed via the API (SQLite):

- **Create** — New conversation created on first message
- **List** — Sidebar shows recent conversations
- **Switch** — Click conversation to load it
- **Delete** — Remove conversation from history

Conversation ID is in the URL: `/chat?conv={id}`

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (port 5173) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run check` | Type check with `svelte-check` |
| `npm run dev:electron` | Run Electron app in development |
| `npm run build:desktop` | Build Windows installer |

**Note:** `npm run check` is the only automated verification — no test suite or linter configured.

## API Integration

All API calls go through wrappers in `src/lib/api/`:

```typescript
import { askQuestion } from '$lib/api/ask';

const response = await askQuestion(
  'What is the main topic?',
  history,
  conversationId
);
```

The API base URL is configured in `src/lib/api/config.ts`:

- **Desktop (Electron)**: Uses `window.retriever.getApiUrl()`
- **Web**: Uses `PUBLIC_API_URL` env var or defaults to `http://127.0.0.1:8000`

## Desktop App (Electron)

The Electron wrapper (`electron/`) provides:

- **Native window** — Runs the SPA in a desktop window
- **API subprocess** — Automatically starts the FastAPI backend
- **Local data** — Stores database and uploads in user data directory
- **System tray** — Optional tray icon (Windows)

### Architecture

```
Electron Main Process
├── Creates BrowserWindow
├── Starts API subprocess (uvicorn)
├── Waits for health check
└── Loads SPA in window

Electron Preload Script
├── Exposes window.retriever API
├── getApiUrl() — Returns API URL
├── checkOllama() — Checks Ollama status
└── isDesktop — Always true
```

### Development

```bash
npm run dev:electron
```

This:
1. Builds the SPA
2. Compiles Electron main/preload
3. Starts the API subprocess
4. Launches Electron window

### Building

```bash
npm run build:desktop  # Windows only
```

Produces `Retriever Setup.exe` installer in `dist/desktop/`.

## Troubleshooting

### API not connecting

- Ensure API is running on port 8000
- Check `PUBLIC_API_URL` in `.env`
- Verify CORS settings in API (should allow `http://localhost:5173`)

### Ollama not found

- Ensure Ollama is running: `ollama serve`
- Check Ollama status in the app (top bar)
- Verify `nomic-embed-text` is pulled: `ollama pull nomic-embed-text`

### Build fails

- Run `npm run check` to see type errors
- Ensure all dependencies installed: `npm install`
- Clear cache: `rm -rf node_modules .svelte-kit && npm install`

## License

To be defined.
