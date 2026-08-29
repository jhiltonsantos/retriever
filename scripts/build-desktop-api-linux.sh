#!/usr/bin/env bash
set -euo pipefail

API_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="$API_ROOT/../retriever-desktop/src-tauri/binaries"

if [ ! -f "$API_ROOT/.venv/bin/activate" ]; then
    echo "Active or create a virtual environment in retriever-api/.venv before running." >&2
    exit 1
fi

cd "$API_ROOT"
source .venv/bin/activate
pip install pyinstaller

rm -rf build dist

pyinstaller --onefile --name retriever-api \
    --hidden-import uvicorn.logging \
    --hidden-import uvicorn.loops \
    --hidden-import uvicorn.loops.auto \
    --hidden-import uvicorn.protocols \
    --hidden-import uvicorn.protocols.http \
    --hidden-import uvicorn.protocols.http.auto \
    --hidden-import uvicorn.protocols.websockets \
    --hidden-import uvicorn.protocols.websockets.auto \
    --hidden-import uvicorn.lifespan \
    --hidden-import uvicorn.lifespan.on \
    --hidden-import langchain_classic \
    --hidden-import langchain_community \
    --hidden-import langchain_ollama \
    --hidden-import langchain_chroma \
    --hidden-import chromadb \
    --hidden-import chromadb_rust_bindings \
    --collect-submodules chromadb \
    --collect-data chromadb \
    --hidden-import pypdf \
    desktop_entry.py

TARGET_TRIPLE="$(rustc --print host-tuple)"
mkdir -p "$BIN_DIR"
cp "dist/retriever-api" "$BIN_DIR/retriever-api-$TARGET_TRIPLE"
chmod +x "$BIN_DIR/retriever-api-$TARGET_TRIPLE"

echo "Generated Linux AppImage in $BIN_DIR/retriever-api-$TARGET_TRIPLE"
