import streamlit as st
import os
import json
import uuid

# Page setup
st.set_page_config(page_title="Health Repository", layout="centered")
st.markdown("<h1 style='text-align: center; color: black;'>🩺 Health Repository</h1>", unsafe_allow_html=True)

# Ensure users database exists
users_db = "users.json"
if not os.path.exists(users_db):
    with open(users_db, "w") as f:
        json.dump({}, f)

# Helper functions
def load_users():
    with open(users_db, "r") as f:
        return json.load(f)

def save_users(users):
    with open(users_db, "w") as f:
        json.dump(users, f, indent=4)

def register_user(name, phone, email, gender, age, height, weight):
    users = load_users()
    if email in users:
        return False, "❌ Email already registered!"
    user_id = str(uuid.uuid4())[:8]
    users[email] = {
        "user_id": user_id,
        "name": name,
        "phone": phone,
        "email": email,
        "gender": gender,
        "age": age,
        "height": height,
        "weight": weight,
        "bmi": calculate_bmi(height, weight),
        "files": []
    }
    save_users(users)
    return True, user_id

def login_user(name, phone):
    users = load_users()
    for email, info in users.items():
        if info["name"] == name and info["phone"] == phone:
            return True, info
    return False, None

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)

# Main interface
menu = st.sidebar.selectbox("Choose Option", ["Register", "Login"])

if menu == "Register":
    st.subheader("📋 Register as a Patient")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=0)
    height = st.number_input("Height (in cm)", min_value=0.0)
    weight = st.number_input("Weight (in kg)", min_value=0.0)

    if st.button("Register"):
        if name and phone and email:
            success, msg = register_user(name, phone, email, gender, age, height, weight)
            if success:
                st.success(f"✅ Registered successfully! Your User ID is: {msg}")
            else:
                st.error(msg)
        else:
            st.warning("⚠️ Please fill all details.")

elif menu == "Login":
    st.subheader("🔐 Patient Login")

    name = st.text_input("Enter your name")
    phone = st.text_input("Enter your phone number")

    if st.button("Login"):
        success, user_info = login_user(name, phone)
        if success:
            st.success(f"✅ Welcome back, {user_info['name']}!")
            st.markdown("---")
            st.markdown("## 🧾 Patient Dashboard")
            st.write(f"**Name**: {user_info['name']}")
            st.write(f"**Email**: {user_info['email']}")
            st.write(f"**Gender**: {user_info['gender']}")
            st.write(f"**Age**: {user_info['age']}")
            st.write(f"**Height**: {user_info['height']} cm")
            st.write(f"**Weight**: {user_info['weight']} kg")
            st.write(f"**BMI**: {user_info['bmi']}")

            # Calorie recommendation
            if user_info['bmi'] > 25:
                st.warning("⚠️ Your BMI indicates overweight. Consider reducing ~500 calories/day.")
            elif user_info['bmi'] < 18.5:
                st.warning("⚠️ You are underweight. Consider consulting a nutritionist.")
            else:
                st.success("✅ Your BMI is in the normal range.")

            st.markdown("### 📁 Upload Medical Files (Reports or Prescriptions)")
            uploaded = st.file_uploader("Upload a file", type=["pdf", "jpg", "png"])
            if uploaded:
                upload_dir = "uploaded_files"
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, uploaded.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded.read())
                st.success(f"✅ File {uploaded.name} uploaded successfully!")

                # Update user info
                users = load_users()
                users[user_info['email']]['files'].append(uploaded.name)
                save_users(users)

        else:
            st.error("❌ Login failed! Check your name and phone number.")

# Footer
st.markdown("<br><hr style='border:1px solid #eee'><div style='text-align:center;'>© 2025 Health Repository</div>", unsafe_allow_html=True)
