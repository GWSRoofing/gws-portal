"""
gws_auth.py — drop this file into each app repo alongside app.py

Usage at the top of each app.py:
    from gws_auth import check_portal_auth
    check_portal_auth()  # Call this before any other st.* calls

If the user arrived via the portal with a valid token, they pass straight through.
If they try to access the app directly without a token, they are redirected to the portal.
"""

import streamlit as st
import os
import hmac
import hashlib
import base64

PORTAL_URL = os.environ.get("PORTAL_URL", "https://gws-portal.up.railway.app/")
AUTH_TOKEN_SECRET = os.environ.get("AUTH_TOKEN_SECRET", "gws-secret-key-change-me")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "gws2024")


def _generate_token(password: str) -> str:
    h = hmac.new(AUTH_TOKEN_SECRET.encode(), password.encode(), hashlib.sha256)
    return base64.urlsafe_b64encode(h.digest()).decode()


def _verify_token(token: str) -> bool:
    expected = _generate_token(APP_PASSWORD)
    return hmac.compare_digest(token, expected)


def check_portal_auth():
    """
    Call at the top of each app's app.py (before any other st.* output).
    - If already authenticated in session: pass through.
    - If valid token in URL query params: store in session and pass through.
    - Otherwise: show redirect message pointing to the portal.
    """
    # Already authenticated this session
    if st.session_state.get("authenticated", False):
        return

    # Check for token in URL query params (passed by portal when linking)
    params = st.query_params
    token = params.get("auth_token", "")

    if token and _verify_token(token):
        st.session_state.authenticated = True
        # Clear token from URL bar for cleanliness
        st.query_params.clear()
        return

    # Not authenticated — show redirect page
    st.markdown("""
    <style>
    #MainMenu, footer, header { display: none !important; }
    .redirect-box {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; min-height: 100vh;
        font-family: sans-serif; background: #0e1a2b; color: white;
        text-align: center; padding: 40px;
    }
    .redirect-box h2 { font-size: 22px; margin-bottom: 12px; }
    .redirect-box p { color: rgba(255,255,255,0.5); margin-bottom: 32px; font-size: 15px; }
    .redirect-btn {
        background: #c8f03c; color: #0e1a2b; border: none;
        padding: 14px 36px; border-radius: 10px; font-size: 16px;
        font-weight: 700; cursor: pointer; text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="redirect-box">
        <h2>🔒 Access via GWS Portal</h2>
        <p>Please log in through the GWS Portal to access this application.</p>
        <a href="{PORTAL_URL}" class="redirect-btn">Go to GWS Portal →</a>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
