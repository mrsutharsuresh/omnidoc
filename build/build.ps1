$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$BuildDir = "$PSScriptRoot"
$Output = "$BuildDir\output"
$Venv = "$BuildDir\venv"
$Python = "$Venv\Scripts\python.exe"
$PyInstaller = "$Venv\Scripts\pyinstaller.exe"
$Version = (Get-Content "$ProjectRoot\omnidoc\__init__.py" | Select-String "__version__ = '(.*)'").Matches.Groups[1].Value

if (-not (Test-Path $Output)) { New-Item -ItemType Directory -Path $Output | Out-Null }

Write-Host "Building OmniDoc v$Version..."
Write-Host "Using PyInstaller..."

& $PyInstaller --noconfirm --clean `
    --name "OmniDoc_v$Version" `
    --onefile `
    --add-data "$ProjectRoot\omnidoc\templates;omnidoc\templates" `
    --add-data "$ProjectRoot\omnidoc\static;omnidoc\static" `
    --paths "$ProjectRoot" `
    --hidden-import "omnidoc.features.smart_convert" `
    --hidden-import "engineio.async_drivers.threading" `
    --hidden-import "pymdownx" `
    --hidden-import "pymdownx.betterem" `
    --hidden-import "pymdownx.superfences" `
    --hidden-import "pymdownx.tabbed" `
    --hidden-import "pymdownx.details" `
    --hidden-import "pymdownx.magiclink" `
    --hidden-import "pymdownx.tasklist" `
    --hidden-import "pymdownx.arithmatex" `
    --hidden-import "pymdownx.highlight" `
    --hidden-import "pymdownx.inlinehilite" `
    --hidden-import "pymdownx.keys" `
    --hidden-import "pymdownx.smartsymbols" `
    --hidden-import "pymdownx.snippets" `
    --hidden-import "pymdownx.tilde" `
    --hidden-import "pymdownx.caret" `
    --hidden-import "pymdownx.mark" `
    --hidden-import "pymdownx.emoji" `
    --hidden-import "pymdownx.saneheaders" `
    --distpath "$Output" `
    --workpath "$BuildDir\temp" `
    --specpath "$BuildDir" `
    "$ProjectRoot\run.py"

Write-Host "Build Complete: $Output\OmniDoc_v$Version.exe" -ForegroundColor Green
