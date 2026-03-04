import streamlit as st
import os
from streamlit.components.v1 import html

# ----------------------------
# Paths
# ----------------------------
FRONTEND_DIR = os.path.join(os.path.dirname(__file__))
INDEX_HTML = os.path.join(FRONTEND_DIR, 'index.html')
CSS_FILE = os.path.join(FRONTEND_DIR, 'styles', 'custom.css')

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Gamified Performance Feedback Agent",
    page_icon="🎮",
    layout="wide"
)

# ----------------------------
# Load custom CSS
# ----------------------------
if os.path.exists(CSS_FILE):
    with open(CSS_FILE) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------------------------
# Load HTML Dashboard
# ----------------------------
if os.path.exists(INDEX_HTML):
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html_content = f.read()
        html(html_content, height=1200, scrolling=True)
else:
    st.warning("index.html not found in frontend folder. Please add your HTML dashboard here.")