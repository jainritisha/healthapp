import streamlit as st
import json
import os
from PIL import Image
import pytesseract

# Initialize or load user data
USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def health_advice(bmi):
    if bmi < 18.5:
        return "You are underweight. Consider a nutritious diet plan."
    elif 18.5 <= bmi < 24.9:
        return "You have a healthy weight. Keep it up!"
    elif 25 <= bmi < 29.9:
        return "You are overweight. A weight loss plan is advised."
    else:
        return "You are obese. Consult a doctor for weight management."

# Streamlit Config
st.set_page_config(page_title="Health Repository", layout="centered")

# Styling
st.markdown("""
    <style>
    body {
        background-color: white;
        color: black;
    }
    .stTextInput > div > div > input {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Health Repository")

# Load user data
users = load_users()

menu = st.sidebar.radio("Navigation", ["Register", "Login"])

if menu == "Register":
    st.subheader("🔐 Register")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
    age = st.number_input("Age", min_value=0, max_value=120)
    height = st.number_input("Height (in cm)")
    weight = st.number_input("Weight (in kg)")
    
    if st.button("Register"):
        if email in users:
            st.error("Email already registered.")
        else:
            bmi = calculate_bmi(weight, height)
            users[email] = {
                "name": name,
                "phone": phone,
                "gender": gender,
                "age": age,
                "height": height,
                "weight": weight,
                "bmi": bmi
            }
            save_users(users)
            st.success(f"Registered successfully! Your BMI is {bmi}.")

elif menu == "Login":
    st.subheader("🔓 Login")
    login_name = st.text_input("Full Name")
    login_phone = st.text_input("Phone Number")

    if st.button("Login"):
        found_user = None
        for email, data in users.items():
            if data["name"] == login_name and data["phone"] == login_phone:
                found_user = data
                break

        if found_user:
            st.success(f"Welcome back, {found_user['name']}!")
            st.header("🧾 Dashboard")
            st.markdown(f"""
            - **Name**: {found_user['name']}
            - **Email**: {email}
            - **Phone**: {found_user['phone']}
            - **Gender**: {found_user['gender']}
            - **Age**: {found_user['age']}
            - **Height**: {found_user['height']} cm
            - **Weight**: {found_user['weight']} kg
            - **BMI**: {found_user['bmi']}
            """)
            st.info(health_advice(found_user['bmi']))

            st.markdown("### 📁 Upload Medical Report/Prescription")
            uploaded_file = st.file_uploader("Upload a PDF/Image file", type=["pdf", "png", "jpg", "jpeg"])

            if uploaded_file is not None:
                st.success("File uploaded successfully.")
                file_bytes = uploaded_file.read()
                
                if uploaded_file.type.startswith("image"):
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Report", use_column_width=True)
                    text = pytesseract.image_to_string(image)
                    st.markdown("**Extracted Text:**")
                    st.text(text)
                else:
                    st.warning("PDF support is limited. Please upload an image for OCR text extraction.")
        else:
            st.error("Invalid name or phone number.")
