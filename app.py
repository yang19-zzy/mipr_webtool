import streamlit as st

from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import ClientSecretJWT

import requests

st.title("Database Access Demo")


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
            st.logout()


