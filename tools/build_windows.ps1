# windows build: embeddable runtime -> pyinstaller onedir -> inno installer
#   tools\build_windows.ps1 -Version 0.0.1
param(
    [Parameter(Mandatory = $true)][string]$Version,
    [string]$Python = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    [string]$EmbedUrl = "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip"
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent

# --- gebündelte runtime (unter der der learner-code läuft wenns frozen is) ---
$runtime = Join-Path $root "build\runtime"
if (-not (Test-Path "$runtime\python.exe")) {
    $zip = Join-Path $root "build\python-embed.zip"
    New-Item -ItemType Directory -Force (Split-Path $zip) | Out-Null
    Write-Host "Downloading embeddable Python..."
    & curl.exe -L -s -o $zip $EmbedUrl
    Expand-Archive $zip -DestinationPath $runtime -Force
}
& "$runtime\python.exe" -I -X utf8 -c `
    "import json, math, random, itertools, datetime, string; print('runtime ok')"

# --- icon + frozen app (zwei exes, ein onedir) ---
& $Python -m pip install --quiet -r (Join-Path $root "requirements-build.txt")
& $Python (Join-Path $root "tools\make_icon.py") | Out-Null
& $Python -m PyInstaller --noconfirm --clean `
    (Join-Path $root "tools\python_learner.spec") | Select-Object -Last 3

$dist = Join-Path $root "dist\Python Learner"
Copy-Item -Recurse -Force $runtime (Join-Path $dist "runtime")
if (-not (Test-Path "$dist\Python Learner.exe")) {
    throw "PyInstaller output missing: $dist" }

# --- portable-zip ---
& $Python -c "import shutil; shutil.make_archive(r'$root\dist\PythonLearner-$Version-windows-portable', 'zip', r'$root\dist', r'Python Learner')"

# --- inno installer ---
$iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (-not (Test-Path $iscc)) {
    $iscc = "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" }
if (Test-Path $iscc) {
    & $iscc "/DMyAppVersion=$Version" (Join-Path $root "tools\installer.iss") |
        Select-Object -Last 3
} else {
    Write-Warning "ISCC.exe not found - skipping installer build"
}
