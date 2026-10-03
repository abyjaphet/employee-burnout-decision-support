import streamlit as st

SESSION_KEY = "predictions"


def save_prediction(record):
    """Store an assessment for this browser session only.

    Records live in st.session_state, so each visitor to the public app
    sees only their own assessments, and nothing is written to the server.
    """
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = []
    st.session_state[SESSION_KEY].append(record)


def load_predictions():
    """Return the assessments recorded in this browser session."""
    return list(st.session_state.get(SESSION_KEY, []))
