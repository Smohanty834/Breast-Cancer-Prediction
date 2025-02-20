import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import base64
from fpdf import FPDF

API_URL = "http://127.0.0.1:5000"  # Adjust if needed

st.set_page_config(page_title="Breast Cancer Prediction", layout="wide")
st.title("🩺 Breast Cancer Prediction System")

# Function to set background image
def set_bg(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    encoded_img = base64.b64encode(img_data).decode()
    
    # Apply custom CSS
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Call the function to set the background
set_bg("img.jpg")  # Change this to your image file

# User Inputs 
st.sidebar.header("Enter Patient Details")
name = st.sidebar.text_input("Patient Name")
age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)

st.sidebar.header("Enter Features")
feature_names = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
       'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
       'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se', 'fractal_dimension_se',
       'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst']
features = []
for feature in feature_names:
    value = st.sidebar.number_input(f"{feature.replace('_', ' ').title()}", value=0.0)
    features.append(value)

if st.sidebar.button("Predict"):
    data = {"features": features}
    response = requests.post(f"{API_URL}/predict", json=data)
    if response.status_code == 200:
        result = response.json()
        st.subheader("Prediction Result")
        if result['prediction'] == "Malignant":
            st.error("⚠️ High Risk: Malignant Tumor Detected")
        else:
            st.success("✅ Low Risk: Benign Tumor")

        # Probability Distribution
        st.write("### Probability Distribution")
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            fig, ax = plt.subplots()
            ax.bar(["Benign", "Malignant"], result["probability"], color=["green", "red"])
            st.pyplot(fig)

        # Save Report
        report_data = {"name": name, "age": age, "features": features, "prediction": result['prediction'], "probability": result['probability']}
        save_response = requests.post(f"{API_URL}/save_report", json=report_data)
        if save_response.status_code == 200:
            st.success("Report Saved Successfully")
    else:
        st.error("Prediction Failed. Please try again.")

if st.button("View Reports"):
    report_response = requests.get(f"{API_URL}/get_reports")
    if report_response.status_code == 200:
        reports = report_response.json()["reports"]
        st.session_state.reports = reports
# Function to generate PDF
if "reports" in st.session_state:
    st.write("### Patient Reports")
    for report in st.session_state.reports:
        report_id, patient_name, patient_age, _, patient_prediction, patient_probability = report
        probability = eval(patient_probability)  # Convert string back to list

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
        <div style="border:2px solid #4CAF50; border-radius:10px; padding:15px; margin-bottom:15px; background-color:#f9f9f9;">
            <h3 style="color:#1E90FF;">Patient: {patient_name}</h3>
            <p style="color:#2F4F4F;"><strong>Age:</strong> {patient_age}</p>
            <p style="color:{'red' if patient_prediction == 'Malignant' else '#228B22'};"><strong>Prediction:</strong> {patient_prediction}</p>
            <p style="color:#2F4F4F;"><strong>Probability:</strong> Benign: {float(probability[0]*100):.2f}%, Malignant: {float(probability[1]*100):.2f}%</p>
            <a href="{API_URL}/download_report/{report_id}" target="_blank">
                <button style="background-color:#008CBA; color:white; padding:8px 12px; border:none; border-radius:5px; cursor:pointer;">Download Report</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        with col2:
            if st.button(f"Delete Report", key=report_id):
                delete_response = requests.delete(f"{API_URL}/delete_report/{report_id}")
                if delete_response.status_code == 200:
                    st.session_state.reports = [r for r in st.session_state.reports if r[0] != report_id]
                    st.rerun()
                else:
                    st.error("Failed to delete report.")

if st.button("Delete All Reports"):
    delete_all_response = requests.delete(f"{API_URL}/delete_all_reports")
    if delete_all_response.status_code == 200:
        st.session_state.reports = []
        st.rerun()
    else:
        st.error("Failed to delete all reports.")
