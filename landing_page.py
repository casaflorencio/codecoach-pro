import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="CodeCoach AI | Home", page_icon="🧠", layout="wide")

# === Background Loader ===
def set_background(png_file):
    with open(png_file, "rb") as f:
        img_bytes = f.read()
    b64_img = base64.b64encode(img_bytes).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_img}");
            background-size: cover;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

if Path("assets/bg.png").exists():
    set_background("assets/bg.png")

# === Global Styles ===
st.markdown("""
    <style>
    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #f5f7fa;
        color: #222;
    }
    .hero {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 3rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 4rem;
    }
    .cta-btn {
        background-color: #1a73e8;
        color: white;
        padding: 0.75rem 1.5rem;
        font-size: 1.2rem;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        margin-top: 2rem;
        transition: background-color 0.3s ease;
    }
    .cta-btn:hover {
        background-color: #0f5bcc;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
        margin: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Logo ===
logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
with logo_col2:
    if Path("assets/logo.png").exists():
        st.image("assets/logo.png", width=140)
    else:
        st.markdown("### 🧠 CodeCoach AI", unsafe_allow_html=True)

# === Hero Section ===
st.markdown("<div class='hero'>", unsafe_allow_html=True)
st.markdown("## Your Personal Coding Coach")
st.markdown("Master Python smarter — with AI that teaches, fixes, and tests your code.")

if st.button("🚀 Get Started", use_container_width=True):
    st.switch_page("codecoach_paywall.py")  # Or "codecoach_dashboard.py" if skipping paywall

st.markdown("</div>", unsafe_allow_html=True)

# === Feature Highlights ===
st.markdown("### 💡 What You Can Do")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("🧠 **Analyze**\n\nGet feedback on what your code does and how to improve it.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("💬 **Teach Me**\n\nLearn concepts behind your code in plain English.")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("🛠 **Fix & Explain**\n\nLet AI rewrite broken code and explain the changes.")
    st.markdown("</div>", unsafe_allow_html=True)

# === Footer ===
st.markdown("---")
st.markdown("Made with ❤️ by FlowSoundz | Powered by OpenAI & Streamlit")
