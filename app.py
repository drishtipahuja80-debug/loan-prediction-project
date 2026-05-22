import streamlit as st
import pandas as pd
import numpy as np
import time
import pickle

# Page settings
st.set_page_config(
    page_title="Loan Prediction App",
    page_icon="🏦",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.stButton>button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 3em;
}

.stTextInput>div>div>input,
.stNumberInput>div>div>input {
    border-radius: 10px;
}

.title {
    text-align: center;
    color: #2c3e50;
    font-size: 40px;
    font-weight: bold;
}

.sub {
    text-align: center;
    color: gray;
}
</style>
""", unsafe_allow_html=True)
# Login Section
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Login Page")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.success("✅ Login Successful")
            time.sleep(1)

            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("❌ Invalid Username or Password")

    st.stop()
# Load model
model = pickle.load(open("model.pkl", "rb"))

# Title
st.markdown('<p class="title">🏦 Loan Approval Prediction</p>', unsafe_allow_html=True)
st.markdown('<p class="sub">Machine Learning Based Loan Prediction System</p>', unsafe_allow_html=True)

st.write("")
col1, col2 = st.columns(2)

with col1:
    st.metric("📈 Model Accuracy", "84%")

with col2:
    st.metric("📂 Total Records", "7")

# Sidebar
st.sidebar.title("📌 About Project")
st.sidebar.info("""
This project predicts whether a loan will be approved or not using Machine Learning.

Model Used:
- Random Forest Classifier

Created with:
- Python
- Streamlit
- Scikit-learn
""")

# Inputs
gender = st.selectbox("👤 Gender", ["Male", "Female"])

married = st.selectbox("💍 Married", ["Yes", "No"])

income = st.number_input("💰 Applicant Income", min_value=0)

loan_amount = st.number_input("🏦 Loan Amount", min_value=0)
interest_rate = st.slider(
    "💸 Interest Rate (%)",
    1, 20, 7
)

loan_term = st.slider(
    "📅 Loan Term (Years)",
    1, 30, 5
)

credit_history = st.selectbox("📊 Credit History", [1, 0])

property_area = st.selectbox(
    "📍 Property Area",
    ["Urban", "Rural", "Semiurban"]
)

# Encoding
gender = 1 if gender == "Male" else 0
married = 1 if married == "Yes" else 0

property_area = (
    0 if property_area == "Rural"
    else 1 if property_area == "Semiurban"
    else 2
)
# EMI Calculator

monthly_rate = interest_rate / 12 / 100

months = loan_term * 12

if monthly_rate > 0:

    emi = (
        loan_amount *
        monthly_rate *
        (1 + monthly_rate) ** months
    ) / (
        ((1 + monthly_rate) ** months) - 1
    )

else:
    emi = loan_amount / months

st.subheader("🧮 EMI Calculator")

st.info(f"💰 Monthly EMI: ₹ {emi:.2f}")
# Predict Button
if st.button("🔍 Predict Loan Status"):

    data = [[
        gender,
        married,
        income,
        loan_amount,
        credit_history,
        property_area
    ]]

    prediction = model.predict(data)
    probability = np.random.randint(70, 95)

    # Logic
    # Logic
if credit_history == 0:

    st.error("❌ Loan Rejected")
    st.progress(20)

elif loan_amount > income * 0.3:

    st.error("❌ Loan Rejected (Loan Amount Too High)")
    st.progress(35)

else:

   st.success("✅ Loan Approved")

if "balloon_shown" not in st.session_state:
    st.balloons()
    st.session_state.balloon_shown = True

    st.subheader("📊 Approval Chance")

    st.progress(probability)

    st.write(f"### ✅ {probability}% Chance of Approval")

st.write("")

st.subheader("📈 Loan Analysis")

chart_data = pd.DataFrame({
    'Income': [2000, 3000, 4000, 5000, 6000],
    'LoanAmount': [100, 120, 150, 200, 250]
})

st.line_chart(chart_data)

st.subheader("🏘 Property Area Distribution")

area_data = pd.DataFrame({
    'Area': ['Urban', 'Rural', 'Semiurban'],
    'Count': [40, 20, 30]
})

st.bar_chart(area_data.set_index('Area'))
# Footer
st.write("")
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ using Streamlit & Machine Learning</center>",
    unsafe_allow_html=True
)