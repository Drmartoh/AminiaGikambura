# Deploying CBO Web App (Django-only) on PythonAnywhere

The app is **fully Django** (no Next.js). The website (home, about, projects, events, gallery, sports, reports, contact, login, register, dashboard) is served by Django templates. You can host everything on **PythonAnywhere** only.

This guide covers:
1. **Pushing the project to GitHub**
2. **Deploying and running the full site on PythonAnywhere**

---

## Part 1: Push to GitHub

### 1.1 Create a new repository on GitHub

1. Go to [github.com](https://github.com) and sign in.
2. Click **New repository** (e.g. name: `cbo-webapp`), set visibility, **do not** initialize with README or .gitignore.
3. Copy the repository URL (e.g. `https://github.com/YOUR_USERNAME/cbo-webapp.git`).

### 1.2 Push from your machine (project root: `CBO`)

In PowerShell or Command Prompt:

```powershell
cd C:\Users\pc\CBO
git init
git add .
git commit -m "Initial commit: CBO web app (Django-only)"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Use a **Personal Access Token** as password if Git asks for credentials.

---

## Part 2: Deploy on PythonAnywhere

### 2.1 Create account

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com) (free tier is fine).
2. Your site will be: `https://YOUR_USERNAME.pythonanywhere.com`.

### 2.2 Clone the repo

In the PythonAnywhere **Consoles** tab, open a **Bash** console:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git CBO
cd CBO
```

### 2.3 Virtualenv and dependencies

```bash
cd ~/CBO/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 Environment variables

Create a `.env` file in the **backend** folder:

```bash
cd ~/CBO/backend
nano .env
```

Add (replace with your values):

```env
SECRET_KEY=your-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
DB_ENGINE=sqlite
```

Save (Ctrl+O, Enter, Ctrl+X). Generate a secret key if needed:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 2.5 Migrate and static files

```bash
cd ~/CBO/backend
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

Create a superuser (optional, for Django admin):

```bash
python manage.py createsuperuser
```

### 2.6 Configure the Web app

1. In the PythonAnywhere dashboard go to **Web**.
2. Click **Add a new web app** → **Manual configuration** → choose **Python 3.10** (or your version).
3. Under **Code**:
   - **Source code:** `/home/YOUR_USERNAME/CBO`
   - **Working directory:** `/home/YOUR_USERNAME/CBO/backend`
4. Under **WSGI configuration file**, click the link and replace the file with:

```python
import os
import sys

path = '/home/YOUR_USERNAME/CBO/backend'
if path not in sys.path:
    sys.path.insert(0, path)

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

Replace **YOUR_USERNAME** with your PythonAnywhere username everywhere.

5. Under **Static files**, add:
   - **URL:** `/static/` → **Directory:** `/home/YOUR_USERNAME/CBO/backend/staticfiles`
   - **URL:** `/media/` → **Directory:** `/home/YOUR_USERNAME/CBO/backend/media`

6. Click **Reload** for your web app.

Your full site will be at: **https://YOUR_USERNAME.pythonanywhere.com/**  
- Home: `/`  
- About: `/about/`  
- Projects: `/projects/`  
- Events: `/events/`  
- Gallery: `/gallery/`  
- Sports: `/sports/`  
- Reports: `/reports/`  
- Contact: `/contact/`  
- Login: `/login/`  
- Register: `/register/`  
- Dashboard: `/dashboard/` (login required)  
- Admin: `/admin/`  
- API: `/api/` (optional, for programmatic access)

---

## Quick reference

| Step        | Where        | Action |
|------------|--------------|--------|
| Push code  | Your PC      | `git init`, `git add .`, `git commit`, `git remote add origin <url>`, `git push -u origin main` |
| Deploy     | PythonAnywhere| Clone repo, venv, `pip install -r backend/requirements.txt`, `.env`, migrate, collectstatic, set Web/WSGI and static/media, Reload |

No Node.js, no separate frontend host. Everything runs on PythonAnywhere.
