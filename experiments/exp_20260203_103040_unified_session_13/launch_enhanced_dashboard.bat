@echo off
echo.
echo ========================================
echo  Black Swarm - Enhanced Engine Visibility
echo ========================================
echo.
echo Starting enhanced dashboard with:
echo  - Per-node engine/model display
echo  - Real-time engine switching updates
echo  - Cost breakdown by engine
echo  - Model distribution analytics
echo.
echo Dashboard will be available at:
echo  http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

python progress_server_enhanced.py --port 8080 --lan

pause