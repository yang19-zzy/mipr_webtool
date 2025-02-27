import streamlit as st
import requests
import urllib.parse
import boto3

import time





## s3 uri:s 3://cosmed-metrics/testVO2MaxParquet/





def page_home():
    st.title("Home")



def main():

    st.write("Welcome to the database access demo")
    # current_user = {
    #     "logged_in": False,
    #     "email": None,
    #     "user_id": None,
    #     "role": None
    # }
    # st.write(st.session_state.keys())
    st.write(st.experimental_user)
    if not st.experimental_user.is_logged_in:
        with st.container():
            if st.button("Log in"):
                st.login()

                #add user login record to database
    else:
        #if logged in, display content
        st.write(f"Logged in as {st.experimental_user.email}")
        st.write(f"User ID: {st.experimental_user.name}")

        pages = {
            "Home": [st.Page(page_home)],
            "Data Mapping": [
                st.Page("main01_map.py", title="Data Mapping", icon="🚨"),
            ],
            "Data Metrics Calculation": [
                st.Page("main02_calc.py", title="Data Metrics Calculation"),
            ],
            "Data Access": [
                st.Page("main03_gui.py", title="Data Access")
            ],
        }



        st.navigation(pages)
        # page_test = st.Page("main02_calc.py", title="Data Metrics Calculation", icon="🚨")

        # pg = st.navigation({'test': [page_test]})

        
        with st.sidebar:
            st.write("Sidebar")
            selected_schema = st.selectbox("Select data source", ["cosmed", "dexa"])
            st.write("Selected schema: ", selected_schema)

            

            if st.button("Log out"):
                st.logout()



        sample_data = None

        if selected_schema == "cosmed":
            with st.container(height=400, key="cosmed-data-selection"):
                st.header("Accessing cosmed data")
                selected_table = st.selectbox("Select a table", ["vo2max", "visit_summary", "visit_data"])
                # st.write("Selected table: ", selected_table)

                if st.button(f"Get sample data from table {selected_table}"):
                    sample_data = db.get_data(selected_table, 'cosmed', 5)
                    st.write(sample_data)


        if selected_schema == "dexa":
            with st.container(height=400, key="dexa-data-selection"):
                st.header("Accessing dexa data")
                selected_table = st.selectbox("Select a table", ["table1", "table2"])
                # st.write("Selected table: ", selected_table)
            
                if st.button(f"Get sample data from table {selected_table}"):
                    sample_data = db.get_data(selected_table, 'dexa', 5)
                    st.write(sample_data)
            

        # if sample_data is not None:
        #     st.download_button(label="Download sample data", data=sample_data.to_csv(), file_name="sample_data.csv", mime="text/csv")
            

    


if __name__ == '__main__':
    st.title("Database Access Demo")
    main()
