import streamlit as st
st.set_page_config(layout='wide')

# ----------------------
# Configuration
# ----------------------
import time
from consts import *
from funcs import *

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

# st.session_state.session_start_time = time.time()

# ----------------------
# Authentication
# ----------------------
if st.experimental_user.is_logged_in:
    WHITELIST = get_secret()
    LOGGED_IN_USER = st.experimental_user.email.split("@")[0] if st.experimental_user.is_logged_in else ""
    AUTHORISED_USER = LOGGED_IN_USER in WHITELIST
    st.session_state.authorised_user = AUTHORISED_USER
    st.session_state.logged_in_user = LOGGED_IN_USER
    st.session_state.session_start_time = time.time() if "session_start_time" not in st.session_state else st.session_state.session_start_time

# ----------------------
# Streamlit Page Configuration
# ----------------------
st.title("Database Access Webtool Demo")


# ----------------------
# Tools
# ----------------------


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
        ##### debug usage below #####
        st.markdown("### User Information")
        st.write(f"User ID: {LOGGED_IN_USER}")
        st.write(f"User Email: {st.experimental_user.email}")
        st.write(f"User Role: {st.session_state.authorised_user}")
        st.write(f"Session Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.session_state.session_start_time))}")
        # st.write_stream(f"Session Duration: {time.strftime('%H:%M:%S', time.gmtime(time.time() - st.session_state.session_start_time))}")
        # st.metric(label="Session Duration", value=time.strftime('%H:%M:%S', time.gmtime(time.time() - st.session_state.session_start_time)), delta=None, delta_color="normal")
        with st.container():
            clock = st.empty()
            # for secs in range(SESSION_TIMEOUT, 0, -1):
            #     minutes, seconds = divmod(secs, 60)
            #     clock.metric("Session will expire in", f"{int(minutes)}:{int(seconds):02d} minutes")
            #     time.sleep(1)
            # st.divider()
            # live_session_countdown(clock)
        ##### debug usage above #####

        st.markdown("### Admin Panel")
        if st.button("Log out"):
            st.session_state.clear()
            st.cache_data.clear()
            st.cache_resource.clear()
            st.logout()

elif not st.experimental_user.is_logged_in:
    st.write(APP_DESCRIPTION)
    if st.button("Log in"):
        st.login()

else:
    st.warning("You are not authorized to access this app. Please contact the admin.")
    st.stop()
