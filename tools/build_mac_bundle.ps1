# baut PythonLearner-<Version>-mac-buildkit.zip: ein self-contained kit
# das auf nem apple-silicon-mac dann die native .app/.dmg erzeugt
param(
    [Parameter(Mandatory = $true)][string]$Version,
    [string]$Python = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$kitName = "PythonLearner-$Version-mac-buildkit"
$base = Join-Path $root "build\mac_kit"
$stage = Join-Path $base $kitName
if (Test-Path $base) { Remove-Item $base -Recurse -Force }
New-Item -ItemType Directory -Force $stage | Out-Null

Copy-Item -Recurse (Join-Path $root "app") (Join-Path $stage "app")
Copy-Item (Join-Path $root "requirements.txt") $stage
Copy-Item (Join-Path $root "requirements-build.txt") $stage
New-Item -ItemType Directory -Force (Join-Path $stage "tools") | Out-Null
Copy-Item (Join-Path $root "tools\entry_server.py") (Join-Path $stage "tools")
Copy-Item (Join-Path $root "tools\make_icon.py") (Join-Path $stage "tools")
foreach ($f in @("build_mac_app.sh", "Build Python Learner.command",
                 "BUILD-ON-MAC.md")) {
    Copy-Item (Join-Path $PSScriptRoot "mackit\$f") $stage
}

Get-ChildItem -Recurse -Directory -Filter __pycache__ $stage |
    Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter *.pyc $stage | Remove-Item -Force

$out = Join-Path $root "dist\$kitName.zip"
New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
& $Python (Join-Path $PSScriptRoot "mac_zip.py") $base $out
Write-Host "Built $out"
