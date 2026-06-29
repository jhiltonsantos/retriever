$ErrorActionPreference = "Stop"

$apiRoot = $PSScriptRoot | Split-Path -Parent
$webRoot = Join-Path $apiRoot ".." "speech-code-web"
$outDir = Join-Path $webRoot "resources" "api"

Push-Location $apiRoot

if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Error "Ative ou crie o venv em speech-code-api/.venv antes do build."
}

.\.venv\Scripts\Activate.ps1
pip install pyinstaller

if (Test-Path "dist\speechcode-api") {
    Remove-Item -Recurse -Force "dist\speechcode-api"
}

pyinstaller speechcode-api.spec --noconfirm

if (Test-Path $outDir) {
    Remove-Item -Recurse -Force $outDir
}
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

Copy-Item -Recurse -Force "dist\speechcode-api\*" $outDir

Write-Host "API desktop copiada para $outDir"

Pop-Location
