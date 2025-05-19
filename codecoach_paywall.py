
import streamlit as st
import base64
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="CodeCoach AI | Pro Access", layout="wide", initial_sidebar_state="collapsed")

# === Background Image Injection ===
def set_background(png_file):
    with open(png_file, "rb") as f:
        img_bytes = f.read()
    b64_img = base64.b64encode(img_bytes).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_img}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

if Path("paywall_bg.png").exists():
    set_background("paywall_bg.png")

# === Safe Logo Load ===
try:
    logo = Image.open("logo.png")
    st.image(logo, width=140)
except:
    st.markdown("<!-- logo not found -->", unsafe_allow_html=True)

# === Custom CSS Styling ===
st.markdown("""
    <style>
    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        color: #222;
        height: 100%%;
        overflow-x: hidden;
    }
    .main-container {
        max-width: 720px;
        margin: auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        margin-top: 3rem;
    }
    .btn-upgrade {
        background-color: #1a73e8;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }
    .btn-upgrade:hover {
        background-color: #155ab6;
    }
    h1 {
        color: #1a73e8;
        font-size: 2.5rem;
        margin-bottom: 0.25rem;
        text-align: center;
    }
    h1 span {
        color: green;
    }
    .subtext {
        font-size: 1.1rem;
        color: #333;
        text-align: center;
        margin-bottom: 2rem;
    }
    .plan-box {
        background: #f1f4f9;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Content ===
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.markdown("""
<h1>Welcome to <span>CodeCoach AI</span></h1>
<p class="subtext">The Smart Coding Assistant for Fixes, Learning, and Testing. Upgrade to Pro to unlock advanced tools.</p>
""", unsafe_allow_html=True)

st.header("🚀 Why Go Pro?")
st.markdown("""
- ✅ Unlock advanced features like Code Similarity Check<br>
- 🧠 Save full session reports<br>
- 🛡 Priority access to updates and support<br>
- 💳 One-time or monthly options
""")

st.header("💳 Choose a Plan")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic (Free)")
    st.markdown("""
    <div class='plan-box'>
    - Fix, Teach & Coach Tools<br>
    - Export basic feedback<br>
    - Limited API calls
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("Pro Access ($9/mo)")
    st.markdown("""
    <div class='plan-box'>
    - All tools unlocked<br>
    - Session history + similarity<br>
    - Priority queue and no limits
    </div>
    """, unsafe_allow_html=True)

# === Stripe Test Mode Checkout ===
checkout_url = "https://buy.stripe.com/test_00g3eS3qYax68JOcMM"

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔓 Upgrade to Pro", key="upgrade"):
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url={checkout_url}" />
    """, unsafe_allow_html=True)

st.markdown("""
<p style='margin-top:2rem;'>Already a Pro user? <a href="/main">Go to CodeCoach AI</a></p>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
