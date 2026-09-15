#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

$ApiRoot = Split-Path -Parent $PSScriptRoot
$BinDir = Join-Path $ApiRoot "../retriever-desktop/src-tauri/binaries"

$VenvActivate = Join-Path $ApiRoot ".venv/Scripts/Activate.ps1"
if (-not (Test-Path $VenvActivate)) {
    Write-Error "Active or create a virtual environment in retriever-api/.venv before running."
    exit 1
}

Set-Location $ApiRoot
& $VenvActivate
pip install pyinstaller

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build, dist

pyinstaller --onefile --name retriever-api `
    --hidden-import uvicorn.logging `
    --hidden-import uvicorn.loops `
    --hidden-import uvicorn.loops.auto `
    --hidden-import uvicorn.protocols `
    --hidden-import uvicorn.protocols.http `
    --hidden-import uvicorn.protocols.http.auto `
    --hidden-import uvicorn.protocols.websockets `
    --hidden-import uvicorn.protocols.websockets.auto `
    --hidden-import uvicorn.lifespan `
    --hidden-import uvicorn.lifespan.on `
    --hidden-import langchain_classic `
    --hidden-import langchain_community `
    --hidden-import langchain_ollama `
    --hidden-import langchain_chroma `
    --hidden-import chromadb `
    --hidden-import chromadb_rust_bindings `
    --collect-submodules chromadb `
    --collect-data chromadb `
    --hidden-import pypdf `
    --collect-submodules keyring.backends `
    --copy-metadata keyring `
    desktop_entry.py

$TargetTriple = (rustc --print host-tuple).Trim()
New-Item -ItemType Directory -Force -Path $BinDir | Out-Null
Copy-Item "dist/retriever-api.exe" "$BinDir/retriever-api-$TargetTriple.exe"

Write-Host "Generated Windows sidecar in $BinDir/retriever-api-$TargetTriple.exe"
