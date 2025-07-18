import streamlit as st
from datetime import datetime
import pandas as pd

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "patient_data" not in st.session_state:
    st.session_state.patient_data = {
        "First Name": "",
        "Middle Name": "",
        "Last Name": "",
        "Date of Birth": "",
        "Phone": "",
        "Email": "",
        "Height (cm)": "",
        "Weight (kg)": "",
        "Vitals History": []
    }

# --------- LOGIN PAGE ---------
def login_page():
    st.title("Patient Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        submitted = st.form_submit_button("Login")

        if submitted:
            # Dummy login for now (you can add authentication later)
            if email and phone:
                st.session_state.logged_in = True
                st.session_state.patient_data["Email"] = email
                st.session_state.patient_data["Phone"] = phone
                st.success("Login successful!")
            else:
                st.error("Please enter both email and phone number to login.")

# --------- PROFILE SIDEBAR ---------
def profile_sidebar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
        full_name = f"{st.session_state.patient_data['First Name']} {st.session_state.patient_data['Middle Name']} {st.session_state.patient_data['Last Name']}"
        st.markdown(f"### {full_name}")
        st.markdown(f"📧 {st.session_state.patient_data['Email']}")
        st.markdown(f"📱 {st.session_state.patient_data['Phone']}")
        st.markdown(f"🎂 {st.session_state.patient_data['Date of Birth']}")

# --------- DASHBOARD ---------
def dashboard():
    st.title("🏠 Patient Dashboard")
    
    # Calories box (placeholder)
    st.metric(label="Recommended Calories", value="XXXX kcal")

    st.subheader("📊 Vitals")
    vitals = st.session_state.patient_data["Vitals History"]

    if vitals:
        df = pd.DataFrame(vitals)
        st.dataframe(df[::-1])  # show latest first
    else:
        st.info("No vitals data added yet.")

    st.subheader("➕ Add Vitals")
    with st.form("vitals_form"):
        height = st.text_input("Height (in cm)")
        weight = st.text_input("Weight (in kg)")
        heart_rate = st.text_input("Heart Rate (bpm)")
        bp = st.text_input("Blood Pressure (e.g., 120/80)")
        sugar = st.text_input("Blood Sugar (mg/dL)")
        submitted = st.form_submit_button("Save Vitals")

        if submitted:
            entry = {
                "Date & Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Height (cm)": height,
                "Weight (kg)": weight,
                "Heart Rate": heart_rate,
                "BP": bp,
                "Sugar": sugar
            }
            st.session_state.patient_data["Vitals History"].append(entry)
            st.success("Vitals saved successfully!")

# --------- REGISTRATION (ONLY FIRST TIME) ---------
def registration_page():
    st.title("📝 Register Patient Details")
    with st.form("register_form"):
        st.session_state.patient_data["First Name"] = st.text_input("First Name")
        st.session_state.patient_data["Middle Name"] = st.text_input("Middle Name")
        st.session_state.patient_data["Last Name"] = st.text_input("Last Name")
        st.session_state.patient_data["Date of Birth"] = st.date_input("Date of Birth").strftime("%Y-%m-%d")
        st.session_state.patient_data["Height (cm)"] = st.text_input("Height (in cm)")
        st.session_state.patient_data["Weight (kg)"] = st.text_input("Weight (in kg)")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Patient profile registered!")
            st.session_state["profile_done"] = True

# --------- APP FLOW ---------
if not st.session_state.logged_in:
    login_page()
else:
    profile_sidebar()
    if "profile_done" not in st.session_state:
        registration_page()
    else:
        dashboard()
