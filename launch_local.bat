@echo off
echo ============================================================
echo   BLACK SWARM - Unified Execution
echo ============================================================
echo.
echo Select inference engine:
echo   1. Claude Code (smarter, uses Anthropic API)
echo   2. Groq (faster, uses Llama models)
echo   3. Auto (intelligent per-task selection)
echo.

set /p ENGINE_CHOICE="Enter choice (1-3, default=3): "

if "%ENGINE_CHOICE%"=="1" (
    set INFERENCE_ENGINE=claude
    echo Using: Claude Code
) else if "%ENGINE_CHOICE%"=="2" (
    set INFERENCE_ENGINE=groq
    echo Using: Groq
) else (
    set INFERENCE_ENGINE=auto
    echo Using: Auto-selection
)

cd /d D:\codingProjects\claude_parasite_brain_suck

echo.
echo Building container...
docker-compose build

echo.
echo Starting swarm with INFERENCE_ENGINE=%INFERENCE_ENGINE%...
docker-compose up

echo.
echo Done. Press any key to exit.
pause
