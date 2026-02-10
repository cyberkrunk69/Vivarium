@echo off
echo ============================================================
echo   BLACK SWARM - Unified Execution
echo ============================================================
echo.
echo Using Groq inference engine
echo.
set INFERENCE_ENGINE=groq

cd /d D:\codingProjects\swarm_workspace

echo.
echo Building container...
docker-compose build

echo.
echo Starting swarm with INFERENCE_ENGINE=%INFERENCE_ENGINE%...
docker-compose up

echo.
echo Done. Press any key to exit.
pause
