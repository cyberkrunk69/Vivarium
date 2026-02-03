@echo off
echo ============================================================
echo   BLACK SWARM - Quick Launch
echo ============================================================
echo:
echo   1. Claude (smart, Anthropic API)
echo   2. Groq (fast, Llama 70B)
echo   3. Auto (picks per-task)
echo:
choice /c 123 /n /m "Select engine [1-3]: "

if errorlevel 3 set INFERENCE_ENGINE=auto
if errorlevel 2 set INFERENCE_ENGINE=groq
if errorlevel 1 set INFERENCE_ENGINE=claude

cd /d D:\codingProjects\claude_parasite_brain_suck
echo:
echo Starting swarm with %INFERENCE_ENGINE% engine...
echo:
python grind_spawner_unified.py --delegate --budget 1.00 --once

echo:
echo Done. Press any key to exit.
pause
