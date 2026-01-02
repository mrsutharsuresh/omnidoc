$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$BuildDir = "$PSScriptRoot"
$Output = "$BuildDir\output"
$Venv = "$BuildDir\venv"
$Python = "$Venv\Scripts\python.exe"
$PyInstaller = "$Venv\Scripts\pyinstaller.exe"
$Version = (Get-Content "$ProjectRoot\docnexus\__init__.py" | Select-String "__version__ = '(.*)'").Matches.Groups[1].Value

if (-not (Test-Path $Output)) { New-Item -ItemType Directory -Path $Output | Out-Null }

Write-Host "Building DocNexus v$Version..."
Write-Host "Using PyInstaller..."

# Base PyInstaller Arguments
$PyInstallerArgs = @(
    "--noconfirm",
    "--clean",
    "--name", "DocNexus_v$Version",
    "--icon", "$ProjectRoot\docnexus\static\logo.ico",
    "--onefile",
    "--add-data", "$ProjectRoot\docnexus\templates;docnexus\templates",
    "--add-data", "$ProjectRoot\docnexus\static;docnexus\static",
    "--paths", "$ProjectRoot",
    "--distpath", "$Output",
    "--workpath", "$BuildDir\temp",
    "--specpath", "$BuildDir\spec"
)

# Standard Hidden Imports
$HiddenImports = @(
    "docnexus.features",
    "docnexus.features.smart_convert",
    "engineio.async_drivers.threading",
    "pymdownx",
    "pymdownx.betterem", 
    "pymdownx.superfences",
    "pymdownx.tabbed",
    "pymdownx.details",
    "pymdownx.magiclink",
    "pymdownx.tasklist",
    "pymdownx.arithmatex",
    "pymdownx.highlight",
    "pymdownx.inlinehilite",
    "pymdownx.keys",
    "pymdownx.smartsymbols",
    "pymdownx.snippets",
    "pymdownx.tilde",
    "pymdownx.caret",
    "pymdownx.mark",
    "pymdownx.emoji",
    "pymdownx.saneheaders"
)

foreach ($import in $HiddenImports) {
    $PyInstallerArgs += "--hidden-import"
    $PyInstallerArgs += $import
}

# Conditional: Premium Plugins
$PluginsDevPath = Join-Path $ProjectRoot "docnexus\plugins_dev"
if (Test-Path $PluginsDevPath) {
    Write-Host " [PREMIUM] Detected plugins_dev. Including in build..." -ForegroundColor Cyan
    $PyInstallerArgs += "--add-data"
    $PyInstallerArgs += "$PluginsDevPath;docnexus\plugins_dev"
    
    # We also need to help PyInstaller find the python modules inside plugins_dev
    # Note: We can't just list them here because we don't know their names yet.
    # We rely on the `hook-docnexus.plugins_dev.py` (created in Task 0.3) or manual entry if strict.
    # For now, we trust the Hook algorithm to find them if we add the runtime hook.
}

# Run PyInstaller
Write-Host "Running command: $PyInstaller $PyInstallerArgs"
& $PyInstaller $PyInstallerArgs "$ProjectRoot\docnexus\app.py"

if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller failed with exit code $LASTEXITCODE"
}
Write-Host "Build Complete! Output in $Output" -ForegroundColor Green
