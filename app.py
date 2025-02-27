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

st.write(st.query_params)

state = None
code = None
scope = None
authuser = None
hd = None
prompt = None
user_id, user_email = None, None
client = OAuth2Session(
    client_id=st.secrets['auth']['client_id'],
    client_secret=st.secrets['auth']['client_secret'],
    scope=st.secrets['auth']['scope'],
    redirect_uri=st.secrets['auth']['redirect_uri'],
    token_endpoint_auth_method='client_secret_post'
)


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
    st.query_params['code']
except KeyError:
    st.query_params['code'] = None

if not st.query_params['code']:
    with st.container():
        if st.button("Log in"):
            st.login()
            # st.write(st.experimental_user)

            #add user login record to database
             
else:
    #if logged in, display content
    

    state = st.query_params['state']
    code = st.query_params['code']
    scope = st.query_params['scope']
    authuser = st.query_params['authuser']
    hd = st.query_params['hd']
    prompt = st.query_params['prompt'] 

    client = OAuth2Session(
        client_id=st.secrets['auth']['client_id'],
        client_secret=st.secrets['auth']['client_secret'],
        scope=st.secrets['auth']['scope'],
        redirect_uri=st.secrets['auth']['redirect_uri'],
        token_endpoint_auth_method='client_secret_post'
    )
    user_id, user_email = client.get_id_email(code)
    st.experimental_user.email = user_email
    st.experimental_user.name = user_id


    st.write(f"Logged in as {st.experimental_user.email}")
    st.write(f"User ID: {st.experimental_user.name}")


    
    with st.sidebar:
        st.title("Navigation")
        logout = st.button("Log out")
        if logout:
            st.logout()
