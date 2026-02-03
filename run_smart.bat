@echo off
echo.
echo ============================================================
echo   SMART SWARM - Dynamic Dependency Resolution
echo ============================================================
echo.
echo Tasks run in parallel, automatically detect dependencies,
echo spawn subtasks when needed, and resume when blocked.
echo.

cd /d D:\codingProjects\claude_parasite_brain_suck

set INFERENCE_ENGINE=claude
python run_smart_executor.py

echo.
echo Done. Press any key to exit.
pause
