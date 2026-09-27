from datetime import date, datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.predictor import predict_burnout
from utils.recommendations import generate_recommendation
from utils.shap_utils import get_shap_explanation, plot_waterfall
from utils.storage import save_prediction
from utils.ui import load_css, show_sidebar

st.set_page_config(
    page_title="Employee Assessment",
    page_icon="📝",
    layout="wide",
)

load_css()
show_sidebar()

st.title("Employee Burnout Assessment")
st.caption(
    "Complete the questionnaire below to generate a prediction and explanation.")

assessment_date = st.date_input("Assessment Date", value=date.today())
assessment_time = datetime.now().strftime("%H:%M:%S")
assessment_id = datetime.now().strftime("BURN-%Y%m%d-%H%M%S")

st.markdown('<span class="section-label">IDENTITY</span>',
            unsafe_allow_html=True)
st.subheader("Employee Details")
col_a, col_b = st.columns(2)
with col_a:
    employee_name = st.text_input("Employee Name")
    department = st.selectbox(
        "Department",
        [
            "Human Resources",
            "Finance",
            "IT",
            "Marketing",
            "Operations",
            "Sales",
            "Customer Service",
            "Administration",
            "Engineering",
            "Other",
        ],
    )
with col_b:
    gender = st.selectbox(
        "Gender",
        [0, 1],
        format_func=lambda x: "Male" if x == 1 else "Female",
    )
    company = st.selectbox(
        "Company Type",
        [0, 1],
        format_func=lambda x: "Private" if x == 1 else "Public",
    )

st.markdown('<span class="section-label">ROLE</span>', unsafe_allow_html=True)
st.subheader("Personal Information")
col1, col2 = st.columns(2)
with col1:
    years = st.number_input("Years in Company", 0, 17, 5)
with col2:
    designation = st.slider("Designation", 0, 5, 2)

st.markdown('<span class="section-label">WORKPLACE</span>',
            unsafe_allow_html=True)
st.subheader("Working Environment")
col1, col2 = st.columns(2)
with col1:
    workhours = st.slider("Work Hours", 35, 59, 45)
    resource = st.slider("Resource Allocation", 1, 10, 5)
    deadline = st.slider("Deadline Pressure", 1, 5, 3)
with col2:
    team = st.slider("Team Size", 1, 20, 5)
    wfh = st.selectbox(
        "WFH Available",
        [0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes",
    )

st.markdown('<span class="section-label">WELLBEING</span>',
            unsafe_allow_html=True)
st.subheader("Employee Wellbeing")
col1, col2 = st.columns(2)
with col1:
    fatigue = st.slider("Mental Fatigue", 0.0, 10.0, 5.0)
    sleep = st.slider("Sleep Hours", 3.4, 9.1, 7.0, step=0.1)
with col2:
    balance = st.slider("Work-Life Balance", 1, 5, 3)
    support = st.slider("Manager Support", 1, 5, 3)
    recognition = st.slider("Recognition Frequency", 0, 5, 2)

employee = {
    "Assessment ID": assessment_id,
    "Employee Name": employee_name,
    "Department": department,
    "Assessment Date": assessment_date,
    "Assessment Time": assessment_time,
}

model_input = {
    "Gender": gender,
    "Company Type": company,
    "Years in Company": years,
    "Designation": designation,
    "Work Hours per Week": workhours,
    "Resource Allocation": resource,
    "Deadline Pressure Score": deadline,
    "Team Size": team,
    "WFH Setup Available": wfh,
    "Mental Fatigue Score": fatigue,
    "Sleep Hours": sleep,
    "Work-Life Balance Score": balance,
    "Manager Support Score": support,
    "Recognition Frequency": recognition,
}

st.write("")
predict_clicked = st.button(
    "Predict Burnout", type="primary", use_container_width=True)

if predict_clicked:
    if not employee_name.strip():
        st.warning("Please enter an employee name before running the prediction.")
        st.stop()

    try:
        level, confidence, probabilities = predict_burnout(model_input)
        employee_df = pd.DataFrame([model_input])
        predicted_class = int(probabilities.argmax())
        shap_values, top_driver, top5 = get_shap_explanation(
            employee_df,
            predicted_class=predicted_class,
        )
        recommendation = generate_recommendation(level)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Prediction failed: {exc}")
        st.stop()

    st.success("Prediction complete")
    st.markdown(
        f"""
        ### Burnout Assessment Report
        **Assessment ID:** {assessment_id}  
        **Employee Name:** {employee_name}  
        **Department:** {department}  
        **Assessment Date:** {assessment_date}  
        **Assessment Time:** {assessment_time}
        """
    )

    st.subheader("Prediction Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Burnout Level", level)
    c2.metric("Confidence", f"{confidence:.1%}")
    c3.metric("Priority", recommendation["Priority"])

    st.divider()
    st.subheader("Top Factors Influencing this Prediction")
    for _, row in top5.iterrows():
        feature = row["Feature"]
        value = row["SHAP"]
        if value > 0:
            st.success(f"**{feature}** — increased burnout risk")
        else:
            st.info(f"**{feature}** — reduced burnout risk")

    top5 = top5.copy()
    top5["ABS"] = top5["ABS"].round(2)
    top5["ABS_Label"] = top5["ABS"].map(lambda x: f"{x:.2f}")

    fig = px.bar(
        top5,
        x="ABS",
        y="Feature",
        orientation="h",
        text="ABS_Label",
        labels={"ABS": "Mean |SHAP Value|", "Feature": "Predictor"},
        template="plotly_dark",
        color="ABS",
        color_continuous_scale="Teal",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E8EEF7",
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=20, b=10),
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("SHAP Waterfall Explanation")
    fig = plot_waterfall(shap_values, predicted_class)
    st.pyplot(fig, clear_figure=True)

    st.subheader("Recommended Actions")
    for action in recommendation["Recommendations"]:
        st.write("✅", action)

    record = employee.copy()
    record.update(model_input)
    record["Prediction"] = level
    record["Confidence"] = confidence
    record["Priority"] = recommendation["Priority"]
    record["Recommendations"] = "; ".join(recommendation["Recommendations"])
    record["Top SHAP Driver"] = top_driver
    record["Top 5 SHAP Drivers"] = "|".join(top5["Feature"].tolist())
    record["Top SHAP Scores"] = "|".join(top5["SHAP"].round(3).astype(str))
    save_prediction(record)
