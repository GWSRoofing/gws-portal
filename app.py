import streamlit as st
import os
import hmac
import hashlib
import base64
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GWS Portal",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Config ────────────────────────────────────────────────────────────────────
APP_PASSWORD = os.environ.get("APP_PASSWORD", "gws2024")
AUTH_TOKEN_SECRET = os.environ.get("AUTH_TOKEN_SECRET", "gws-secret-key-change-me")

APPS = [
    {
        "title": "✉️  Cover Letter",
        "description": "Generate professional cover letters from dictated job details",
        "url": "https://coverletter-production.up.railway.app/",
    },
    {
        "title": "📋  Quote",
        "description": "Create accurate roofing quotes from voice or typed input",
        "url": "https://quote-production-a674.up.railway.app/",
    },
    {
        "title": "🔧  Live Job Sheet",
        "description": "Produce live job sheets ready for site and client sign-off",
        "url": "https://livejobsheet-production.up.railway.app/",
    },
]

# ── Auth helpers ───────────────────────────────────────────────────────────────
def generate_token(password: str) -> str:
    h = hmac.new(AUTH_TOKEN_SECRET.encode(), password.encode(), hashlib.sha256)
    return base64.urlsafe_b64encode(h.digest()).decode()

def check_auth() -> bool:
    return st.session_state.get("authenticated", False)

# ── Logo ──────────────────────────────────────────────────────────────────────
def get_logo_b64():
    logo_path = Path(__file__).parent / "GWS_Roofing_Logo_Reversed.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def show_logo():
    logo_b64 = get_logo_b64()
    if logo_b64:
        st.markdown(
            f'<div style="text-align:center;margin-bottom:4px;padding-top:20px;">'
            f'<img src="data:image/png;base64,{logo_b64}" style="height:90px;width:auto;" />'
            f'</div>',
            unsafe_allow_html=True
        )

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;600;700;800&display=swap');

#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

html, body, .stApp {
    font-family: 'Barlow', sans-serif !important;
    background: #0e1a2b !important;
}

[data-testid="stAppViewContainer"] {
    background: #0e1a2b !important;
}

.block-container {
    padding-top: 20px !important;
    padding-bottom: 60px !important;
    max-width: 700px !important;
}

h1, h2, h3 {
    color: #ffffff !important;
    font-family: 'Barlow', sans-serif !important;
    text-align: center;
}

p, label {
    color: rgba(255,255,255,0.6) !important;
    font-family: 'Barlow', sans-serif !important;
    text-align: center;
}

/* Password input — dark background, white text, visible when revealed */
.stTextInput > div > div > input {
    background: #1e2f45 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stTextInput > div > div > input:focus {
    border-color: #c8f03c !important;
    box-shadow: 0 0 0 2px rgba(200,240,60,0.2) !important;
}

/* Eye icon colour */
.stTextInput > div > div > button {
    color: rgba(255,255,255,0.6) !important;
}

.stButton > button {
    background: #c8f03c !important;
    color: #0e1a2b !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Barlow', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 32px !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #d4f54a !important;
}
</style>
""", unsafe_allow_html=True)

# ── Shared header (logo + portal tag) ─────────────────────────────────────────
show_logo()
st.markdown(
    '<p style="color:#c8f03c !important;font-size:12px;letter-spacing:3px;'
    'text-transform:uppercase;text-align:center;margin-bottom:24px;">GWS Portal</p>',
    unsafe_allow_html=True
)

# ── Login screen ───────────────────────────────────────────────────────────────
if not check_auth():
    st.markdown("### Welcome back")
    st.markdown("Enter your access code to continue")
    st.markdown("<br>", unsafe_allow_html=True)

    password = st.text_input(
        "Access code",
        type="password",
        placeholder="Enter access code",
        label_visibility="collapsed"
    )

    if st.button("Enter Portal"):
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.auth_token = generate_token(password)
            st.rerun()
        else:
            st.error("Incorrect access code. Please try again.")

    st.stop()

# ── Authenticated — hub ────────────────────────────────────────────────────────
token = st.session_state.get("auth_token", "")

st.markdown("### Select an application")
st.markdown("<br>", unsafe_allow_html=True)

for app in APPS:
    url_with_token = f"{app['url']}?auth_token={token}"
    st.markdown(
        f'<a href="{url_with_token}" target="_blank" style="text-decoration:none;">'
        f'<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);'
        f'border-radius:12px;padding:24px 28px;margin-bottom:16px;cursor:pointer;" '
        f'onmouseover="this.style.borderColor=\'#c8f03c\';this.style.background=\'rgba(200,240,60,0.08)\'" '
        f'onmouseout="this.style.borderColor=\'rgba(255,255,255,0.1)\';this.style.background=\'rgba(255,255,255,0.05)\'">'
        f'<div style="color:#ffffff;font-size:18px;font-weight:700;margin-bottom:6px;">{app["title"]}</div>'
        f'<div style="color:rgba(255,255,255,0.45);font-size:13px;text-align:left;">{app["description"]}</div>'
        f'</div></a>',
        unsafe_allow_html=True
    )
