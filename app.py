import streamlit as st
import numpy as np
import joblib


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Cardiovascular Health Assessment",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =============================================================================
# LOAD TRAINED MODEL
# =============================================================================

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")


model = load_model()


# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>

/* ============================================================================
   GLOBAL
   ============================================================================ */

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

.block-container {
    max-width: 1150px !important;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}


/* ============================================================================
   MAIN TITLE
   ============================================================================ */

h1 {
    color: #ef4444 !important;
    font-weight: 800 !important;
    text-align: center !important;
    margin-bottom: 8px !important;
}

.title-description {
    text-align: center;
    color: var(--text-color);
    opacity: 0.70;
    font-size: 16px;
    margin-bottom: 25px;
}


/* ============================================================================
   FORM
   ============================================================================ */

div[data-testid="stForm"] {
    background: var(--secondary-background-color) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 20px !important;
    padding: 30px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08) !important;
}


/* ============================================================================
   SECTION TITLES
   ============================================================================ */

.form-section-title {
    color: var(--text-color) !important;
    font-size: 19px !important;
    font-weight: 700 !important;

    border-left: 4px solid #ef4444;

    background: rgba(239, 68, 68, 0.08);

    padding: 11px 14px;

    border-radius: 0 10px 10px 0;

    margin-top: 8px;
    margin-bottom: 24px;

    line-height: 1.4;
}


/* ============================================================================
   INPUT LABELS
   ============================================================================ */

.stNumberInput label,
.stSelectbox label {
    color: var(--text-color) !important;
    font-size: 13px !important;
    font-weight: 650 !important;
    margin-bottom: 6px !important;
}


/* ============================================================================
   NUMBER INPUT
   ============================================================================ */

.stNumberInput input {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;

    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;

    min-height: 42px !important;
}

.stNumberInput input:hover {
    border-color: #94a3b8 !important;
}

.stNumberInput input:focus {
    border-color: #ef4444 !important;
    box-shadow: 0 0 0 1px #ef4444 !important;
}


/* ============================================================================
   SELECT BOX
   ============================================================================ */

div[data-baseweb="select"] {
    background-color: var(--background-color) !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] > div {
    background-color: var(--background-color) !important;

    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;

    color: var(--text-color) !important;

    min-height: 42px !important;
}

div[data-baseweb="select"] span {
    color: var(--text-color) !important;
}


/* ============================================================================
   SELECT DROPDOWN
   ============================================================================ */

div[data-baseweb="popover"] {
    background-color: var(--secondary-background-color) !important;
}

ul[role="listbox"] {
    background-color: var(--secondary-background-color) !important;
}

li[role="option"] {
    color: var(--text-color) !important;
}

li[role="option"]:hover {
    background-color: rgba(239, 68, 68, 0.10) !important;
}


/* ============================================================================
   SUBMIT BUTTON
   ============================================================================ */

div[data-testid="stFormSubmitButton"] button {

    width: 100% !important;

    background: #ef4444 !important;

    color: white !important;

    border: none !important;

    border-radius: 12px !important;

    min-height: 48px !important;

    padding: 12px 20px !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    margin-top: 20px !important;

    box-shadow: 0 7px 18px rgba(239, 68, 68, 0.25) !important;

    transition: all 0.2s ease !important;
}

div[data-testid="stFormSubmitButton"] button:hover {

    background: #dc2626 !important;

    color: white !important;

    transform: translateY(-1px);

    box-shadow: 0 9px 22px rgba(239, 68, 68, 0.35) !important;
}


/* ============================================================================
   RESULTS TITLE
   ============================================================================ */

.results-title {

    color: var(--text-color) !important;

    font-size: 25px !important;

    font-weight: 800 !important;

    margin-top: 30px !important;

    margin-bottom: 18px !important;
}


/* ============================================================================
   RESULT CARD
   ============================================================================ */

.result-card {

    background: var(--secondary-background-color);

    border: 1px solid var(--border-color);

    border-radius: 18px;

    padding: 22px;

    text-align: center;

    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}


/* ============================================================================
   METRICS
   ============================================================================ */

div[data-testid="stMetric"] {

    background: var(--secondary-background-color) !important;

    border: 1px solid var(--border-color) !important;

    border-radius: 14px !important;

    padding: 16px !important;

    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

div[data-testid="stMetricLabel"] {

    color: var(--text-color) !important;

    opacity: 0.65;
}

div[data-testid="stMetricValue"] {

    color: var(--text-color) !important;

    font-weight: 750 !important;
}


/* ============================================================================
   SECONDARY HEALTH TITLE
   ============================================================================ */

h3,
h4 {

    color: var(--text-color) !important;

    font-weight: 750 !important;
}


/* ============================================================================
   PROGRESS BAR
   ============================================================================ */

div[data-testid="stProgressBar"] {
    margin-top: 10px;
}


/* ============================================================================
   ALERTS
   ============================================================================ */

div[data-testid="stAlert"] {

    border-radius: 12px !important;

    border: 1px solid var(--border-color) !important;
}


/* ============================================================================
   DIVIDER
   ============================================================================ */

hr {

    border-color: var(--border-color) !important;
}


/* ============================================================================
   FOOTER
   ============================================================================ */

.footer {

    text-align: center;

    color: var(--text-color) !important;

    opacity: 0.45;

    margin-top: 45px;

    padding-top: 20px;

    border-top: 1px solid var(--border-color);

    font-size: 13px;
}


/* ============================================================================
   MOBILE
   ============================================================================ */

@media (max-width: 768px) {

    .block-container {

        padding-left: 1rem !important;

        padding-right: 1rem !important;
    }

    div[data-testid="stForm"] {

        padding: 20px !important;
    }

    h1 {

        font-size: 29px !important;
    }

    .title-description {

        font-size: 14px;
    }
}

</style>
""", unsafe_allow_html=True)


# =============================================================================
# HEADER
# =============================================================================

st.title("❤️ Cardiovascular Risk Assessment")

st.markdown(
    """
    <div class="title-description">
        Enter your health details below to estimate cardiovascular
        disease risk using our trained machine learning model.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =============================================================================
# FORM
# =============================================================================

with st.form("cardio_risk_form"):

    # =========================================================================
    # SECTION 1 - PATIENT PROFILE
    # =========================================================================

    st.markdown(
        """
        <div class="form-section-title">
            1. Patient Profile & Demographics
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4, gap="medium")


    # -------------------------------------------------------------------------
    # AGE
    # -------------------------------------------------------------------------

    with c1:

        age = st.number_input(
            "Age (Years)",
            min_value=18,
            max_value=100,
            value=25,
            step=1
        )


    # -------------------------------------------------------------------------
    # GENDER
    # -------------------------------------------------------------------------

    with c2:

        gender_str = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        gender = 1 if gender_str == "Female" else 2


    # -------------------------------------------------------------------------
    # HEIGHT
    # -------------------------------------------------------------------------

    with c3:

        height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=230,
            value=170,
            step=1
        )


    # -------------------------------------------------------------------------
    # WEIGHT
    # -------------------------------------------------------------------------

    with c4:

        weight = st.number_input(
            "Weight (kg)",
            min_value=30.0,
            max_value=200.0,
            value=60.0,
            step=0.5
        )


    # =========================================================================
    # SECTION 2 - CLINICAL MEASUREMENTS
    # =========================================================================

    st.markdown(
        """
        <div class="form-section-title">
            2. Clinical Measurements & Vitals
        </div>
        """,
        unsafe_allow_html=True
    )

    c5, c6, c7, c8 = st.columns(4, gap="medium")


    # -------------------------------------------------------------------------
    # SYSTOLIC BP
    # -------------------------------------------------------------------------

    with c5:

        ap_hi = st.number_input(
            "Systolic BP (mmHg)",
            min_value=70,
            max_value=240,
            value=110,
            step=1
        )


    # -------------------------------------------------------------------------
    # DIASTOLIC BP
    # -------------------------------------------------------------------------

    with c6:

        ap_lo = st.number_input(
            "Diastolic BP (mmHg)",
            min_value=40,
            max_value=160,
            value=70,
            step=1
        )


    # -------------------------------------------------------------------------
    # CHOLESTEROL
    # -------------------------------------------------------------------------

    with c7:

        cholesterol_str = st.selectbox(
            "Cholesterol Level",
            [
                "Normal",
                "Above Normal",
                "Well Above Normal"
            ]
        )

        chol_map = {
            "Normal": 1,
            "Above Normal": 2,
            "Well Above Normal": 3
        }

        cholesterol = chol_map[cholesterol_str]


    # -------------------------------------------------------------------------
    # GLUCOSE
    # -------------------------------------------------------------------------

    with c8:

        gluc_str = st.selectbox(
            "Glucose Level",
            [
                "Normal",
                "Above Normal",
                "Well Above Normal"
            ]
        )

        gluc_map = {
            "Normal": 1,
            "Above Normal": 2,
            "Well Above Normal": 3
        }

        gluc = gluc_map[gluc_str]


    # =========================================================================
    # SECTION 3 - LIFESTYLE
    # =========================================================================

    st.markdown(
        """
        <div class="form-section-title">
            3. Lifestyle Behaviors
        </div>
        """,
        unsafe_allow_html=True
    )

    c9, c10, c11 = st.columns(3, gap="medium")


    # -------------------------------------------------------------------------
    # SMOKING
    # -------------------------------------------------------------------------

    with c9:

        smoke_str = st.selectbox(
            "Smoking Status",
            ["Non-Smoker", "Smoker"]
        )

        smoke = 1 if smoke_str == "Smoker" else 0


    # -------------------------------------------------------------------------
    # ALCOHOL
    # -------------------------------------------------------------------------

    with c10:

        alco_str = st.selectbox(
            "Alcohol Consumption",
            ["No", "Yes"]
        )

        alco = 1 if alco_str == "Yes" else 0


    # -------------------------------------------------------------------------
    # PHYSICAL ACTIVITY
    # -------------------------------------------------------------------------

    with c11:

        active_str = st.selectbox(
            "Physical Activity",
            ["Active", "Inactive"]
        )

        active = 1 if active_str == "Active" else 0


    # =========================================================================
    # SUBMIT BUTTON
    # =========================================================================

    submit_btn = st.form_submit_button(
        "Calculate Risk Evaluation"
    )


# =============================================================================
# PREDICTION
# =============================================================================

if submit_btn:

    # =========================================================================
    # BLOOD PRESSURE VALIDATION
    # =========================================================================

    if ap_lo >= ap_hi:

        st.error(
            "Diastolic BP must be lower than Systolic BP."
        )

        st.stop()


    # =========================================================================
    # PREPARE INPUT
    # =========================================================================

    features = np.array([[
        age,
        gender,
        height,
        weight,
        ap_hi,
        ap_lo,
        cholesterol,
        gluc,
        smoke,
        alco,
        active
    ]])


    # =========================================================================
    # MODEL PREDICTION
    # =========================================================================

    try:

        prediction = int(
            model.predict(features)[0]
        )

        risk_prob = float(
            model.predict_proba(features)[0][1]
        )

    except Exception as e:

        st.error(
            "There is a mismatch between the input data and the trained model."
        )

        st.code(str(e))

        st.stop()


    risk_percentage = risk_prob * 100


    # =========================================================================
    # RESULTS TITLE
    # =========================================================================

    st.markdown(
        '<div class="results-title">Evaluation Results</div>',
        unsafe_allow_html=True
    )


    # =========================================================================
    # RESULT LAYOUT
    # =========================================================================

    res_col1, res_col2 = st.columns(
        [1, 2],
        gap="large"
    )


    # =========================================================================
    # RISK RESULT
    # =========================================================================

    with res_col1:

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        if prediction == 1:

            st.error(
                "⚠️ High Risk Detected"
            )

        else:

            st.success(
                "✅ Lower Risk Detected"
            )


        st.metric(
            "Estimated Model Risk Probability",
            f"{risk_percentage:.1f}%"
        )


        st.progress(
            min(max(int(risk_percentage), 0), 100)
        )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =========================================================================
    # SECONDARY HEALTH INFORMATION
    # =========================================================================

    with res_col2:

        st.markdown(
            "#### Patient Secondary Health Markers"
        )


        # ---------------------------------------------------------------------
        # BMI
        # ---------------------------------------------------------------------

        height_m = height / 100.0

        bmi = weight / (height_m ** 2)


        # ---------------------------------------------------------------------
        # PULSE PRESSURE
        # ---------------------------------------------------------------------

        pulse_pressure = ap_hi - ap_lo


        # ---------------------------------------------------------------------
        # LIFESTYLE STATUS
        # ---------------------------------------------------------------------

        lifestyle_status = (
            "Good"
            if smoke == 0 and active == 1
            else "Needs Attention"
        )


        # ---------------------------------------------------------------------
        # METRICS
        # ---------------------------------------------------------------------

        m1, m2, m3 = st.columns(3)


        with m1:

            st.metric(
                "Body Mass Index (BMI)",
                f"{bmi:.1f}"
            )


        with m2:

            st.metric(
                "Pulse Pressure",
                f"{pulse_pressure} mmHg"
            )


        with m3:

            st.metric(
                "Lifestyle Status",
                lifestyle_status
            )


        # =====================================================================
        # RESULT MESSAGE
        # =====================================================================

        if prediction == 1:

            st.warning(
                "The machine learning model estimates an elevated "
                "cardiovascular disease risk based on the provided inputs. "
                "This result is not a medical diagnosis."
            )

        else:

            st.info(
                "The machine learning model estimates a lower "
                "cardiovascular disease risk based on the provided inputs. "
                "This result is not a medical diagnosis."
            )


# =============================================================================
# FOOTER
# =============================================================================

st.markdown(
    """
    <div class="footer">
        Cardiovascular Risk Assessment • Machine Learning Project
    </div>
    """,
    unsafe_allow_html=True
)