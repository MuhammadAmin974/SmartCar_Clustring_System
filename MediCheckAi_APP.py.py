import streamlit as st
import joblib
import base64
import pickle
from PIL import Image

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="MediCheck AI",
    page_icon="🏥",
    layout="wide"
)

# -----------------------------
# LOAD MODELS
# -----------------------------
heart_model = joblib.load("Heart_disease.joblib")
diabetes_model = joblib.load("Diabetes_Prediction.joblib")
parkinsons_model = pickle.load(open("parkinsons.pkl", "rb"))

# -----------------------------
# IMAGE TO BASE64
# -----------------------------
def get_base64(path):
    with open(path,"rb") as f:
        return base64.b64encode(f.read()).decode()

# -----------------------------
# BACKGROUND IMAGE
# -----------------------------
def set_background(image):

    img = get_base64(image)

    st.markdown(f"""
    <style>

    .stApp {{
        background-image: linear-gradient(
        rgba(0,0,0,0.45),
        rgba(0,0,0,0.45)),
        url("data:image/jpg;base64,{img}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

section[data-testid="stSidebar"]{
    background:#0b1320;
}

section[data-testid="stSidebar"] *{
    color:white;
}

.title{
    text-align:center;
    font-size:50px;
    color:#00E5FF;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    font-size:22px;
    color:white;
}

.card{

background:rgba(255,255,255,.15);

padding:30px;

border-radius:15px;

backdrop-filter:blur(10px);

}

.stButton>button{

background:#00B4D8;

color:white;

font-size:18px;

border-radius:10px;

width:100%;

height:50px;

border:none;

}

.stButton>button:hover{

background:#0077B6;

color:white;

}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🏥 MediCheck AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "❤️ Heart Disease Prediction",
        "🩸 Diabetes Prediction"
        
    ]
)

# =====================================================
# HOME PAGE
# =====================================================

if page=="🏠 Home":

    st.markdown("<h1 class='title'>MediCheck AI</h1>",unsafe_allow_html=True)

    st.markdown("<p class='subtitle'>Multiple Disease Prediction System using Machine Learning</p>",unsafe_allow_html=True)

    col1,col2=st.columns([1,1])

    with col1:

        st.image(
            "medical.jfif",
            use_container_width=True
        )

    with col2:

        st.markdown("""
        <div class='card'>

        <h2>Welcome</h2>

        <hr>

        <p>

        MediCheck AI is an intelligent healthcare system
        that predicts multiple diseases using Machine
        Learning algorithms.

        </p>

        <h3>Available Prediction Systems</h3>

        ❤️ Heart Disease Prediction

        <br><br>

        🩸 Diabetes Prediction

       
        </div>

        """,unsafe_allow_html=True)


    # =====================================================
# HEART DISEASE PREDICTION
# =====================================================

elif page == "❤️ Heart Disease Prediction":

    # Background Image
    # set_background("hear.jfif")

    st.markdown(
        "<h1 style='text-align:center;color:Black;'>❤️ Heart Disease Prediction System</h1>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age (Years)",
            min_value=1,
            max_value=120,
            value=30
        )

        sex = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        cp = st.selectbox(
            "Chest Pain Type",
            [
                "Typical Angina",
                "Atypical Angina",
                "Non-anginal Pain",
                "Asymptomatic"
            ]
        )

        trestbps = st.number_input(
            "Resting Blood Pressure (mm Hg)",
            value=120
        )

        chol = st.number_input(
            "Serum Cholesterol (mg/dl)",
            value=200
        )

        fbs = st.selectbox(
            "Fasting Blood Sugar > 120 mg/dl ?",
            ["No", "Yes"]
        )

        restecg = st.selectbox(
            "Resting ECG Results",
            [
                "Normal",
                "ST-T Wave Abnormality",
                "Left Ventricular Hypertrophy"
            ]
        )

    with col2:

        thalach = st.number_input(
            "Maximum Heart Rate Achieved",
            value=150
        )

        exang = st.selectbox(
            "Exercise Induced Angina",
            ["No", "Yes"]
        )

        oldpeak = st.number_input(
            "ST Depression (Oldpeak)",
            value=1.0,
            step=0.1
        )

        slope = st.selectbox(
            "Slope of Peak Exercise ST Segment",
            [
                "Upsloping",
                "Flat",
                "Downsloping"
            ]
        )

        ca = st.selectbox(
            "Number of Major Vessels (0-3)",
            [0, 1, 2, 3]
        )

        thal = st.selectbox(
            "Thalassemia Type",
            [
                "Normal",
                "Fixed Defect",
                "Reversible Defect"
            ]
        )

    # ---------------------------------------
    # Encoding
    # ---------------------------------------

    sex = 1 if sex == "Male" else 0

    cp = {
        "Typical Angina": 0,
        "Atypical Angina": 1,
        "Non-anginal Pain": 2,
        "Asymptomatic": 3
    }[cp]

    fbs = 1 if fbs == "Yes" else 0

    restecg = {
        "Normal": 0,
        "ST-T Wave Abnormality": 1,
        "Left Ventricular Hypertrophy": 2
    }[restecg]

    exang = 1 if exang == "Yes" else 0

    slope = {
        "Upsloping": 0,
        "Flat": 1,
        "Downsloping": 2
    }[slope]

    thal = {
        "Normal": 1,
        "Fixed Defect": 2,
        "Reversible Defect": 3
    }[thal]

    # ---------------------------------------
    # Prediction Button
    # ---------------------------------------

    st.write("")

    if st.button("❤️ Predict Heart Disease"):

        prediction = heart_model.predict([[
            age,
            sex,
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            slope,
            ca,
            thal
        ]])

        st.write("")

        if prediction[0] == 1:

            st.error("⚠ Patient is likely to have Heart Disease.")

        else:

            st.success("✅ Patient is Healthy.")
# =====================================================
# DIABETES PREDICTION
# =====================================================

elif page == "🩸 Diabetes Prediction":

    st.markdown(
        "<h1 style='text-align:center;color:#0d6efd;'>🩸 Diabetes Prediction System</h1>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        pregnancies = st.number_input(
            "Number of Pregnancies",
            min_value=0,
            value=0
        )

        glucose = st.number_input(
            "Glucose Level (mg/dL)",
            value=120
        )

        blood_pressure = st.number_input(
            "Blood Pressure (mm Hg)",
            value=70
        )

        skin_thickness = st.number_input(
            "Skin Thickness (mm)",
            value=20
        )

    with col2:

        insulin = st.number_input(
            "Insulin Level (mu U/ml)",
            value=79
        )

        bmi = st.number_input(
            "Body Mass Index (BMI)",
            value=25.0,
            step=0.1
        )

        dpf = st.number_input(
            "Diabetes Pedigree Function",
            value=0.47,
            step=0.01
        )

        age = st.number_input(
            "Age (Years)",
            min_value=1,
            max_value=120,
            value=30
        )

    st.write("")

    if st.button("🩸 Predict Diabetes"):

        prediction = diabetes_model.predict([[
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            dpf,
            age
        ]])

        st.write("")

        if prediction[0] == 1:

            st.error("⚠ Patient is likely to have Diabetes.")

        else:

            st.success("✅ Patient is Healthy.")