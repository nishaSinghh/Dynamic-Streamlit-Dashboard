import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Admin Panel", page_icon="🛡️", layout="wide")

# 1. Database Connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# 2. Security Check (Invisible Protection)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("main.py")
    st.stop()

    # Check if logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first from the Home page.")
    if st.button("Go to Login"):
        st.switch_page("main.py")
    st.stop()

# Verify Admin Status
user = st.session_state.username
cursor.execute("SELECT is_admin FROM users WHERE username = ?", (user,))
res = cursor.fetchone()
is_admin = res[0] if res else 0

if not is_admin:
    st.error("Access Denied: Admin privileges required.")
    st.stop()

st.title("🛡️ Admin Control Center")
st.markdown("---")

# 3. User Overview Table
st.subheader("👥 All Registered Users")
df_users = pd.read_sql("SELECT username, is_admin FROM users", conn)

# Make the table look cleaner
df_users['Role'] = df_users['is_admin'].apply(lambda x: "⭐ Admin" if x == 1 else "👤 User")
st.dataframe(df_users[['username', 'Role']], use_container_width=True)

st.markdown("---")

# 4. Management Section (Columns for better layout)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Promote to Admin")
    # Only show users who are NOT admins yet
    regular_users = df_users[df_users['is_admin'] == 0]['username'].tolist()
    
    if regular_users:
        user_to_promote = st.selectbox("Select user to promote:", regular_users)
        if st.button("Grant Admin Status", use_container_width=True):
            cursor.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (user_to_promote,))
            conn.commit()
            st.success(f"Success! {user_to_promote} is now an Admin.")
            st.rerun()
    else:
        st.info("No regular users available to promote.")

with col2:
    st.subheader("🗑️ Remove User")
    all_users = df_users['username'].tolist()
    user_to_delete = st.selectbox("Select user to delete:", all_users)
    
    if st.button("Permanently Delete", type="primary", use_container_width=True):
        if user_to_delete == user:
            st.warning("Safety Lock: You cannot delete your own account.")
        else:
            cursor.execute("DELETE FROM users WHERE username = ?", (user_to_delete,))
            conn.commit()
            st.success(f"User {user_to_delete} removed from database.")
            st.rerun()

conn.close()