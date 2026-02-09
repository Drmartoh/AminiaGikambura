# Push updates to GitHub (then pull on PythonAnywhere)

Follow these steps in order.

---

## Step 1: Open terminal in your project

- In Cursor/VS Code: **Terminal → New Terminal** (or `` Ctrl+` ``).
- Make sure you're in the project root: `c:\Users\pc\CBO`

---

## Step 2: Stage all changes

```powershell
cd c:\Users\pc\CBO
git add .
```

This stages modified and new files. The `.gitignore` already excludes `backend/media/`, `db.sqlite3`, `venv`, etc., so they won't be added.

---

## Step 3: Check what will be committed (optional)

```powershell
git status
```

You should see a list of files “to be committed”. If `backend/media/` appears, run:

```powershell
git reset backend/media/
```

Then add `backend/media/` to `.gitignore` if it’s not there.

---

## Step 4: Commit with a message

```powershell
git commit -m "Security and UX: admin/manage panel, donor & county official registration, logout redirect, footer address, responsive manage sidebar"
```

Use any message you like; the one above is a suggestion.

---

## Step 5: Push to GitHub

```powershell
git push origin main
```

- If your branch is named `master` instead of `main`, use: `git push origin master`
- If GitHub asks for login, use a **Personal Access Token** as the password (not your GitHub account password). Create one at: **GitHub → Settings → Developer settings → Personal access tokens**.

---

## Step 6: On PythonAnywhere – pull the updates

1. Open a **Bash console** on PythonAnywhere.
2. Go to your project directory, for example:
   ```bash
   cd ~/AminiaGikambura
   ```
   (Use the path where your repo is.)
3. Pull from GitHub:
   ```bash
   git pull origin main
   ```
   (Use `master` if that’s your branch name.)
4. If you use a virtualenv, activate it, then reinstall if needed:
   ```bash
   workon your-venv-name
   pip install -r backend/requirements.txt
   ```
5. Run migrations if you added new ones:
   ```bash
   cd backend
   python manage.py migrate
   ```
6. Reload your web app from the **PythonAnywhere Web** tab.

---

## Quick reference

| Where        | Command / action |
|-------------|-------------------|
| **Your PC** | `git add .` → `git commit -m "message"` → `git push origin main` |
| **PythonAnywhere** | `git pull origin main` → `python manage.py migrate` (if needed) → Reload web app |

---

## If push is rejected

If you see “failed to push” or “rejected (non-fast-forward)”:

1. Someone else may have pushed, or you pushed from another machine. Pull first:
   ```powershell
   git pull origin main --rebase
   ```
2. Then push again:
   ```powershell
   git push origin main
   ```

If you use **two-factor authentication** on GitHub, you must use a **Personal Access Token** instead of your password when Git asks for credentials.
