import re
import streamlit as st
import random
import string
import requests
import hashlib
import qrcode
from io import BytesIO
from PIL import Image

# Check if password is in a data breach
def check_password_breach(password):
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    sha1_prefix, sha1_suffix = sha1_password[:5], sha1_password[5:]
    
    response = requests.get(f"https://api.pwnedpasswords.com/range/{sha1_prefix}")
    if sha1_suffix in response.text:
        return True
    return False

# Password Strength Checker
def check_password_strength(password):
    score = 0
    feedback = []

    if check_password_breach(password):
        feedback.append("❌ Your password was found in a data breach! Choose another one.")
        return 0, feedback

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Use both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*()_+{}|:<>?]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    return score, feedback

# Strong Password Generator
def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+{}|:<>?"
    return "".join(random.choice(chars) for _ in range(length))

# Generate a Secure 2FA Code
def generate_2fa_code():
    return random.randint(100000, 999999)

# Generate MFA QR Code
def generate_qr_code(secret):
    qr = qrcode.make(f"otpauth://totp/YourApp?secret={secret}")
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Streamlit UI
st.set_page_config(page_title="🔐 Password Security Checker", layout="centered")

st.title("🔐 Password Security App")
st.write("Check your password strength & security in real-time!")

# Password Input with Strength Analysis
password = st.text_input("Enter your password:", type="password")

if password:
    score, feedback = check_password_strength(password)
    
    if score >= 5:
        st.success("✅ Ultra Secure Password!")
    elif score == 4:
        st.success("✅ Strong Password!")
    elif score == 3:
        st.warning("⚠️ Moderate Password - Consider improving it.")
    else:
        st.error("❌ Weak Password! Improve using these tips:")
        for msg in feedback:
            st.write(msg)

    st.progress(score / 5)

# Password Generator
st.subheader("🔑 Generate a Strong Password")
length = st.slider("Password Length", 8, 32, 16)
if st.button("Generate Password"):
    strong_password = generate_strong_password(length)
    st.code(strong_password, language="")

# 2FA Code Generator
st.subheader("🔓 Generate a Secure 2FA Code")
if st.button("Generate 2FA Code"):
    st.success(f"Your 2FA Code: {generate_2fa_code()}")

# QR Code for MFA
st.subheader("🔐 Generate QR Code for MFA")
mfa_secret = "JBSWY3DPEHPK3PXP"
if st.button("Generate MFA QR Code"):
    qr_image = generate_qr_code(mfa_secret)
    st.image(qr_image, caption="Scan this QR Code with your authenticator app.")
