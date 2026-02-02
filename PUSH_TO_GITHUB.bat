@echo off
REM Run this from the CBO project root to prepare and push to a NEW GitHub repo.
REM You must create the empty repo on GitHub first, then run the commands printed at the end.

cd /d "%~dp0"

echo Checking Git...
git status >nul 2>&1
if errorlevel 1 (
    echo Initializing Git...
    git init
)

echo Adding all files (respects .gitignore)...
git add .

echo.
git status --short
echo.

set /p confirm="Commit all these changes? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)

set /p msg="Commit message (default: Initial commit: CBO web app): "
if "%msg%"=="" set msg=Initial commit: CBO web app

git commit -m "%msg%"
git branch -M main 2>nul

echo.
echo ============================================================
echo   Next steps (run these yourself after creating a repo on GitHub):
echo ============================================================
echo   1. On GitHub: New repository, no README/.gitignore. Copy the repo URL.
echo   2. Run:
echo.
echo      git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
echo      git push -u origin main
echo.
echo   Replace the URL with your actual repository URL.
echo ============================================================
pause
