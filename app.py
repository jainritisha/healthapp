import streamlit as st
import pandas as pd
import os
import uuid

st.set_page_config(page_title="Health App", layout="wide")

# File to store user data
USER_DATA_FILE = "user_data.csv"

# Initialize CSV
if not os.path.exists(USER_DATA_FILE):
    df = pd.DataFrame(columns=[
        "name", "email", "phone", "gender", "age", "height", "weight", "bmi", "user_id"
    ])
    df.to_csv(USER_DATA_FILE, index=False)

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def register_user():
    st.subheader("Register as a Patient")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    height = st.number_input("Height (in cm)", min_value=50.0, max_value=250.0)
    weight = st.number_input("Weight (in kg)", min_value=10.0, max_value=300.0)

    if st.button("Register"):
        if not name or not email or not phone:
            st.warning("Please fill all mandatory fields.")
        else:
            df = pd.read_csv(USER_DATA_FILE)
            if email in df["email"].values:
                st.error("Email already registered.")
            else:
                bmi = calculate_bmi(height, weight)
                user_id = str(uuid.uuid4())[:8]
                new_user = {
                    "name": name, "email": email, "phone": phone,
                    "gender": gender, "age": age, "height": height,
                    "weight": weight, "bmi": bmi, "user_id": user_id
                }
                df = df.append(new_user, ignore_index=True)
                df.to_csv(USER_DATA_FILE, index=False)
                st.success(f"Registered Successfully! Your User ID is: {user_id}")
                st.info("Now you can log in using your Name and Phone Number.")

def login_user():
    st.subheader("Login")
    name = st.text_input("Enter your name")
    phone = st.text_input("Enter your phone number")

    if st.button("Login"):
        df = pd.read_csv(USER_DATA_FILE)
        user = df[(df["name"] == name) & (df["phone"] == phone)]

        if not user.empty:
            user = user.iloc[0]
            st.success(f"Welcome, {user['name']}!")
            display_dashboard(user)
        else:
            st.error("No matching user found. Please check your credentials.")

def display_dashboard(user):
    st.markdown("### 🧾 Patient Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Gender:** {user['gender']}")
        st.write(f"**Age:** {user['age']}")
        st.write(f"**Phone:** {user['phone']}")

    with col2:
        st.write(f"**Height:** {user['height']} cm")
        st.write(f"**Weight:** {user['weight']} kg")
        st.write(f"**BMI:** {user['bmi']}")
        bmi = user['bmi']
        if bmi < 18.5:
            st.warning("You are underweight. Increase calorie intake.")
        elif bmi > 24.9:
            st.warning("You are overweight. Reduce calorie intake.")
        else:
            st.success("Your BMI is in a healthy range.")

    st.markdown("---")
    st.markdown("### 📁 Upload Prescription or Medical Report")

    uploaded_file = st.file_uploader("Upload Medical File (PDF/IMG)", type=['pdf', 'png', 'jpg', 'jpeg'])

    if uploaded_file:
        st.success("File uploaded successfully.")
        # Placeholder for analysis
        st.info("We will analyze your report soon...")

# Streamlit layout
st.title("🏥 Health App Portal")

menu = st.sidebar.selectbox("Choose an option", ["Register", "Login"])

if menu == "Register":
    register_user()
elif menu == "Login":
    login_user()

st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True
)
