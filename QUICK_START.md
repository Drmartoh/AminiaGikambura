# Quick Start Guide - AGCBO Digital Hub

## Current Status

Both servers have been started in the background. Here's how to access them:

### Backend Server (Django)
- **URL**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

### Frontend Server (Next.js)
- **URL**: http://localhost:3000
- **Status**: Starting up (may take 1-2 minutes on first run)

## Troubleshooting

If the homepage is not opening:

### 1. Check if servers are running:
```powershell
# Check Node.js processes
Get-Process -Name node

# Check Python processes  
Get-Process -Name python
```

### 2. Check server logs:
The servers are running in background terminals. Check the terminal output for any errors.

### 3. Manual Start (if needed):

**Backend:**
```powershell
cd C:\Users\pc\CBO\backend
python manage.py runserver
```

**Frontend:**
```powershell
cd C:\Users\pc\CBO\frontend
npm run dev
```

### 4. Common Issues:

**Port already in use:**
- Backend: Change port with `python manage.py runserver 8001`
- Frontend: Change port with `npm run dev -- -p 3001`

**Dependencies not installed:**
```powershell
cd frontend
npm install
```

**Database not migrated:**
```powershell
cd backend
python manage.py migrate
```

### 5. Create Admin User:
```powershell
cd backend
python manage.py createsuperuser
```

Then login at http://localhost:8000/admin/

### 6. Load Sample Data:
```powershell
cd backend
python manage.py seed_data
```

## Next Steps

1. Wait 1-2 minutes for Next.js to compile
2. Open http://localhost:3000 in your browser
3. If you see errors, check the browser console (F12)
4. Check the terminal output for compilation errors

## Need Help?

- Check browser console (F12) for frontend errors
- Check terminal output for server errors
- Verify both servers are running on correct ports
