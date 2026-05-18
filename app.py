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
        "title": "Cover Letter",
        "description": "Generate professional cover letters from dictated job details",
        "url": "https://coverletter-production.up.railway.app/",
        "icon": "✉️",
        "color": "#c8f03c"
    },
    {
        "title": "Quote Generator",
        "description": "Create accurate roofing quotes from voice or typed input",
        "url": "https://quote-production-a674.up.railway.app/",
        "icon": "📋",
        "color": "#c8f03c"
    },
    {
        "title": "Live Job Sheet",
        "description": "Produce live job sheets ready for site and client sign-off",
        "url": "https://livejobsheet-production.up.railway.app/",
        "icon": "🔧",
        "color": "#c8f03c"
    },
]

# ── Auth helpers ───────────────────────────────────────────────────────────────
def generate_token(password: str) -> str:
    """Generate a signed token from the password."""
    h = hmac.new(AUTH_TOKEN_SECRET.encode(), password.encode(), hashlib.sha256)
    return base64.urlsafe_b64encode(h.digest()).decode()

def verify_token(token: str) -> bool:
    """Verify a token is valid."""
    expected = generate_token(APP_PASSWORD)
    return hmac.compare_digest(token, expected)

def check_auth() -> bool:
    """Check if user is authenticated via session state."""
    return st.session_state.get("authenticated", False)

# ── Logo ──────────────────────────────────────────────────────────────────────
def get_logo_b64():
    logo_path = Path(__file__).parent / "GWS_Roofing_Logo.jpg"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;600;700;800&family=Barlow+Condensed:wght@700;800&display=swap');

/* Hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stApp > header { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Root */
html, body, .stApp {
    margin: 0; padding: 0;
    font-family: 'Barlow', sans-serif;
    background: #0e1a2b;
    min-height: 100vh;
}

[data-testid="stAppViewContainer"] {
    background: #0e1a2b;
    min-height: 100vh;
}

[data-testid="stMain"] {
    background: transparent;
    padding: 0 !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Portal wrapper */
.portal-wrapper {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(200,240,60,0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(14,26,43,0.9) 0%, transparent 50%),
        #0e1a2b;
}

/* Header */
.portal-header {
    text-align: center;
    margin-bottom: 48px;
}

.portal-logo {
    height: 80px;
    margin-bottom: 16px;
    filter: drop-shadow(0 4px 24px rgba(200,240,60,0.2));
}

.portal-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #c8f03c;
    margin: 0;
}

/* Login box */
.login-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 40px;
    width: 100%;
    max-width: 400px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.login-title {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 8px 0;
}

.login-subtitle {
    font-size: 14px;
    color: rgba(255,255,255,0.45);
    margin: 0 0 32px 0;
}

/* App grid */
.apps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
    width: 100%;
    max-width: 900px;
    margin-top: 0;
}

.app-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 32px 28px;
    text-decoration: none;
    display: block;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.app-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: #c8f03c;
    transform: scaleX(0);
    transition: transform 0.25s ease;
}

.app-card:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(200,240,60,0.3);
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.4);
    text-decoration: none;
}

.app-card:hover::before {
    transform: scaleX(1);
}

.app-icon {
    font-size: 32px;
    margin-bottom: 16px;
    display: block;
}

.app-name {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 8px 0;
}

.app-desc {
    font-size: 13px;
    color: rgba(255,255,255,0.45);
    line-height: 1.5;
    margin: 0;
}

.app-arrow {
    position: absolute;
    bottom: 24px;
    right: 24px;
    color: #c8f03c;
    font-size: 18px;
    opacity: 0;
    transition: opacity 0.25s ease, transform 0.25s ease;
}

.app-card:hover .app-arrow {
    opacity: 1;
    transform: translateX(4px);
}

/* Welcome bar */
.welcome-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    max-width: 900px;
    margin-bottom: 24px;
    padding: 0 4px;
}

.welcome-text {
    font-size: 13px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.5px;
}

/* Streamlit input overrides */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #c8f03c !important;
    box-shadow: 0 0 0 2px rgba(200,240,60,0.15) !important;
}

.stTextInput label {
    color: rgba(255,255,255,0.6) !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
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
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
    margin-top: 8px !important;
}

.stButton > button:hover {
    background: #d4f54a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(200,240,60,0.3) !important;
}

.stAlert {
    border-radius: 10px !important;
}

div[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Logo base64 ────────────────────────────────────────────────────────────────
logo_b64 = get_logo_b64()
logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" class="portal-logo" />' if logo_b64 else ""

# ── Login screen ───────────────────────────────────────────────────────────────
if not check_auth():
    st.markdown(f"""
    <div class="portal-wrapper">
        <div class="portal-header">
            {logo_html}
            <p class="portal-title">GWS Portal</p>
        </div>
        <div class="login-box">
            <p class="login-title">Welcome back</p>
            <p class="login-subtitle">Enter your access code to continue</p>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        password = st.text_input("Access code", type="password", label_visibility="collapsed", placeholder="Enter access code")
        submitted = st.form_submit_button("Enter Portal")
        if submitted:
            if password == APP_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.auth_token = generate_token(password)
                st.rerun()
            else:
                st.error("Incorrect access code. Please try again.")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# ── Authenticated — hub screen ─────────────────────────────────────────────────
token = st.session_state.get("auth_token", "")

apps_html = ""
for app in APPS:
    # Append token to URL so individual apps can verify
    url_with_token = f"{app['url']}?auth_token={token}"
    apps_html += f"""
    <a href="{url_with_token}" target="_blank" class="app-card">
        <span class="app-icon">{app['icon']}</span>
        <p class="app-name">{app['title']}</p>
        <p class="app-desc">{app['description']}</p>
        <span class="app-arrow">→</span>
    </a>
    """

st.markdown(f"""
<div class="portal-wrapper">
    <div class="portal-header">
        {logo_html}
        <p class="portal-title">GWS Portal</p>
    </div>
    <div class="welcome-bar">
        <span class="welcome-text">SELECT AN APPLICATION TO CONTINUE</span>
    </div>
    <div class="apps-grid">
        {apps_html}
    </div>
</div>
""", unsafe_allow_html=True)
