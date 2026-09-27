import streamlit as st

from utils.ui import load_css, show_sidebar

st.set_page_config(
    page_title="Employee Burnout Decision Support Framework",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
show_sidebar()

st.sidebar.success("Use the pages on the left to move through the framework.")

st.markdown(
    """
    <div class="hero">
      <h1>Employee Burnout Decision Support Framework</h1>
      <h3>Predicting employee burnout with explainable machine learning</h3>
      <p>
        Supporting organisational decision-making through Explainable Artificial Intelligence (XAI).
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card-grid">
      <div class="card">
        <h2>📝 Employee Assessment</h2>
        <p>Complete the burnout questionnaire and capture workplace context.</p>
      </div>
      <div class="card">
        <h2>🤖 Explainable AI</h2>
        <p>XGBoost predicts burnout risk and SHAP shows why the model decided that.</p>
      </div>
      <div class="card">
        <h2>📊 Decision Support</h2>
        <p>Give managers clear priorities and recommended wellbeing actions.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("System Workflow")
st.markdown(
    """
    <div class="workflow">
      <ol>
        <li>Employee completes assessment</li>
        <li>XGBoost predicts burnout level</li>
        <li>SHAP explains the prediction</li>
        <li>Decision-support recommendations are generated</li>
        <li>Results are stored for the organisational dashboard</li>
      </ol>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.subheader("About")
st.markdown(
    """
    <div class="about-panel">
      This Decision Support Framework was developed as part of an MSc Data Science dissertation.
      It combines Explainable Artificial Intelligence with machine learning to help organisations
      identify employees at risk of burnout.<br><br>
      The framework predicts <strong>Low</strong>, <strong>Moderate</strong>, or <strong>High</strong>
      burnout and explains the prediction with SHAP.
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("Open **Employee Assessment** in the sidebar to begin.")
