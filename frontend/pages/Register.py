import streamlit as st
import requests

st.title("Register for Assignment Task Tracker")
st.markdown("### Create an account to start managing your tasks")

email = st.text_input("Email")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if not email or not username or not password:
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Registering..."):
            response = requests.post("http://localhost:8000/api/auth/register", json={"email": email, "username": username, "password": password})
            if response.status_code == 200:
                st.success("Registration successful! Please login.")
                st.switch_page("pages/Login.py")
            else:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"Registration failed: {error_detail}")
                except:
                    st.error(f"Registration failed: Status code {response.status_code}")

if st.button("Go to Login"):
    st.switch_page("pages/Login.py")
