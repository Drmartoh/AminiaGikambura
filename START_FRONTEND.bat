@echo off
echo ========================================
echo Starting AGCBO Frontend Server
echo ========================================
echo.

cd /d C:\Users\pc\CBO\frontend

echo Checking dependencies...
if not exist "node_modules\next" (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting Next.js development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
