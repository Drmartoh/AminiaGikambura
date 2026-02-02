# Fix: Next.js Installation Corrupted

## Problem
The Next.js installation is corrupted - missing the `require-hook` module. This happens when npm install is interrupted or incomplete.

## Solution: Reinstall Next.js

### Option 1: Use the Batch File (Easiest)
1. Double-click `frontend/FIX_AND_START.bat`
2. It will automatically:
   - Remove corrupted Next.js
   - Reinstall Next.js 14.0.4
   - Start the dev server

### Option 2: Manual Fix

**Step 1: Remove Corrupted Next.js**
```powershell
cd C:\Users\pc\CBO\frontend
Remove-Item -Recurse -Force node_modules\next
```

**Step 2: Reinstall Next.js**
```powershell
npm install next@14.0.4 --save-exact
```
**Wait for this to complete** (may take 1-2 minutes)

**Step 3: Start Dev Server**
```powershell
npm run dev
```

### Option 3: Complete Reinstall (If Option 2 doesn't work)

**Step 1: Remove Everything**
```powershell
cd C:\Users\pc\CBO\frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
```

**Step 2: Fresh Install**
```powershell
npm install
```
**Wait for this to complete** (may take 3-5 minutes)

**Step 3: Start Dev Server**
```powershell
npm run dev
```

## What to Expect

After reinstalling, you should see:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
✓ Ready in X.Xs
```

Then open: **http://localhost:3000**

## Current Status

✅ **Backend**: Running at http://localhost:8000  
❌ **Frontend**: Next.js installation corrupted - needs reinstall

---

**Use `frontend/FIX_AND_START.bat` for the easiest fix!**
