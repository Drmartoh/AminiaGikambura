@echo off
echo Starting AGCBO Digital Hub Servers...
echo.

echo [1/2] Starting Backend Server (Django)...
start "Backend Server" cmd /k "cd /d C:\Users\pc\CBO\backend && python manage.py runserver"
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Server (Next.js)...
start "Frontend Server" cmd /k "cd /d C:\Users\pc\CBO\frontend && npm run dev"

echo.
echo Servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window (servers will keep running)...
pause >nul
