# Restart Instructions - AGCBO Digital Hub

## ✅ Servers Have Been Restarted

Both servers are now starting in the background.

### Current Status:
- **Backend (Django)**: Starting at http://localhost:8000
- **Frontend (Next.js)**: Compiling at http://localhost:3000

## ⏰ Wait Time

**Please wait 30-60 seconds** for:
1. Backend to fully start (usually 5-10 seconds)
2. Frontend to compile (usually 30-60 seconds on first run)

## 🌐 Access the Application

Once ready, open your browser and go to:
- **Homepage**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

## 🔍 How to Check if Servers are Ready

### Option 1: Check Browser
1. Open http://localhost:3000
2. If you see the homepage → ✅ Working!
3. If you see "This site can't be reached" → ⏳ Still starting

### Option 2: Check Terminal Output
Look for these messages:

**Backend:**
```
Starting development server at http://127.0.0.1:8000/
```

**Frontend:**
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
✓ Ready in X.Xs
```

## 🛠️ If Frontend Still Doesn't Work

### Manual Start (Recommended):

1. **Open a NEW PowerShell terminal**

2. **Start Backend:**
```powershell
cd C:\Users\pc\CBO\backend
python manage.py runserver
```
Wait until you see: `Starting development server at http://127.0.0.1:8000/`

3. **Open ANOTHER NEW PowerShell terminal**

4. **Start Frontend:**
```powershell
cd C:\Users\pc\CBO\frontend
npm run dev
```
Wait until you see: `✓ Ready in X.Xs`

5. **Open Browser:**
Go to http://localhost:3000

## 🐛 Troubleshooting

### Port Already in Use:
```powershell
# Kill processes on ports
netstat -ano | findstr ":3000"
netstat -ano | findstr ":8000"
# Then kill the PID shown
```

### Frontend Compilation Errors:
Check the terminal where `npm run dev` is running for error messages.

### Backend Errors:
Check the terminal where `python manage.py runserver` is running for error messages.

## 📝 Quick Test URLs

- Backend API: http://localhost:8000/api/ (should show API endpoints)
- Backend Admin: http://localhost:8000/admin/ (should show login)
- Frontend: http://localhost:3000 (should show homepage)

## ⚡ Quick Restart Script

I've created `START_SERVERS.bat` - double-click it to start both servers automatically.

---

**The servers are starting now. Please wait 30-60 seconds and then try http://localhost:3000 in your browser.**
