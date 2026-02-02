# Manual Start Instructions

## The Issue
The `next` command isn't being found because npm install is still running or didn't complete properly.

## Solution: Manual Start

### Step 1: Complete npm install (if still running)

Open a **NEW PowerShell terminal** and run:

```powershell
cd C:\Users\pc\CBO\frontend
npm install
```

**Wait for it to complete** - this may take 2-5 minutes. You'll see:
```
added 500+ packages, and audited 600+ packages
```

### Step 2: Start Backend Server

Open a **NEW PowerShell terminal** and run:

```powershell
cd C:\Users\pc\CBO\backend
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 3: Start Frontend Server

Open **ANOTHER NEW PowerShell terminal** and run:

```powershell
cd C:\Users\pc\CBO\frontend
npm run dev
```

**OR** if that doesn't work, try:

```powershell
cd C:\Users\pc\CBO\frontend
npx next dev
```

**OR** if that doesn't work, try:

```powershell
cd C:\Users\pc\CBO\frontend
node node_modules\next\dist\bin\next.js dev
```

You should see:
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
```

### Step 4: Open in Browser

Once both servers are running:
1. Open your browser
2. Go to: **http://localhost:3000**

## Alternative: Use the Batch File

I've created `START_SERVERS.bat` - double-click it to start both servers automatically.

## Troubleshooting

### If npm install fails:
```powershell
cd C:\Users\pc\CBO\frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm install
```

### If "next" command not found:
The package.json has been updated to use the direct path. Try:
```powershell
npm run dev
```

### If port 3000 is already in use:
```powershell
npm run dev -- -p 3001
```
Then open http://localhost:3001

### Check if servers are running:
```powershell
# Check backend
netstat -ano | findstr ":8000"

# Check frontend  
netstat -ano | findstr ":3000"
```

## Quick Test

1. Backend API: http://localhost:8000/api/ (should show API endpoints)
2. Backend Admin: http://localhost:8000/admin/ (should show login)
3. Frontend: http://localhost:3000 (should show homepage)

## Need Help?

- Check terminal output for error messages
- Make sure Python and Node.js are installed
- Verify you're in the correct directories
- Check browser console (F12) for frontend errors
