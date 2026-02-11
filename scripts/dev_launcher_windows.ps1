$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$PythonExe = Join-Path $RootDir ".venv\Scripts\python.exe"
if (Test-Path $PythonExe) {
    & $PythonExe (Join-Path $RootDir "scripts\dev_launcher.py")
    exit $LASTEXITCODE
}
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 (Join-Path $RootDir "scripts\dev_launcher.py")
    exit $LASTEXITCODE
}
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python (Join-Path $RootDir "scripts\dev_launcher.py")
    exit $LASTEXITCODE
}
throw "Python was not found. Install Python 3.11+ first."
