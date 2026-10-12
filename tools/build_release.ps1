# release-orchestrator: gates -> windows build -> installer -> mac bundle
# -> checksums -> stagen -> aufn usb-stick kopieren
#   tools\build_release.ps1 -Version 0.0.1 [-UsbRoot E:\PyLearner] [-Force]
param(
    [Parameter(Mandatory = $true)][string]$Version,
    [string]$UsbRoot = "E:\PyLearner",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"

function Gate($name, [scriptblock]$cmd) {
    Write-Host "== $name" -ForegroundColor Cyan
    & $cmd
    if ($LASTEXITCODE -ne 0) { throw "Gate failed: $name" }
}

Push-Location $root
try {
    # ---------- erstmal die gates (content-check usw.) ----------
    Gate "validate_content" { & $py tools\validate_content.py | Select-Object -Last 2 }
    Gate "validate_lessons" { & $py tools\validate_lessons.py | Select-Object -Last 2 }
    Gate "test_gamification" { & $py tools\test_gamification.py }
    Gate "audit_examples" { & $py tools\audit_examples.py | Select-Object -Last 2 }
    Gate "test_errors" { & $py tools\test_errors.py }
    Gate "test_whatsnew" { & $py tools\test_whatsnew.py }

    # ---------- windows build (runtime + onedir + portable + installer) ----------
    & $PSHOME\powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
        (Join-Path $PSScriptRoot "build_windows.ps1") `
        -Version $Version -Python $py
    if ($LASTEXITCODE -ne 0) { throw "windows build failed" }

    # ---------- mac-bundle ----------
    & $PSHOME\powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
        (Join-Path $PSScriptRoot "build_mac_bundle.ps1") `
        -Version $Version -Python $py

    # ---------- alles stagen ----------
    $rel = Join-Path $root "dist\release"
    $winDir = Join-Path $rel "ver-$Version-windows"
    $macDir = Join-Path $rel "ver-$Version-mac"
    foreach ($d in @($winDir, $macDir)) {
        if (Test-Path $d) { Remove-Item $d -Recurse -Force }
        New-Item -ItemType Directory -Force $d | Out-Null
    }
    Copy-Item (Join-Path $root "dist\installer\Installer.exe") $winDir
    Copy-Item (Join-Path $root "dist\PythonLearner-$Version-windows-portable.zip") $winDir
    Copy-Item (Join-Path $root "dist\PythonLearner-$Version-mac-buildkit.zip") $macDir
    Copy-Item (Join-Path $root "tools\mackit\BUILD-ON-MAC.md") $macDir

    # ---------- checksums / prüfsummen ----------
    foreach ($d in @($winDir, $macDir)) {
        $sums = Get-ChildItem $d -File | Where-Object {
            $_.Name -ne "SHA256SUMS.txt" } | ForEach-Object {
            "{0}  {1}" -f ((Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()), $_.Name
        }
        $sums | Set-Content (Join-Path $d "SHA256SUMS.txt") -Encoding ascii
    }

    # ---------- aufn usb-stick kopieren ----------
    $targets = @(
        @{src = $winDir; dst = Join-Path $UsbRoot "Windows Releases\ver-$Version-windows"},
        @{src = $macDir; dst = Join-Path $UsbRoot "MAC Releases\ver-$Version-mac"}
    )
    foreach ($t in $targets) {
        if ((Test-Path $t.dst) -and -not $Force) {
            throw "USB target exists: $($t.dst) (use -Force to overwrite)" }
        New-Item -ItemType Directory -Force $t.dst | Out-Null
        Copy-Item -Recurse -Force (Join-Path $t.src "*") $t.dst
    }

    Write-Host "`nRelease $Version staged in dist\release and copied to $UsbRoot" -ForegroundColor Green
} finally {
    Pop-Location
}
