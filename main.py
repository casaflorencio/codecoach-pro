from pathlib import Path
import streamlit as st
import os
from dotenv import load_dotenv
from fpdf import FPDF
import base64
import openai

# === Load API key ===
if Path(".env").exists():
    load_dotenv()
else:
    st.warning("⚠️ .env file is missing. Please create one and add your 'OPENAI_API_KEY'.")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except KeyError:
        api_key = st.text_input("🔐 Enter your OpenAI API Key", type="password")
        if not api_key:
            st.error("❌ OPENAI_API_KEY not provided.")
            st.stop()

# === OpenAI Client ===
client = openai.OpenAI(api_key=api_key)

# === Page Config ===
st.set_page_config(page_title="CodeCoach AI", layout="wide")

# === Styling ===
st.markdown("""
    <style>
    html, body, .stApp {
        height: 100vh;
        margin: 0;
        padding: 0;
        overflow: auto;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.3);
        z-index: -1;
    }
    .content-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 1rem;
        margin: 2rem auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    textarea {
        resize: vertical !important;
        min-height: 150px !important;
        max-height: 500px !important;
    }
    </style>
""", unsafe_allow_html=True)

# === Optional Background Image ===
def set_bg_from_local(png_file):
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

if Path("bg.png").exists():
    set_bg_from_local("bg.png")

# === Logo ===
logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
with logo_col2:
    if Path("logo.png").exists():
        st.image("logo.png", width=160)

# === Title Section ===
with st.container():
    st.markdown("""
        <div class='content-card' style='text-align:center;'>
            <h1 style='color:#1a73e8;'>Welcome to <span style='color:green;'>CodeCoach AI</span></h1>
            <p>Analyze, Learn, Fix, and Export Python Code Smarter & Faster.</p>
        </div>
    """, unsafe_allow_html=True)

# === Session State ===
for key in ["feedback", "lesson", "fixed_code", "fix_explained", "coaching", "unit_test"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# === Input ===
with st.container():
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    auto_mode = st.toggle("🔁 Auto-Coach Mode")
    code_input = st.text_area("🧑‍💻 Paste Your Python Code", height=250)
    st.markdown("</div>", unsafe_allow_html=True)

# === Sidebar ===
st.sidebar.header("📊 Live Code Stats")
st.sidebar.metric("📏 Lines", len(code_input.strip().splitlines()))
st.sidebar.metric("🔤 Words", len(code_input.strip().split()))

# === Export ===
def export_pdf(title, content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)
    with open(filename, "rb") as f:
        st.sidebar.download_button(title, f, file_name=filename, mime="application/pdf")

st.sidebar.subheader("📤 Export")
if st.sidebar.button("📄 Export Fix PDF"):
    if st.session_state.fixed_code:
        content = f"Original Code:\n{code_input}\n\nFixed Code:\n{st.session_state.fixed_code}\n\nExplanation:\n{st.session_state.fix_explained}"
        export_pdf("📥 Download Fix PDF", content, "CodeCoach_Fix.pdf")
    else:
        st.sidebar.warning("❗ Generate fix first.")

if st.sidebar.button("📄 Export Full Report"):
    content = (
        f"Code Feedback:\n{st.session_state.feedback}\n\n"
        f"Lesson:\n{st.session_state.lesson}\n\n"
        f"Fixed Code:\n{st.session_state.fixed_code}\n\n"
        f"Fix Explanation:\n{st.session_state.fix_explained}"
    )
    export_pdf("📥 Download Full Report", content, "CodeCoach_Full_Report.pdf")

# === GPT Call ===
def ask_openai(system_msg, user_msg):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

# === Auto Mode ===
if auto_mode and code_input:
    if not st.session_state.feedback:
        st.session_state.feedback = ask_openai("You are a Python tutor. Analyze and summarize this code.", code_input)
    if not st.session_state.lesson:
        st.session_state.lesson = ask_openai("Explain the programming concepts in this code for a beginner.", code_input)

# === Tabs ===
with st.container():
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    tabs = st.tabs(["🧠 Analyze", "💬 Teach Me", "🛠 Fix", "👨‍🏫 Coach Me", "🧪 Unit Test"])

    with tabs[0]:
        if st.button("🧠 Analyze Code"):
            st.session_state.feedback = ask_openai("You are a Python tutor. Analyze and summarize this code.", code_input)
        if st.button("🔄 Clear Results (Analyze)"):
            st.session_state.feedback = ""

    with tabs[1]:
        if st.button("💬 Teach Me This"):
            st.session_state.lesson = ask_openai("Explain the programming concepts in this code for a beginner.", code_input)
        if st.button("🔄 Clear Results (Teach)"):
            st.session_state.lesson = ""

    with tabs[2]:
        if st.button("🛠 Fix My Code"):
            response = ask_openai("You are a Python expert. Fix and improve this code, then explain.", code_input)
            parts = response.split("```")
            fixed_code = ""
            for i in range(1, len(parts)):
                if parts[i].strip().startswith("python"):
                    fixed_code = parts[i].strip()[6:].strip()
                    break
                elif parts[i].strip():
                    fixed_code = parts[i].strip()
                    break
            st.session_state.fixed_code = fixed_code if fixed_code else response.strip()
            st.session_state.fix_explained = parts[i+1].strip() if (i+1) < len(parts) else ""
        if st.button("🔄 Clear Results (Fix)"):
            st.session_state.fixed_code = ""
            st.session_state.fix_explained = ""

    with tabs[3]:
        if st.button("👨‍🏫 Coach Me"):
            st.session_state.coaching = ask_openai("Explain the code line-by-line in beginner-friendly terms.", code_input)
            st.markdown("### 👨‍🏫 Line-by-Line Coaching")
            st.write(st.session_state.coaching)
        if st.button("🔄 Clear Results (Coach)"):
            st.session_state.coaching = ""

    with tabs[4]:
        framework = st.selectbox("Choose test framework:", ["unittest", "pytest", "doctest"])
        if st.button("🧪 Generate Unit Test"):
            prompt = f"Write a {framework} test for this Python code."
            st.session_state.unit_test = ask_openai(prompt, code_input)
            st.markdown("### ✅ Unit Test")
            st.code(st.session_state.unit_test, language="python")
        if st.button("🔄 Clear Results (Test)"):
            st.session_state.unit_test = ""
    st.markdown("</div>", unsafe_allow_html=True)

# === Output Section ===
with st.container():
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    if st.session_state.feedback:
        st.markdown("### 🧾 CodeCoach Feedback")
        st.write(st.session_state.feedback)
    if st.session_state.lesson:
        st.markdown("### 📘 Lesson")
        st.write(st.session_state.lesson)
    if st.session_state.fixed_code:
        st.markdown("### 🔧 AI Fixed Code")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Original Code:**")
            st.code(code_input, language="python")
        with col2:
            st.markdown("**Fixed Code:**")
            st.code(st.session_state.fixed_code, language="python")
        st.markdown("**🧠 Explanation:**")
        st.write(st.session_state.fix_explained)
    st.markdown("</div>", unsafe_allow_html=True)