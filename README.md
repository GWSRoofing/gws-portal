# GWS Portal

Central hub and authentication gateway for all GWS Roofing document apps.

## Files in this repo

| File | Purpose |
|------|---------|
| `app.py` | The portal landing page & login |
| `gws_auth.py` | Auth helper — copy into each individual app repo |
| `GWS_Roofing_Logo.jpg` | Logo shown on the portal |
| `requirements.txt` | Python dependencies |

---

## Deploying the Portal on Railway

1. Create a new GitHub repo: `GWSRoofing/gws-portal`
2. Upload all files in this folder to that repo
3. In Railway: **New Project → Deploy from GitHub repo** → select `GWSRoofing/gws-portal`
4. Add these environment variables in Railway → Variables:

| Variable | Value |
|----------|-------|
| `APP_PASSWORD` | Your chosen staff password (e.g. `GWSRoofing2024`) |
| `AUTH_TOKEN_SECRET` | A long random string (e.g. `gws-xk92-secret-mq47-token`) |

5. Add start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Generate a domain in Railway → Settings → Networking
7. Note your portal URL (e.g. `https://gws-portal.up.railway.app`)

---

## Securing each individual app

For each existing app (coverletter, quote, livejobsheet):

### Step 1 — Add gws_auth.py to the repo
Copy `gws_auth.py` into the root of each app's GitHub repo alongside `app.py`.

### Step 2 — Add two lines to each app.py
At the very top of each `app.py`, after the imports, add:
```python
from gws_auth import check_portal_auth
check_portal_auth()
```

### Step 3 — Add environment variables in Railway
For each app's Railway service, add:

| Variable | Value |
|----------|-------|
| `APP_PASSWORD` | **Same value** as the portal's APP_PASSWORD |
| `AUTH_TOKEN_SECRET` | **Same value** as the portal's AUTH_TOKEN_SECRET |
| `PORTAL_URL` | Your portal's Railway URL |

All three values must match exactly across all services — this is what makes the single login work.

---

## How the auth flow works

1. Staff go to the portal URL and enter the access code
2. Portal generates a signed token and appends it to each app link as `?auth_token=...`
3. When staff click an app, the app checks the token, verifies it matches, and lets them in
4. If anyone tries to go directly to an app URL without a valid token, they see a redirect page pointing back to the portal
