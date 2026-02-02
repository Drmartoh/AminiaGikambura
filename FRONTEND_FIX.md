# Frontend Not Starting - Fix Instructions

## Problem
The frontend server is not running on port 3000.

## Solution: Manual Start

### Step 1: Open a NEW PowerShell Terminal

### Step 2: Navigate to Frontend Directory
```powershell
cd C:\Users\pc\CBO\frontend
```

### Step 3: Check if Dependencies are Installed
```powershell
Test-Path node_modules\next
```

If it returns `False`, install dependencies:
```powershell
npm install
```
**Wait for this to complete** (may take 2-5 minutes)

### Step 4: Start the Frontend Server
```powershell
npm run dev
```

**OR** if that doesn't work, try:
```powershell
npx next dev
```

**OR** if that doesn't work, try:
```powershell
node node_modules\next\dist\bin\next.js dev
```

### Step 5: Wait for Compilation

You should see output like:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
✓ Ready in X.Xs
```

### Step 6: Open Browser

Once you see "Ready", open:
**http://localhost:3000**

## Alternative: Use the Batch File

I've created `START_FRONTEND.bat` - double-click it to start the frontend automatically.

## Common Errors & Fixes

### Error: "next is not recognized"
**Fix:** Use `npx next dev` instead of `npm run dev`

### Error: "Cannot find module"
**Fix:** Run `npm install` again

### Error: Port 3000 already in use
**Fix:** 
```powershell
# Find what's using port 3000
netstat -ano | findstr ":3000"
# Kill the process (replace PID with the number shown)
taskkill /PID <PID> /F
```

### Error: Compilation errors
**Fix:** Check the terminal output for specific errors and share them

## Quick Test

While frontend is starting, test backend:
- Backend API: http://localhost:8000/api/ (should now work!)
- Backend Admin: http://localhost:8000/admin/

## Current Status

✅ **Backend**: Running at http://localhost:8000
❌ **Frontend**: Not running - needs manual start

---

**Follow the steps above to start the frontend manually. The backend is working fine!**
