# Media files (logos, images, videos) – how they work

## How it works

1. **Upload:** Files are saved to `backend/media/` (e.g. `media/site/`, `media/sections/`) using `get_storage()` (filesystem when Cloudinary is not configured).

2. **URLs:** Templates use `{{ obj.logo.url|absolute_media:request }}` (or similar) so the browser gets a full URL like `https://yoursite.com/media/site/logo.jpg`.

3. **Serving:** The URL pattern `path('media/<path:path>', serve_media)` in `agcbo/urls.py` serves every `/media/...` request from `MEDIA_ROOT` via `agcbo/media_views.serve_media`.

## PythonAnywhere – critical

**Remove the Static files mapping for `/media/`** so that `/media/` requests reach Django instead of the web server.

- In the **Web** tab → **Static files**, if there is a row with **URL** `/media/`, **delete that row**.
- If you keep a mapping for `/media/`, the server will serve from that directory and often return 404 (wrong or empty path). Django’s media view will never run.
- After removing it, click **Reload** for your web app.

## After deploy

1. Open **Manage → Settings** and re-upload the **logo** (and favicon if you use it). That writes the file under `backend/media/site/`.
2. Hard-refresh the site (Ctrl+F5).
3. If something still 404s, check that the file exists on the server at `backend/media/...` (e.g. in a Bash console: `ls -la backend/media/site/`).
