import streamlit as st
import requests



def pop_tracker_status():
    st.toast('''Form submitted!''', icon='🎉')

    #TODO: add code to save tracker data to database (s3 bucket)


if st.query_params['code'] != 'None':
    with st.container():
        st.header('Test Tracker')
        owner = st.empty()
        date = st.empty()
        st.session_state.submit_owner = owner.text_input(label='Enter your name:', key='owner_submit')
        st.session_state.submit_date = date.date_input(label='Test date:', key='date_submit')
        submit_button = st.button(label='Submit', on_click=pop_tracker_status, help='Submit the form')
            


        clear_form = st.button('Clear form')
        if clear_form:
            st.session_state.form_submitted = False
            st.session_state.submit_owner = owner.text_input(label='Enter your name:', value='', key='owner_clear')
            st.session_state.submit_date = date.date_input(label='Test date:', key='date_clear')
else:
    st.write("Please log in")

            #add user login record to database
