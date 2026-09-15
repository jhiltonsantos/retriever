# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0-beta.2] - 2026-09-15

### Added

- Windows distribution: an `.exe` installer (NSIS), built alongside the existing Linux AppImage in the same release.

### Known limitations

- **Linux and Windows only.**.
- **Requires a local Ollama installation** with the `nomic-embed-text` model pulled, even when the chat LLM itself is a remote provider — embeddings always run locally.
- **API key rotation while the app is running is not supported yet.** Changing the stored key requires restarting the app for it to take effect.
- No auto-update mechanism; new versions must be downloaded manually from the releases page.

## [0.1.0-beta.1] - 2026-09-11

First beta release of the Retriever desktop app, distributed as a Linux AppImage.

### Included

- Desktop shell built with Tauri, spawning the `retriever-api` backend as a sidecar process.
- Linear RAG pipeline: PDF upload and ingestion, chat-based question answering over ingested documents.
- Chat history persisted locally in the browser (no server-side conversation state).
- Secure local storage of the LLM provider API key via the OS keyring (Secret Service / Keychain / Credential Locker) when running inside the desktop app.
- Splash screen with backend health polling before showing the main window.
- Single-instance behavior (relaunching the app refocuses the existing window).

### Known limitations

- **Linux only.** Windows (`.msi`) and macOS (`.dmg`) bundles are not produced yet.
- **Requires a local Ollama installation** with the `nomic-embed-text` model pulled, even when the chat LLM itself is a remote provider — embeddings always run locally.
- **API key rotation while the app is running is not supported yet.** Changing the stored key requires restarting the app for it to take effect.
- No auto-update mechanism; new versions must be downloaded manually from the releases page.
