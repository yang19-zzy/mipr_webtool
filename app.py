import streamlit as st
from streamlit.logger import get_logger
from streamlit.user_info import UserInfo
import requests

st.title("Database Access Demo")


pages = [
    st.Page("p0_home.py", title='home', icon="🏠"), 
    st.Page("p1_tracker.py", title='tracker', icon="🚨")
]

pg = st.navigation(pages)
pg.run()

st.write(st.session_state)
st.write(st.experimental_user)
st.write(UserInfo.values())

if not st.experimental_user.is_logged_in:
    with st.container():
        if st.button("Log in"):
            st.login()
            st.write(st.experimental_user)

            #add user login record to database
else:
    #if logged in, display content
    st.write(f"Logged in as {st.experimental_user.email}")
    st.write(f"User ID: {st.experimental_user.name}")

    with st.sidebar:
        st.title("Navigation")
        logout = st.button("Log out")
        if logout:
            st.logout()
