import streamlit as st
import requests



def pop_tracker_status():
    st.toast('''Form submitted!''', icon='🎉')

    #TODO: add code to save tracker data to database (s3 bucket)

def clear_form():
    st.session_state.form_submitted = False
    st.session_state.submit_owner = st.experimental_user.name
    st.session_state.submit_date = None
    st.session_state.submit_subid = ''
    st.session_state.submit_testid = ''
    st.session_state.submit_testtype = ''
    st.session_state.submit_visitnum = ''
    st.session_state.submit_aw = ''
    st.session_state.submit_awmetadata = ''
    st.session_state.submit_gar = ''
    st.session_state.submit_garmetadata = ''
    st.session_state.submit_gw = ''
    st.session_state.submit_gwmetadata = ''
    st.session_state.submit_notes = ''
    


if st.experimental_user.is_logged_in:
    with st.container(height=500, border=True, key="test_tracker"):
        st.header('Test Tracker')
        
        #tracked variables
        owner = st.empty()
        date = st.empty()
        subid = st.empty()
        testid = st.empty()
        testtype = st.empty() #dropdown: cosmedcpet-interval, cosmedcpet-cycle, dexa, inbody, etc.
        visitnum = st.empty() #dropdown: 1, 2, 3, etc. indicating which visit number this participant is on
        aw = st.empty() #applewatch worn? yes/no
        awmetadata = st.empty() #TODO: clarify what metadata is needed
        gar = st.empty() #garmin worn? yes/no
        garmetadata = st.empty() #TODO: clarify what metadata is needed
        gw = st.empty() #galacywatch worn? yes/no
        gwmetadata = st.empty() #TODO: clarify what metadata is needed
        notes = st.empty() #text input for notes
        

        


        owner.text_input(label='Who is filling this form:', value=st.experimental_user.name,  key='submit_owner', disabled=True)
        subid.text_input(label='Subject ID:', key='submit_subid')
        date.date_input(label='Test date:', value=None, key='submit_date')
        testid.text_input(label='Test ID:', key='submit_testid')
        testtype.selectbox('Test type:', options=['', 'cosmedcpet-interval', 'cosmedcpet-cycle', 'dexa', 'inbody', 'other'], key='submit_testtype')
        visitnum.selectbox('Visit number:', options=[''] + [str(i) for i in range(1, 11)], key='submit_visitnum')
        aw.selectbox('Apple Watch worn?', options=['', 'yes', 'no'], key='submit_aw')
        awmetadata.text_input(label='Apple Watch metadata:', key='submit_awmetadata')
        gar.selectbox('Garmin worn?', options=['', 'yes', 'no'], key='submit_gar')
        garmetadata.text_input(label='Garmin metadata:', key='submit_garmetadata')
        gw.selectbox('Galaxy Watch worn?', options=['', 'yes', 'no'], key='submit_gw')
        gwmetadata.text_input(label='Galaxy Watch metadata:', key='submit_gwmetadata')
        notes.text_area(label='Notes:', key='submit_notes')
        # st.session_state.form_submitted = False
        




        submit_button = st.button(label='Submit', on_click=pop_tracker_status, help='Submit the form')
        clear_button = st.button('Clear form', on_click=clear_form, help='Clear the form')

else:
    st.write("Please log in")

            #add user login record to database
