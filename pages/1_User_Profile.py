import streamlit as st
import sqlite3
import pandas as pd

# Page Config
st.set_page_config(page_title="User Profile", page_icon="👤")

# Check if logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first from the Home page.")
    if st.button("Go to Login"):
        st.switch_page("main.py")
    st.stop()

# Database Connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Get Current User Info (Assuming you store username in session_state during login)
# Note: You'll need to update login() in main.py to set st.session_state.username = username
current_user = st.session_state.get("username", "User")

st.title(f"👤 Welcome, {current_user}!")

# Simple Profile UI
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://www.w3schools.com/howto/img_avatar.png", width=150) # Placeholder avatar

with col2:
    st.subheader("Account Details")
    st.info(f"**Username:** {current_user}")
    st.write("**Account Type:** Developer/Admin")
    
# Change Password Feature
with st.expander("🔐 Change Password"):
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm New Password", type="password")
    
    if st.button("Update Password"):
        if new_pass == confirm_pass and new_pass != "":
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_pass, current_user))
            conn.commit()
            st.success("Password updated successfully!")
        else:
            st.error("Passwords do not match.")

conn.close()