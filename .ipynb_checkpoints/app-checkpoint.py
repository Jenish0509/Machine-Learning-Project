import streamlit as st
import numpy as np

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Cardiovascular Health Assessment",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS FOR PADDING, MARGINS & MODERN GLASSMORPHIC UI
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Base Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #f8fafc;
    }

    /* Outer Container Spacing Optimization */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1100px !important;
    }

    /* Glassmorphic Header Card */
    .header-card {
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.25rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
    }

    .header-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f87171 0%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .header-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* Form Container Padding & Elevation */
    div[data-testid="stForm"] {
        background: rgba(30, 41, 59, 0.55);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.25rem !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
    }

    /* Form Section Dividers */
    .form-section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        border-left: 4px solid #ef4444;
        padding-left: 0.75rem;
    }

    /* Form Elements Vertical Spacing */
    .stNumberInput, .stSelectbox {
        margin-bottom: 1.25rem !important;
    }

    .stNumberInput label, .stSelectbox label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.4rem !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    /* SPECIFIC TARGETING: Custom Form Submit Button ONLY */
    /* This prevents the + / - buttons and dropdown toggles from breaking */
    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.85rem 1.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        cursor: pointer;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.35) !important;
        margin-top: 1rem !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.5) !important;
    }

    /* Metrics Container Styling */
    .result-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.75rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# STANDALONE MODEL CALCULATION 
# -----------------------------------------------------------------------------
# Coefficients extracted directly from model metadata
MODEL_COEFFICIENTS = np.array([[
    0.05260196,  # age (in years)
    -0.02181747, # gender (1: female, 2: male)
    -0.00395379, # height (cm)
    0.01083652,  # weight (kg)
    0.05609385,  # ap_hi (systolic)
    0.01062081,  # ap_lo (diastolic)
    0.49081273,  # cholesterol (1, 2, 3)
    -0.10839217, # gluc (1, 2, 3)
    -0.12836214, # smoke (0, 1)
    -0.18721644, # alco (0, 1)
    -0.21850119  # active (0, 1)
]])
MODEL_INTERCEPT = np.array([-0.13426214])

def predict_cardio_risk(features):
    """Calculates Logistic Regression prediction probability and binary output."""
    z = np.dot(features, MODEL_COEFFICIENTS.T) + MODEL_INTERCEPT
    probability = 1 / (1 + np.exp(-z))
    risk_prob = float(probability[0][0])
    prediction = 1 if risk_prob >= 0.5 else 0
    return prediction, risk_prob

# -----------------------------------------------------------------------------
# HEADER CARD
# -----------------------------------------------------------------------------
st.markdown("""
<div class="header-card">
    <div class="header-title">Cardiovascular Risk Assessment</div>
    <div class="header-subtitle">Provide your health metrics below to evaluate cardiovascular risk probability using our trained predictive model.</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FORM AND INPUT METRICS
# -----------------------------------------------------------------------------
with st.form("cardio_risk_form"):

    # SECTION 1: PHYSICAL MEASUREMENTS
    st.markdown('<div class="form-section-title">1. Patient Profile & Demographics</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        age = st.number_input("Age (Years)", min_value=18, max_value=100, value=50, step=1)
    with c2:
        gender_str = st.selectbox("Gender", options=["Female", "Male"], index=0)
        gender = 1 if gender_str == "Female" else 2
    with c3:
        height = st.number_input("Height (cm)", min_value=100, max_value=230, value=165, step=1)
    with c4:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 2: CLINICAL MEASUREMENTS
    st.markdown('<div class="form-section-title">2. Clinical Marks & Vitals</div>', unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4, gap="medium")

    with c5:
        ap_hi = st.number_input("Systolic BP (mmHg)", min_value=70, max_value=240, value=120, step=1)
    with c6:
        ap_lo = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=160, value=80, step=1)
    with c7:
        cholesterol_str = st.selectbox("Cholesterol Level", options=["Normal", "Above Normal", "Well Above Normal"], index=0)
        chol_map = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}
        cholesterol = chol_map[cholesterol_str]
    with c8:
        gluc_str = st.selectbox("Glucose Level", options=["Normal", "Above Normal", "Well Above Normal"], index=0)
        gluc_map = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}
        gluc = gluc_map[gluc_str]

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 3: LIFESTYLE FACTORS
    st.markdown('<div class="form-section-title">3. Lifestyle Behaviors</div>', unsafe_allow_html=True)
    c9, c10, c11 = st.columns(3, gap="medium")

    with c9:
        smoke_str = st.selectbox("Smoking Status", options=["Non-Smoker", "Smoker"], index=0)
        smoke = 1 if smoke_str == "Smoker" else 0
    with c10:
        alco_str = st.selectbox("Alcohol Consumption", options=["No", "Yes"], index=0)
        alco = 1 if alco_str == "Yes" else 0
    with c11:
        active_str = st.selectbox("Physical Activity", options=["Active", "Inactive"], index=0)
        active = 1 if active_str == "Active" else 0

    submit_btn = st.form_submit_button(label="Calculate Risk Evaluation")

# -----------------------------------------------------------------------------
# PREDICTION & RESULTS DISPLAY
# -----------------------------------------------------------------------------
if submit_btn:
    features = np.array([[
        age, gender, height, weight, ap_hi, ap_lo, 
        cholesterol, gluc, smoke, alco, active
    ]])

    prediction, risk_prob = predict_cardio_risk(features)
    risk_percentage = risk_prob * 100

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### Evaluation Results")

    res_col1, res_col2 = st.columns([1, 2], gap="large")

    with res_col1:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        if prediction == 1:
            st.error("Elevated Risk Detected")
        else:
            st.success("Low Risk Detected")

        st.metric(label="Predicted Cardiovascular Disease Probability", value=f"{risk_percentage:.1f}%")
        st.progress(int(risk_percentage))
        st.markdown('</div>', unsafe_allow_html=True)

    with res_col2:
        st.markdown("#### Patient Secondary Health Markers")
        height_m = height / 100.0
        bmi = weight / (height_m ** 2)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Body Mass Index (BMI)", f"{bmi:.1f}")
        m2.metric("Pulse Pressure", f"{ap_hi - ap_lo} mmHg")
        m3.metric("Lifestyle Status", "Optimal" if (smoke == 0 and active == 1) else "Needs Attention")

        if risk_percentage >= 50:
            st.warning("Clinical metrics signal elevated cardiovascular risk. Consult a medical healthcare professional for further clinical assessment.")
        else:
            st.info("Clinical metrics indicate normal expected ranges. Maintain active lifestyle behaviors and balanced nutrition.")