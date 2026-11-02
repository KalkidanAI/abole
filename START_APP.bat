@echo off
echo ========================================
echo Starting Abole Coffee Leaf Disease Detection
echo ========================================
echo.

echo Step 1: Starting Backend Server (Port 8000)...
start "Abole Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
timeout /t 3 /nobreak > nul

echo Step 2: Starting Frontend Server (Port 3000)...
echo.
echo NOTE: If this is your first time, run this command manually:
echo   cd frontend
echo   npm install
echo.
start "Abole Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo Frontend App: http://localhost:3000
echo.
echo Access the application at: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul
