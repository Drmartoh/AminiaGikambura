# Deploying CBO Web App: GitHub → PythonAnywhere

This guide walks you through:
1. **Pushing the project to a new GitHub repository**
2. **Deploying the Django backend on PythonAnywhere**
3. **Running the frontend** (Next.js on Vercel or static export)

---

## Part 1: Push to GitHub

### 1.1 Create a new repository on GitHub

1. Go to [github.com](https://github.com) and sign in.
2. Click **New repository** (or **+** → **New repository**).
3. Choose a name (e.g. `cbo-webapp`), set visibility (Public/Private), **do not** initialize with README, .gitignore, or license.
4. Click **Create repository**.
5. Copy the repository URL (e.g. `https://github.com/YOUR_USERNAME/cbo-webapp.git`).

### 1.2 Initialize Git and push (run in project root: `CBO`)

Open PowerShell or Command Prompt in `C:\Users\pc\CBO` and run:

```powershell
# Initialize Git (if not already)
git init

# Add all files (respects .gitignore: no .env, node_modules, db.sqlite3, etc.)
git add .

# First commit
git commit -m "Initial commit: CBO web app (Django + Next.js)"

# Rename branch to main if needed
git branch -M main

# Add your GitHub repo (replace with YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

If Git asks for credentials, use a **Personal Access Token** (not your GitHub password):
- GitHub → Settings → Developer settings → Personal access tokens → Generate new token (with `repo` scope).

---

## Part 2: Deploy Django backend on PythonAnywhere

**Note:** PythonAnywhere hosts Python/Django only. The Next.js frontend will be deployed separately (e.g. Vercel) and will call this API.

### 2.1 Create account and get a subdomain

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com) (free tier is fine).
2. Your site will be: `https://YOUR_USERNAME.pythonanywhere.com`.

### 2.2 Clone your repo

In the PythonAnywhere **Consoles** tab, open a **Bash** console and run:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git CBO
cd CBO
```

### 2.3 Create virtualenv and install dependencies

```bash
cd ~/CBO
python3 -m venv venv
source venv/bin/activate   # On Windows Bash: venv\Scripts\activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 2.4 Set environment variables

Create a `.env` file in the **backend** folder (or in project root and load it before running Django). In the Bash console:

```bash
cd ~/CBO/backend
nano .env
```

Add (replace values as needed):

```env
SECRET_KEY=your-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
DB_ENGINE=sqlite
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://YOUR_USERNAME.pythonanywhere.com
```

Save (Ctrl+O, Enter, Ctrl+X in nano).

**Generate a secret key (optional):**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 2.5 Migrate and collect static files

```bash
cd ~/CBO
source venv/bin/activate
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
```

Create a superuser for Django admin (optional):

```bash
python manage.py createsuperuser
```

### 2.6 Configure the Web app (WSGI)

1. In PythonAnywhere dashboard go to **Web**.
2. Click **Add a new web app** → **Manual configuration** → **Python 3.10** (or the version you used).
3. Under **Code**, set:
   - **Source code:** `/home/YOUR_USERNAME/CBO`
   - **Working directory:** `/home/YOUR_USERNAME/CBO/backend`
4. Under **WSGI configuration file**, click the link and replace the file content with:

```python
import os
import sys

# Project root
path = '/home/YOUR_USERNAME/CBO'
if path not in sys.path:
    sys.path.insert(0, path)

# Backend directory for Django
sys.path.insert(0, '/home/YOUR_USERNAME/CBO/backend')

os.environ['DJANGO_SETTINGS_MODULE'] = 'agcbo.settings'

# Load .env from backend folder
from pathlib import Path
env_path = Path('/home/YOUR_USERNAME/CBO/backend') / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace `YOUR_USERNAME` with your PythonAnywhere username in both **Code** and the WSGI file.

5. Under **Static files**, add:
   - **URL:** `/static/`
   - **Directory:** `/home/YOUR_USERNAME/CBO/backend/staticfiles`
   - **URL:** `/media/`
   - **Directory:** `/home/YOUR_USERNAME/CBO/backend/media`

6. Click **Reload** for your web app.

Your API will be at: `https://YOUR_USERNAME.pythonanywhere.com/api/`

---

## Part 3: Deploy Next.js frontend (Vercel – recommended)

PythonAnywhere does **not** run Node.js, so host the Next.js app on Vercel (free) and point it to your PythonAnywhere API.

### 3.1 Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub.
2. **Import** your GitHub repository (`YOUR_USERNAME/YOUR_REPO_NAME`).
3. Set **Root Directory** to `frontend`.
4. Add **Environment Variable:**
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://YOUR_USERNAME.pythonanywhere.com/api`
5. Deploy. Vercel will build and give you a URL like `https://your-app.vercel.app`.

### 3.2 Allow frontend in Django CORS

In your PythonAnywhere **backend** `.env`, ensure:

```env
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app,https://YOUR_USERNAME.pythonanywhere.com
```

Then reload the web app in the **Web** tab.

---

## Quick reference

| Step            | Where        | What to do |
|-----------------|-------------|------------|
| Push code       | Your PC     | `git init`, `git add .`, `git commit`, `git remote add origin <url>`, `git push -u origin main` |
| Backend         | PythonAnywhere | Clone repo, venv, `pip install -r backend/requirements.txt`, `.env`, migrate, collectstatic, WSGI, static/media, Reload |
| Frontend        | Vercel      | Import repo, root = `frontend`, set `NEXT_PUBLIC_API_URL` to your PythonAnywhere API URL |
| CORS            | Backend .env | Add your Vercel URL to `CORS_ALLOWED_ORIGINS` |

After this, your website will run with:
- **Frontend:** `https://your-app.vercel.app`
- **API / Admin:** `https://YOUR_USERNAME.pythonanywhere.com/api/` and `https://YOUR_USERNAME.pythonanywhere.com/admin/`
