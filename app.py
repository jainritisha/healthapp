import streamlit as st
import uuid
import base64
import os

st.set_page_config(page_title="Health App", layout="wide")

# Store user data
users = {}
uploaded_reports = {}

# App styling
def local_css():
    st.markdown("""
        <style>
            .reportview-container {
                background: white;
            }
            .main {
                background: white;
            }
            .block-container {
                padding: 2rem;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 24px;
            }
        </style>
    """, unsafe_allow_html=True)

local_css()

# Function to generate unique ID
def generate_user_id():
    return str(uuid.uuid4())[:8]

# Dashboard view
def show_dashboard(user_id):
    user = users[user_id]
    st.markdown(f"## Welcome, {user['name']} 👋")
    st.markdown(f"### Your Health Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Gender:** {user['gender']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Phone:** {user['phone']}")
        st.write(f"**Age:** {user['age']}")
    with col2:
        st.write(f"**Weight (kg):** {user['weight']}")
        st.write(f"**Height (cm):** {user['height']}")
        bmi = round(user['weight'] / ((user['height'] / 100) ** 2), 2)
        st.write(f"**BMI:** {bmi}")
        if bmi > 25:
            st.error("You need to reduce weight. Suggested calorie control.")
        elif bmi < 18.5:
            st.warning("You are underweight. Consider a balanced diet.")
        else:
            st.success("You have a healthy BMI!")

    st.markdown("---")
    st.subheader("Upload Reports / Prescriptions")
    uploaded_file = st.file_uploader("Choose a PDF or text file", type=['pdf', 'txt'])

    if uploaded_file:
        content = uploaded_file.read()
        try:
            content = content.decode('utf-8')
        except:
            content = "Unable to read file."
        st.write("**File Content:**")
        st.text_area("Report Preview", value=content, height=200)
        uploaded_reports[user_id] = content

        # Basic analysis
        if "blood sugar" in content.lower():
            st.info("⚠️ Blood Sugar mentioned. Schedule a diabetes checkup.")
        elif "cholesterol" in content.lower():
            st.info("⚠️ Cholesterol levels mentioned. Schedule lipid profile.")
        else:
            st.success("✅ Report looks fine. Keep uploading for regular checkups.")

# Registration
def register(role):
    st.title(f"{role} Registration")
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    age = st.number_input("Age", min_value=0, max_value=120)
    weight = st.number_input("Weight (in kg)", min_value=0.0)
    height = st.number_input("Height (in cm)", min_value=0.0)

    if st.button("Register"):
        if not all([name, email, phone, age, weight, height]):
            st.warning("Please fill in all fields.")
        else:
            user_id = generate_user_id()
            users[user_id] = {
                "name": name,
                "gender": gender,
                "email": email,
                "phone": phone,
                "age": age,
                "weight": weight,
                "height": height,
                "role": role
            }
            st.success(f"Registered successfully! Your User ID is `{user_id}`")
            st.info("Please copy your ID to log in next time.")

# Login
def login():
    st.title("User Login")
    user_id = st.text_input("Enter your Unique ID")

    if st.button("Login"):
        if user_id in users:
            st.success("Login successful!")
            show_dashboard(user_id)
        else:
            st.error("User ID not found. Please register first.")

# Home
def home():
    st.title("🏥 Health Assistant App")
    st.subheader("Choose your role:")
    option = st.selectbox("Are you a...", ["Patient", "Doctor"])
    action = st.radio("Choose action:", ["Register", "Login"])

    if action == "Register":
        register(option)
    else:
        login()

home()
