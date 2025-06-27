import streamlit as st
import numpy as np
from PIL import Image

# --- Page Setup ---
st.set_page_config(page_title="NIMHANS Pediatric PTCI Calculator", layout="centered")

# --- Title and Logo ---
st.image("nimhans_logo.png", width=120)  # Save logo in the same directory
st.title("🧠 NIMHANS Pediatric Post-Traumatic Cerebral Infarction Risk Calculator")

st.markdown("""
This calculator estimates the probability of developing **Post-Traumatic Cerebral Infarction (PTCI)** in pediatric patients based on a multivariate logistic regression model derived from institutional data.
""")

# --- Input Section ---
st.header("Patient Factors")

sdh = st.radio("Presence of SDH/Contusion/DAI", ["Absent (0)", "Present (1)"])
instability = st.radio("Intraoperative Hemodynamic Instability", ["Absent (0)", "Present (1)"])
fall = st.radio("Mechanism of Injury: Fall from Height", ["No (0)", "Yes (1)"])

# --- Encode Inputs ---
X_sdh = 1 if "Present" in sdh else 0
X_instability = 1 if "Present" in instability else 0
X_fall = 1 if "Yes" in fall else 0

# --- Logistic Model Coefficients ---
intercept = -1.02
coef_sdh = 3.24
coef_instability = 2.80
coef_fall = 1.97

# --- Calculate Log-Odds and Probability ---
log_odds = intercept + coef_sdh * X_sdh + coef_instability * X_instability + coef_fall * X_fall
probability = 1 / (1 + np.exp(-log_odds))

# --- Display Output ---
st.subheader("🧮 Predicted Risk of PTCI:")
st.metric(label="Probability", value=f"{probability*100:.2f} %")

# --- Optional Nomogram-style Display ---
st.subheader("📊 Nomogram-based Point Assignment")

def get_points(value, points_if_present):
    return points_if_present if value == 1 else 0

points_sdh = get_points(X_sdh, 100)
points_instability = get_points(X_instability, 75)
points_fall = get_points(X_fall, 50)
total_points = points_sdh + points_instability + points_fall

st.write(f"**SDH/Contusion Present:** {points_sdh} points")
st.write(f"**Intraop Instability Present:** {points_instability} points")
st.write(f"**Fall from Height:** {points_fall} points")

st.markdown(f"### 🎯 **Total Nomogram Score:** {total_points} points")

# Optional: Risk curve mapping score to probability (visual if available)
