@echo off
echo Starting LAN Server (network accessible)...
cd /d "%~dp0..\.."
python experiments/exp_20260203_102443_unified_session_5/lan_server.py --lan-only
pause