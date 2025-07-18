import streamlit as st
import uuid
import json
import os

# File to store user data
DATA_FILE = "user_data.json"

# Load existing data or initialize
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {}

# Save function
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f)

# Generate unique ID
def generate_id():
    return str(uuid.uuid4())[:8]

# ----------------------------------------------
# App Layout
st.set_page_config(page_title="Health Dashboard", layout="centered")
st.title("🏥 Health App Dashboard")

role = st.radio("Who are you?", ["Patient", "Doctor"], horizontal=True)

# ----------------------------------------------
# PATIENT SECTION
if role == "Patient":
    menu = st.radio("Select Option", ["Register", "Login"])

    if menu == "Register":
        st.subheader("📝 New Patient Registration")
        name = st.text_input("Full Name")
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        age = st.number_input("Age", min_value=1, max_value=120)
        height = st.number_input("Height (in cm)", min_value=50.0, max_value=250.0)
        weight = st.number_input("Weight (in kg)", min_value=10.0, max_value=300.0)

        if st.button("Register"):
            if name and gender != "Select":
                bmi = round(weight / ((height / 100) ** 2), 2)
                status = ""
                if bmi < 18.5:
                    status = "Underweight"
                elif 18.5 <= bmi < 24.9:
                    status = "Normal"
                elif 25 <= bmi < 29.9:
                    status = "Overweight"
                else:
                    status = "Obese"

                uid = generate_id()
                user_data[uid] = {
                    "name": name,
                    "gender": gender,
                    "age": age,
                    "height": height,
                    "weight": weight,
                    "bmi": bmi,
                    "status": status
                }
                save_data()

                st.success(f"🎉 Registered successfully! Your Unique ID is: {uid}")
                st.info("Please save your ID to log in later.")

            else:
                st.warning("Please fill all details.")

    elif menu == "Login":
        st.subheader("🔐 Patient Login")
        uid = st.text_input("Enter your Unique ID")
        if st.button("Login"):
            if uid in user_data:
                user = user_data[uid]
                st.success(f"Welcome back, {user['name']}!")
                st.write(f"**Gender:** {user['gender']}")
                st.write(f"**Age:** {user['age']}")
                st.write(f"**Height:** {user['height']} cm")
                st.write(f"**Weight:** {user['weight']} kg")
                st.write(f"**BMI:** {user['bmi']} ({user['status']})")

                if user['status'] == "Overweight" or user['status'] == "Obese":
                    st.warning("⚠️ You may need to reduce your calorie intake.")
                elif user['status'] == "Underweight":
                    st.warning("⚠️ You may need to increase your calorie intake.")
                else:
                    st.success("✅ You are in a healthy range!")
            else:
                st.error("❌ ID not found. Please check and try again.")

# ----------------------------------------------
# DOCTOR SECTION
elif role == "Doctor":
    menu = st.radio("Select Option", ["Register", "View Patients"])

    if menu == "Register":
        st.subheader("👨‍⚕️ Doctor Registration")
        name = st.text_input("Doctor Name")
        specialization = st.text_input("Specialization")
        hospital = st.text_input("Hospital / Clinic Name")

        if st.button("Save Doctor Info"):
            st.success(f"Doctor {name} registered successfully.")
            st.info("Doctor module access is currently for viewing patient data only.")

    elif menu == "View Patients":
        st.subheader("📋 Patient Records")
        if user_data:
            for uid, user in user_data.items():
                with st.expander(f"{user['name']} (ID: {uid})"):
                    st.write(f"**Gender:** {user['gender']}")
                    st.write(f"**Age:** {user['age']}")
                    st.write(f"**Height:** {user['height']} cm")
                    st.write(f"**Weight:** {user['weight']} kg")
                    st.write(f"**BMI:** {user['bmi']} ({user['status']})")
        else:
            st.info("No patients registered yet.")
