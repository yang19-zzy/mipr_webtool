import time
import boto3
from botocore.exceptions import ClientError
import streamlit as st
import json
from consts import *
from funcs import *

# ----------------------
# Configuration
# ----------------------
st.set_page_config(layout='wide')

# ----------------------
# Functions - imported from funcs.py
# ----------------------


# ----------------------
# Session Management
# ----------------------
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = time.time()

if time.time() - st.session_state.session_start_time > SESSION_TIMEOUT:
    st.warning("Session timed out. Please log in again.")
    time.sleep(1)
    st.cache_data.clear()
    st.session_state.clear()
    st.logout()

st.session_state.session_start_time = time.time()

# ----------------------
# Authentication
# ----------------------
if st.experimental_user.is_logged_in:
    WHITELIST = get_secret()
    LOGGED_IN_USER = st.experimental_user.email.split("@")[0] if st.experimental_user.is_logged_in else ""
    AUTHORISED_USER = LOGGED_IN_USER in WHITELIST
    st.session_state.authorised_user = AUTHORISED_USER
    st.session_state.logged_in_user = LOGGED_IN_USER

# ----------------------
# Streamlit Page Configuration
# ----------------------
st.title("Database Access Webtool Demo")

# ----------------------
# UI Rendering
# ----------------------
if st.experimental_user.is_logged_in and AUTHORISED_USER:
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Logged in as {st.experimental_user.email}")
    with col2:
        st.write(f"User ID: {LOGGED_IN_USER}")
    st.divider()

    pages = [
        st.Page("p0_home.py", title='Home', icon="🏠"),
        st.Page("p1_tracker.py", title='Test Tracker', icon="👣", ),
        st.Page("p2_data_puller.py", title='Data Puller', icon="🗄️"),
        st.Page("p3_data_vis.py", title='Data Visualizer', icon="📊"),
    ]
    pg = st.navigation(pages)
    pg.run()

    with st.sidebar:
        st.title("Navigation")
        if st.button("Log out"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.logout()

elif not st.experimental_user.is_logged_in:
    st.write("""
This is a demo of a Streamlit app that allows users to log in and access a database.

The app is divided into two sections:
- Test Tracker / File Submission Tracker
- Database Acess
- Data Visualization
""")
    with st.container():
        if st.button("Log in"):
            st.login()

else:
    st.warning("You are not authorized to access this app. Please contact the admin.")
    st.stop()
