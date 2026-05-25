import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Admin Panel", page_icon="🛡️")

# 1. Security Check: Only show if logged in AND is admin
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Access Denied.")
    st.stop()

# 2. Check if the user has admin privileges
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
user = st.session_state.username
cursor.execute("SELECT is_admin FROM users WHERE username = ?", (user,))
is_admin = cursor.fetchone()[0]

if not is_admin:
    st.error("You do not have permission to view this page.")
    st.stop()

st.title("🛡️ Admin Control Center")

# 3. Fetch User List
st.subheader("Registered Users")
query = "SELECT id, username, is_admin FROM users"
df_users = pd.read_sql(query, conn)

# Display a nice table
st.dataframe(df_users, use_container_width=True)

# 4. Feature: Delete a User
st.subheader("Manage Users")
user_to_delete = st.selectbox("Select user to remove:", df_users['username'])
if st.button("Delete User", type="primary"):
    if user_to_delete == user:
        st.warning("You cannot delete your own admin account!")
    else:
        cursor.execute("DELETE FROM users WHERE username = ?", (user_to_delete,))
        conn.commit()
        st.success(f"User {user_to_delete} has been removed.")
        st.rerun()

conn.close()