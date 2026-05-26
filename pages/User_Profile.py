import streamlit as st
import sqlite3
from PIL import Image
import io

# Database connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

st.title("👤 User Profile")

if st.session_state.logged_in:
    user = st.session_state.username
    st.subheader(f"Welcome, {user}!")

    # --- UPLOAD SECTION ---
    uploaded_file = st.file_uploader("Choose a profile picture", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # Image ko display karein
        img = Image.open(uploaded_file)
        st.image(img, width=150, caption="Preview")

        if st.button("Save Profile Picture"):
            # Image ko binary format mein convert karein
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            img_blob = img_byte_arr.getvalue()

            # Database mein save karein
            cursor.execute("UPDATE users SET profile_pic = ? WHERE username = ?", (img_blob, user))
            conn.commit()
            st.success("Profile picture updated successfully!")
            st.rerun()

    # --- DISPLAY SECTION ---
    cursor.execute("SELECT profile_pic FROM users WHERE username = ?", (user,))
    data = cursor.fetchone()
    
    if data and data[0]:
        st.markdown("### Your Current Photo")
        st.image(data[0], width=150)
    else:
        st.info("No profile picture uploaded yet.")
else:
    st.warning("Please login first.")