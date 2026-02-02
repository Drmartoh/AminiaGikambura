@echo off
echo ========================================
echo Fixing Next.js Installation
echo ========================================
echo.

cd /d C:\Users\pc\CBO\frontend

echo Step 1: Removing corrupted Next.js...
if exist "node_modules\next" (
    rmdir /s /q "node_modules\next"
    echo Removed corrupted Next.js
) else (
    echo Next.js folder not found
)

echo.
echo Step 2: Reinstalling Next.js 14.0.4...
call npm install next@14.0.4 --save-exact

echo.
echo Step 3: Starting development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
