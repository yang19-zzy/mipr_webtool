import streamlit as st
from datetime import datetime
import pandas as pd
from consts import *
from funcs import *


#aws credentials - imported from consts.py

#data puller app
if st.experimental_user.is_logged_in:
    with st.sidebar:
        st.write("Sidebar")
        selected_schema = st.selectbox("Select data source", ["cosmed", "dexa"])
        st.write("Selected schema: ", selected_schema)


    sample_data = None

    if selected_schema == "cosmed":
        with st.container(height=400, key="cosmed-data-selection"):
            st.header("Accessing cosmed data")
            folders = list_prefix(BUCKET_NAME,'cosmed-metrics/','/')
            print(folders)
            selected_folder = st.selectbox("Select a metrics", folders)
            # selected_table = st.selectbox("Select a table", ["vo2max", "visit_summary", "visit_data"])
            # # st.write("Selected table: ", selected_table)

            if st.button(f"Get sample data from metrics {selected_folder}"):
                # sample_data = db.get_data(selected_table, 'cosmed', 5)
                f_list = list_prefix(BUCKET_NAME, selected_folder)
                sample_data = pd.read_parquet(f's3://{BUCKET_NAME}/{selected_folder}', storage_options=PQ_STORAGE_OPTIONS).head()
                st.write(sample_data)


    if selected_schema == "dexa":
        with st.container(height=400, key="dexa-data-selection"):
            st.header("Accessing dexa data")
            # folders = list_prefix(BUCKET_NAME,'dexa-metrics/','/')
            # print(folders)
            # selected_folder = st.selectbox("Select a metrics", folders)
            selected_table = st.selectbox("Select a table", ["table1", "table2"])
            # st.write("Selected table: ", selected_table)
        
            if st.button(f"Get sample data from table {selected_table}"):
                sample_data = db.get_data(selected_table, 'dexa', 5)
                st.write(sample_data)

else:
    st.write("Please log in")