import streamlit as st
import os
from supabase import create_client, Client

# ================= DATABASE INITIALIZATION (SUPABASE) =================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# ================= PAGE CONFIG =================
# Must stay at the top before rendering any UI!
st.set_page_config(
    page_title="Login | Sales Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= HIDE STREAMLIT UI & CUSTOM CSS =================
st.markdown("""
<style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    [data-testid="stSidebar"] {display:none;}
    
    /* Smooth transitions for the login card */
    .login-card {
        transition: transform 0.3s ease;
    }
    .login-card:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# Load External CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.info("Custom CSS file not found, using default styles.")

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# ================= FUNCTIONS =================
def signup():
    st.subheader("Create Account")
    
    # Names Row
    col1, col2 = st.columns(2)
    with col1:
        f_name = st.text_input("First Name", placeholder="Nisha", key="signup_fname")
    with col2:
        l_name = st.text_input("Last Name", placeholder="Singh", key="signup_lname")
        
    # Email and Password
    email = st.text_input("Email Address", placeholder="example@mail.com", key="signup_email")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        new_password = st.text_input("Password", type="password", placeholder="••••••••", key="signup_pass")
    with p_col2:
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_confirm")
    
    if st.button("Create Account", use_container_width=True):
        if not (f_name and l_name and email and new_password and confirm_password):
            st.warning("⚠️ Please fill all fields")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match!")
        else:
            try:
                # Data dictionary
                user_data = {
                    "username": email, 
                    "password": new_password,
                    "first_name": f_name,
                    "last_name": l_name
                }
                # Supabase Execution
                response = supabase.table("users").insert(user_data).execute()
                
                # Check if insert was successful
                if response:
                    st.success("✅ Account Created! Now please login.")
                    st.balloons()
            except Exception as e:
                # Yeh line humein asli wajah batayegi (Policy error, Table error, etc.)
                st.error(f"❌ Backend Error: {e}")
def login():
    st.subheader("Welcome Back")
    email = st.text_input("Email Address", placeholder="Enter email", key="login_user")
    password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
    
    if st.button("Login", use_container_width=True):
        if email and password:
            try:
                response = supabase.table("users").select("*").eq("username", email).eq("password", password).execute()
                
                if response.data:
                    user_info = response.data[0]
                    st.session_state.logged_in = True
                    st.session_state.username = user_info['first_name'] # Stores first name for dashboard welcome panel
                    st.success(f"Logged in as {user_info['first_name']}")
                    st.rerun()
                else:
                    st.error("Invalid Email or Password")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please fill all fields")

# ================= MAIN UI LOGIC =================
if st.session_state.logged_in:
    st.switch_page("pages/dashboard.py")
else:
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown(f"""
            <div class="left-side">
                <h1 class="main-title">Sales Analytics <br>Dashboard</h1>
                <p class="sub-title">Actionable insights for your business growth.</p>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="logo-circle">⚡</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Signup"])
        with tab1:
            login()
        with tab2:
            signup()

        st.markdown("""
            <div class="google-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="20">
                Continue with Google
            </div>
            <div class="footer-text">
                Secure • Enterprise Grade • Reliable
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) 
    st.markdown('</div>', unsafe_allow_html=True)