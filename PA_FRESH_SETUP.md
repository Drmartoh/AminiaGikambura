# PythonAnywhere – Fresh setup after cloning from GitHub

Do this **on PythonAnywhere** after you have cloned the repo. Replace:

- **YOUR_USERNAME** → your PythonAnywhere username (e.g. `aminiagikambura`)
- **REPO_FOLDER** → the folder you cloned into (e.g. `AminiaGikambura` or `CBO`)

Your project path will be: `/home/YOUR_USERNAME/REPO_FOLDER` and the Django app is in `/home/YOUR_USERNAME/REPO_FOLDER/backend`.

---

## Step 1: Open Bash and go to the project

1. In PythonAnywhere, open the **Consoles** tab.
2. Click **Bash** to open a new console.
3. Go to your project (use the folder name you used when cloning):

```bash
cd ~/REPO_FOLDER
```

Example: `cd ~/AminiaGikambura` or `cd ~/CBO`.

---

## Step 2: Create virtualenv with Python 3.10

Use **Python 3.10** (Pillow often fails on 3.13).

```bash
cd ~/REPO_FOLDER/backend
rm -rf venv
python3.10 -m venv venv
```

If `python3.10` is not found, try:

```bash
python3.9 -m venv venv
```

---

## Step 3: Activate venv and install dependencies

```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Wait until it finishes. You should see `(venv)` in the prompt.

---

## Step 4: Create the `.env` file

```bash
cd ~/REPO_FOLDER/backend
nano .env
```

Paste this (replace values as needed):

```env
SECRET_KEY=put-a-long-random-string-here
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
DB_ENGINE=sqlite
```

**Generate a secret key** (run in another Bash line, then copy the output into `.env` as `SECRET_KEY`):

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

In nano: **Ctrl+O**, Enter, **Ctrl+X** to save and exit.

---

## Step 5: Run migrations and collect static files

```bash
cd ~/REPO_FOLDER/backend
source venv/bin/activate
python manage.py migrate
python manage.py seed_kiambu_wards
python manage.py collectstatic --noinput
```

**(Optional)** Create a superuser for the manage area and Django admin:

```bash
python manage.py createsuperuser
```

---

## Step 6: Create the Web app (if you haven’t already)

1. Go to the **Web** tab.
2. Click **Add a new web app**.
3. Choose **Manual configuration**.
4. Select **Python 3.10** (match your venv).
5. Click **Next** until the app is created.

---

## Step 7: Set Code and Virtualenv

On the **Web** tab, under **Code**:

- **Source code:** `/home/YOUR_USERNAME/REPO_FOLDER`
- **Working directory:** `/home/YOUR_USERNAME/REPO_FOLDER/backend`

Under **Virtualenv**, click “Enter path to a virtualenv” and set:

```
/home/YOUR_USERNAME/REPO_FOLDER/backend/venv
```

Use the green check to save.

---

## Step 8: Edit the WSGI file

Under **WSGI configuration file**, click the link.

**Replace the entire file** with (use your actual username and repo folder):

```python
import os
import sys

path = '/home/YOUR_USERNAME/REPO_FOLDER/backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'agcbo.settings'

# Load .env from backend folder
from pathlib import Path
env_path = Path('/home/YOUR_USERNAME/REPO_FOLDER/backend') / '.env'
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

Replace **YOUR_USERNAME** and **REPO_FOLDER** in both paths. Save (Ctrl+S).

---

## Step 9: Add static and media mappings

On the **Web** tab, scroll to **Static files**. Add:

| URL          | Directory                                              |
|-------------|---------------------------------------------------------|
| `/static/`  | `/home/YOUR_USERNAME/REPO_FOLDER/backend/staticfiles`  |
| `/media/`   | `/home/YOUR_USERNAME/REPO_FOLDER/backend/media`        |

Save if there is a check button.

---

## Step 10: Reload and test

1. On the **Web** tab, click the green **Reload** button.
2. Open **https://YOUR_USERNAME.pythonanywhere.com/**

You should see the site. Try:

- `/` – Home  
- `/about/` – About  
- `/login/` – Login  
- `/manage/` – Manage (admin; requires superuser or admin user)  
- `/admin/` – Django admin  

---

## If something goes wrong

- **500 error:** Open **Web** → **Error log** and read the last lines.
- **“DisallowedHost”:** In `.env`, set `ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com` (no `https://`, no slash).
- **Static/CSS not loading:** Confirm the two static file URLs and paths, and that you ran `collectstatic`.
- **“No module named …”:** Ensure the virtualenv path is correct and you ran `pip install -r requirements.txt` inside that venv.
