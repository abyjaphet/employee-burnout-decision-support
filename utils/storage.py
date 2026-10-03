from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FILE = DATA_DIR / "predictions.csv"

SESSION_KEY = "predictions"


def save_prediction(record):
    """Store an assessment for the Manager Dashboard.

    1. Always appends to st.session_state so the dashboard can read it
       straight away (per-user, so visitors to the public app never see
       each other's entries).
    2. Also tries to append to data/predictions.csv as a local audit log.
       On Streamlit Community Cloud this file is temporary, so a failure
       here must never stop the app.
    """
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = []
    st.session_state[SESSION_KEY].append(record)

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        df = pd.read_csv(FILE) if FILE.exists() else pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        df.to_csv(FILE, index=False)
    except OSError:
        pass


def load_predictions():
    """Return the assessments recorded in this browser session."""
    return list(st.session_state.get(SESSION_KEY, []))
