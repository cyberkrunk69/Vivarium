@echo off
echo Starting Dual-Server Infrastructure...
cd /d "%~dp0..\.."
python experiments/exp_20260203_102443_unified_session_5/lan_server.py
pause