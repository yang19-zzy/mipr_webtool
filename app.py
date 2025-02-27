import streamlit as st

from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import ClientSecretJWT

import requests

st.title("Database Access Demo")



# st.secrets['auth']['redirect_uri']
# st.secrets['auth']['client_id']
# st.secrets['auth']['client_secret']
# st.secrets['auth']['token_url']
# st.secrets['auth']['scope']

st.write('query-params', st.query_params)
st.write('session-state', st.session_state)
st.write('secrets', st.secrets)
st.write('experimental_user', st.experimental_user)

state = None
code = None
scope = None
authuser = None
hd = None
prompt = None
user_id, user_email = None, None







pages = [
    st.Page("p0_home.py", title='home', icon="🏠"), 
    st.Page("p1_tracker.py", title='tracker', icon="🚨")
]

pg = st.navigation(pages)
pg.run()

st.write(st.session_state)
# st.write(st.experimental_user)
# st.write(UserInfo.values())

try:
    code = st.query_params['code']
    state = st.query_params['state']
    scope = st.query_params['scope']
    authuser = st.query_params['authuser']
    hd = st.query_params['hd']
    prompt = st.query_params['prompt']

    st.write('logged in', st.query_params)
    st.write('experimental user', st.experimental_user)

    client = OAuth2Session(
        client_id=st.secrets['auth']['client_id'], 
        client_secret=st.secrets['auth']['client_secret'], 
        scope=scope
    )
    token = client.fetch_access_token(url=st.secrets['auth']['redirect_uri'], code=code)
    st.write('token', token)
    user_id, user_email = client.get_id_email(token['access_token'])
    st.experimental_user.email = user_email
    st.experimental_user.user_id = user_id

    st.write(f"Logged in as {st.experimental_user.email}")
    st.write(f"User ID: {st.experimental_user.name}")

    with st.sidebar:
        st.title("Navigation")
        logout = st.button("Log out")
        if logout:
            st.logout()

except KeyError:
    with st.container():
        if st.button("Log in"):
            st.login()
