# Why am I seeing old data on the website?

Use this checklist. The most common cause is **the server is still running old code** or your **browser is showing a cached page**.

---

## 1. Where are you viewing the site?

### A) On **PythonAnywhere** (your live site)

- **Reload the web app**  
  - Go to the **Web** tab → find your app → click the green **Reload** button.  
  - Until you reload, PythonAnywhere keeps running the **old code** in memory.

- **Confirm you pulled the latest code**  
  In a Bash console:
  ```bash
  cd ~/AminiaGikambura   # or your project path
  git status
  git pull origin main
  ```
  Then **reload the web app** again.

- **Run migrations** (if you pulled new code that has migrations)  
  ```bash
  cd backend
  workon your-venv-name
  python manage.py migrate
  ```
  Then **reload the web app**.

### B) On **your PC** (http://127.0.0.1:8000)

- **Restart the dev server**  
  Stop it (Ctrl+C) and run again:
  ```bash
  cd backend
  python manage.py runserver
  ```
  This loads the latest code.

- **Confirm you’re not on an old branch**  
  ```bash
  git status
  git branch
  ```

---

## 2. Browser cache (old HTML/CSS/JS)

Your browser may be showing an **old version** of the page.

- **Hard refresh**  
  - Windows/Linux: **Ctrl + F5** or **Ctrl + Shift + R**  
  - Mac: **Cmd + Shift + R**

- **Or try**  
  - Another browser, or  
  - Incognito/Private window, or  
  - Clear cache for this site.

---

## 3. Database is different (e.g. on PythonAnywhere)

- **Local** uses `backend/db.sqlite3` on your PC.  
- **PythonAnywhere** uses its own database (e.g. another `db.sqlite3` on the server).

So:
- Content you added **only on your PC** (e.g. Site settings, uploads) **won’t** appear on PythonAnywhere until you either:
  - Add it again in the PA admin, or  
  - Copy the DB/file store to PA (advanced).

- New **code** (templates, views, footer text, etc.) will appear on PA after **git pull** and **reload**.

---

## 4. Quick checklist (PythonAnywhere)

| Step | Action |
|------|--------|
| 1 | Bash: `cd` to project → `git pull origin main` |
| 2 | Bash: `cd backend` → `python manage.py migrate` (if you pulled new migrations) |
| 3 | Web tab: **Reload** your web app |
| 4 | Browser: **Ctrl+F5** (hard refresh) or try incognito |

After this, you should see the new site (new footer, logout redirect, etc.). If you still see old data, say whether you’re on **PythonAnywhere** or **local** and what exactly looks old (e.g. “footer text”, “menu”, “content from admin”).
