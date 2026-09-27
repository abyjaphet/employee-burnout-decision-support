from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "styles.css"
LOGO_PATH = ROOT / "assets" / "logo.png"


def load_css() -> None:
    if CSS_PATH.exists():
        st.markdown(
            f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def show_sidebar() -> None:
    if LOGO_PATH.exists():
        st.sidebar.image(str(LOGO_PATH), width=140)
    st.sidebar.markdown("### Burnout DSS")
    st.sidebar.caption(
        "Predict risk, explain drivers, and support organisational decisions."
    )
