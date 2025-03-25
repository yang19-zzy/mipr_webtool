import streamlit as st
import time

SESSION_TIMEOUT = 60 # 30 minutes

if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = time.time()

if time.time() - st.session_state.session_start_time > SESSION_TIMEOUT:
    st.warning("Session timed out. Please log in again.")
    st.logout()



st.title("Database Access Demo")
st.session_state.session_start_time = time.time()




if st.experimental_user.is_logged_in:
    col1, col2 =  st.columns(2)
    with col1:
        st.write(f"Logged in as {st.experimental_user.email}")
    with col2:
        st.write(f"User ID: {st.experimental_user.name}")
st.divider()

pages = [
    st.Page("p0_home.py", title='Home', icon="🏠"), 
    st.Page("p1_tracker.py", title='Test Tracker', icon="👣"),
    st.Page("p2_data_gui.py", title='Data Puller', icon="🗄️")
]

pg = st.navigation(pages)
pg.run()


if not st.experimental_user.is_logged_in:
     with st.container():
        if st.button("Log in"):
            st.login()
else:
    with st.sidebar:
        st.title("Navigation")
        logout = st.button("Log out")
        if logout:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.logout()


