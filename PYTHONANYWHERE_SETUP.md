# PythonAnywhere setup – run the app after cloning

Do this **on PythonAnywhere** (in the Bash console and Web tab). Replace **YOUR_USERNAME** with your PythonAnywhere username everywhere.

---

## Step 1: Virtual environment and dependencies

**You must use Python 3.10 (not 3.13).** The error “Getting requirements to build wheel … error” / `KeyError: '__version__'` happens because Pillow does not build on Python 3.13. Create the venv **in Bash** with **python3.10** (do not use the Web tab’s “Create virtualenv” if it would use 3.13).

Open a **Bash** console (Consoles → Bash). Run these commands **one by one**:

**1) See which Python 3.10 is available:**
```bash
which python3.10
```
If you see a path (e.g. `/usr/bin/python3.10`), use it in the next step. If “not found”, try:
```bash
which python3.9
```

**2) Go to the project and remove any old venv:**
```bash
cd ~/CBO/backend
rm -rf venv
```

**3) Create a new venv with Python 3.10 (or 3.9 if 3.10 is not installed):**
```bash
python3.10 -m venv venv
```
If that says “command not found”, use:
```bash
python3.9 -m venv venv
```

**4) Activate and install (you must see `(venv)` in the prompt):**
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Check the version in the venv:
```bash
python --version
```
It should show **Python 3.10.x** or **3.9.x**, not 3.13.

**5) In the Web tab**, set the virtualenv path to:
`/home/YOUR_USERNAME/CBO/backend/venv`
(use your PythonAnywhere username). Do **not** create a new virtualenv from the Web tab; use this one you created in Bash.

Wait until `pip install -r requirements.txt` finishes without errors.

---

## Step 2: Create `.env` file

Still in the Bash console:

```bash
cd ~/CBO/backend
nano .env
```

Paste this (change the values as needed):

```
SECRET_KEY=change-this-to-a-long-random-string
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
DB_ENGINE=sqlite
```

To generate a secret key, in another Bash line run:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```
Copy the output and use it as `SECRET_KEY` in `.env`.

Save in nano: **Ctrl+O**, Enter, then **Ctrl+X** to exit.

---

## Step 3: Migrate, seed Kiambu data, and collect static files

```bash
cd ~/CBO/backend
source venv/bin/activate
python manage.py migrate
python manage.py seed_kiambu_wards
python manage.py collectstatic --noinput
```

(Optional) Create an admin user:
```bash
python manage.py createsuperuser
```

---

## Step 4: Create the Web app

1. Go to the **Web** tab in the PythonAnywhere dashboard.
2. Click **Add a new web app**.
3. Choose **Manual configuration** (not “Django”).
4. Select **Python 3.10** (must match the venv from Step 1; do not use 3.13 – Pillow can fail to build).
5. Click **Next** until the web app is created.

---

## Step 5: Set source code and working directory

On the **Web** tab, under **Code**:

- **Source code:** `/home/YOUR_USERNAME/CBO`
- **Working directory:** `/home/YOUR_USERNAME/CBO/backend`

Click the green check to save if needed.

---

## Step 6: Set virtualenv

Under **Virtualenv**, click the text that says “Enter path to a virtualenv, if desired”.

Enter:

```
/home/YOUR_USERNAME/CBO/backend/venv
```

Click the green check.

---

## Step 7: Edit the WSGI file

Under **WSGI configuration file**, click the link (e.g. `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`).

**Delete everything** in that file and replace with:

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

Replace **YOUR_USERNAME** with your PythonAnywhere username (in both `/home/YOUR_USERNAME/...` paths).

Save the file (Ctrl+S in the editor).

---

## Step 8: Add static and media files

On the **Web** tab, scroll to **Static files**.

Add two mappings:

| URL         | Directory                                  |
|------------|---------------------------------------------|
| `/static/` | `/home/YOUR_USERNAME/CBO/backend/staticfiles` |
| `/media/`  | `/home/YOUR_USERNAME/CBO/backend/media`       |

Use **YOUR_USERNAME** in the paths. Save if there’s a check button.

---

## Step 9: Reload the web app

On the **Web** tab, click the green **Reload** button for your web app.

---

## Step 10: Open your site

Visit: **https://YOUR_USERNAME.pythonanywhere.com/**

You should see the AGCBO home page. Try:

- `/about/` – About
- `/projects/` – Projects
- `/contact/` – Contact
- `/admin/` – Admin (if you ran `createsuperuser`)

---

## If something goes wrong

- **500 error:** On the **Web** tab, open **Error log** and read the last lines for the traceback.
- **Static files (CSS) not loading:** Check that the `/static/` URL and path are correct and that you ran `collectstatic`.
- **“Module not found” or “No module named …”:** Make sure the virtualenv path is correct and you ran `pip install -r requirements.txt` inside that venv.
- **“DisallowedHost”:** In `.env`, `ALLOWED_HOSTS` must be exactly `YOUR_USERNAME.pythonanywhere.com` (no `https://`, no trailing slash).
