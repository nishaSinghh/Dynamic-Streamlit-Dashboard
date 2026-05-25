import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Admin Panel", page_icon="🛡️")

# 1. Connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# 2. Security Check: Ensure column exists before checking admin status
try:
    cursor.execute("SELECT is_admin FROM users LIMIT 1")
except sqlite3.OperationalError:
    # If column is missing, create it immediately
    cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
    cursor.execute("UPDATE users SET is_admin = 1 WHERE username = 'nisha'")
    conn.commit()

# 3. Access Control
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Access Denied. Please log in.")
    st.stop()

user = st.session_state.username
cursor.execute("SELECT is_admin FROM users WHERE username = ?", (user,))
res = cursor.fetchone()
is_admin = res[0] if res else 0

if not is_admin:
    st.error("You do not have permission to view this page.")
    st.stop()

st.title("🛡️ Admin Control Center")

# 4. Fetch User List (Safe Query)
st.subheader("Registered Users")
try:
    df_users = pd.read_sql("SELECT id, username, is_admin FROM users", conn)
except Exception:
    # Fallback if 'id' column is also missing in older versions
    df_users = pd.read_sql("SELECT username, is_admin FROM users", conn)

st.dataframe(df_users, use_container_width=True)

# 5. Management UI
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