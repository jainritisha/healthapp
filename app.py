import streamlit as st
import pandas as pd
import os
import uuid
import json
from pathlib import Path

# Set app config
st.set_page_config(page_title="Health Repository", layout="wide")

# CSV file to store users
USERS_FILE = "users.csv"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Utility Functions
def load_users():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["name", "phone", "email", "gender", "height", "weight"])
        df.to_csv(USERS_FILE, index=False)
    return pd.read_csv(USERS_FILE)

def save_user(user):
    df = load_users()
    if user['email'] in df['email'].values:
        return False
    df = pd.concat([df, pd.DataFrame([user])], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)
    return True

def validate_user(name, phone):
    df = load_users()
    user = df[(df['name'] == name) & (df['phone'].astype(str) == str(phone))]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

def calculate_bmi(height_cm, weight_kg):
    try:
        height_m = float(height_cm) / 100
        bmi = float(weight_kg) / (height_m ** 2)
        return round(bmi, 2)
    except:
        return None

def analyze_file(file):
    filename = os.path.join(UPLOAD_DIR, file.name)
    with open(filename, "wb") as f:
        f.write(file.read())
    # Dummy check for "report" or "prescription" in file name
    if "report" in file.name.lower():
        file_type = "Medical Report"
    elif "prescription" in file.name.lower():
        file_type = "Prescription"
    else:
        file_type = "Unknown Document"
    return file_type, filename

# Styling
st.markdown("""
    <style>
        .main { background-color: white; }
        h1 { color: #005288; }
        .stTextInput>div>div>input { color: black; }
    </style>
""", unsafe_allow_html=True)

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# App title
st.title("Health Repository")

# Login/Register system
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        if st.button("Login"):
            user = validate_user(name, phone)
            if user:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.user = user
                st.experimental_rerun()
            else:
                st.error("User not found. Please register.")

    with tab2:
        st.subheader("Register")
        reg_name = st.text_input("Full Name")
        reg_phone = st.text_input("Phone Number")
        reg_email = st.text_input("Email")
        reg_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        reg_height = st.text_input("Height (cm)")
        reg_weight = st.text_input("Weight (kg)")

        if st.button("Register"):
            user_data = {
                "name": reg_name,
                "phone": reg_phone,
                "email": reg_email,
                "gender": reg_gender,
                "height": reg_height,
                "weight": reg_weight,
            }
            if save_user(user_data):
                st.success("Registered successfully! Now you can login.")
            else:
                st.error("Email already registered!")

# After login dashboard
else:
    st.subheader(f"Welcome, {st.session_state.user['name']}")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Phone:** {st.session_state.user['phone']}")
        st.write(f"**Email:** {st.session_state.user['email']}")
        st.write(f"**Gender:** {st.session_state.user['gender']}")
    with col2:
        bmi = calculate_bmi(st.session_state.user['height'], st.session_state.user['weight'])
        st.write(f"**Height:** {st.session_state.user['height']} cm")
        st.write(f"**Weight:** {st.session_state.user['weight']} kg")
        st.write(f"**BMI:** {bmi}")
        if bmi:
            if bmi < 18.5:
                st.warning("Underweight")
            elif bmi < 25:
                st.success("Normal weight")
            else:
                st.error("Overweight or Obese")

    # Upload report
    st.markdown("---")
    st.header("Upload Medical Document")
    uploaded_file = st.file_uploader("Upload your prescription or report", type=["pdf", "jpg", "png"])
    if uploaded_file:
        file_type, path = analyze_file(uploaded_file)
        st.success(f"Uploaded as: {file_type}")
        st.write(f"File saved at: {path}")

    # Logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.experimental_rerun()
