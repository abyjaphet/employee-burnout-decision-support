from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.ui import load_css, show_sidebar

st.set_page_config(
    page_title="Manager Dashboard",
    page_icon="📊",
    layout="wide",
)

load_css()
show_sidebar()

st.title("Manager Decision Support Dashboard")
st.caption("Monitor employee burnout across the organisation.")

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "predictions.csv"

if not DATA_FILE.exists():
    st.warning("No employee assessments available yet.")
    st.stop()

df = pd.read_csv(DATA_FILE)
df["Confidence"] = pd.to_numeric(df["Confidence"], errors="coerce")
df["Assessment Date"] = pd.to_datetime(df["Assessment Date"], errors="coerce")
df["Gender"] = df["Gender"].map({0: "Female", 1: "Male"})
df["Company Type"] = df["Company Type"].map({0: "Public", 1: "Private"})

high = int((df["Prediction"] == "High").sum())
moderate = int((df["Prediction"] == "Moderate").sum())
low = int((df["Prediction"] == "Low").sum())
total = len(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Employees Assessed", total)
c2.metric("High", high)
c3.metric("Moderate", moderate)
c4.metric("Low", low)

st.divider()
st.subheader("Burnout Distribution")

burnout = df["Prediction"].value_counts().reset_index()
burnout.columns = ["Burnout", "Employees"]

fig = px.pie(
    burnout,
    names="Burnout",
    values="Employees",
    hole=0.62,
    color="Burnout",
    color_discrete_map={
        "Low": "#34D399",
        "Moderate": "#FBBF24",
        "High": "#F87171",
    },
    template="plotly_dark",
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E8EEF7",
    legend_font_color="#E8EEF7",
    margin=dict(t=20, b=20, l=10, r=10),
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Burnout Overview")
fig = px.bar(
    burnout,
    x="Burnout",
    y="Employees",
    text="Employees",
    color="Burnout",
    color_discrete_map={
        "Low": "#34D399",
        "Moderate": "#FBBF24",
        "High": "#F87171",
    },
    template="plotly_dark",
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E8EEF7",
    showlegend=False,
    margin=dict(t=20, b=20, l=10, r=10),
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Prediction Confidence")
avg_confidence = float(df["Confidence"].mean(
)) if df["Confidence"].notna().any() else 0.0
fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=avg_confidence * 100,
        number={"suffix": "%", "font": {"color": "#E8EEF7"}},
        title={"text": "Average Prediction Confidence",
               "font": {"color": "#E8EEF7"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
            "bar": {"color": "#38BDF8"},
            "bgcolor": "#1E293B",
            "bordercolor": "#334155",
            "steps": [
                {"range": [0, 50], "color": "#0F172A"},
                {"range": [50, 75], "color": "#152033"},
                {"range": [75, 100], "color": "#1E3A5F"},
            ],
        },
    )
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#E8EEF7",
    margin=dict(t=40, b=20, l=10, r=10),
    height=320,
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Employee Records")
st.dataframe(
    df.sort_values("Assessment Date", ascending=False),
    use_container_width=True,
)

employee = st.text_input("Search Employee")
if employee:
    result = df[
        df["Employee Name"].fillna("").str.contains(
            employee, case=False, na=False)
    ]
    st.dataframe(result, use_container_width=True)

st.divider()
st.subheader("Employee Report")
selected = st.selectbox(
    "Select Employee",
    df["Employee Name"].fillna("Unknown"),
)
row = df[df["Employee Name"] == selected].iloc[0]

st.subheader("Employee Summary")
with st.container(border=True):
    st.markdown("### Employee Information")
    c1, c2, c3 = st.columns(3)
    c1.metric("Employee", row["Employee Name"])
    c2.metric("Department", row["Department"])
    assessment_date = pd.to_datetime(row["Assessment Date"], errors="coerce")
    date_label = (
        assessment_date.strftime("%d-%b-%Y")
        if pd.notna(assessment_date)
        else "Unknown"
    )
    c3.metric("Assessment Date", date_label)

    st.divider()
    st.markdown("### Prediction Result")
    c1, c2, c3 = st.columns(3)
    c1.metric("Burnout Level", row["Prediction"])
    c2.metric("Confidence", f"{float(row['Confidence']):.1%}")
    c3.metric("Priority", row["Priority"])

    st.divider()
    left, right = st.columns([1, 2])
    with left:
        st.markdown("### Primary Driver")
        st.info(str(row["Top SHAP Driver"]))
    with right:
        st.markdown("### Top 5 Burnout Drivers")
        drivers = str(row["Top 5 SHAP Drivers"]).split("|")
        for i, driver in enumerate(drivers, start=1):
            st.write(f"**{i}.** {driver}")

st.subheader("Recommended HR Actions")
with st.container(border=True):
    for item in str(row["Recommendations"]).split(";"):
        if item.strip():
            st.success(item.strip())

st.divider()
st.subheader("Organisational Insight")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Average Confidence", f"{avg_confidence:.1%}")
c2.metric("High", high)
c3.metric("Moderate", moderate)
c4.metric("Low", low)

st.subheader("Organisation Burnout Drivers")
driver_counts = df["Top SHAP Driver"].value_counts().reset_index()
driver_counts.columns = ["Driver", "Frequency"]
fig = px.bar(
    driver_counts,
    x="Frequency",
    y="Driver",
    orientation="h",
    color="Frequency",
    text="Frequency",
    template="plotly_dark",
    color_continuous_scale="Teal",
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E8EEF7",
    coloraxis_showscale=False,
    margin=dict(t=20, b=20, l=10, r=10),
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Prediction Summary")
st.dataframe(
    df[["Employee Name", "Department", "Prediction", "Confidence"]],
    use_container_width=True,
)

st.download_button(
    "Download CSV Report",
    df.to_csv(index=False),
    "burnout_report.csv",
    "text/csv",
)
