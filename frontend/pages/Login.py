import streamlit as st
import requests

st.title("Login to Assignment Task Tracker")
st.markdown("### Enter your credentials to access your tasks")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if not email or not password:
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Logging in..."):
            response = requests.post("http://localhost:8000/api/auth/login", json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data["access_token"]
                st.success("Login successful!")
                st.switch_page("pages/Tasks.py")
            else:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"Login failed: {error_detail}")
                except:
                    st.error(f"Login failed: Status code {response.status_code}")

if st.button("Go to Register"):
    st.switch_page("pages/Register.py")
