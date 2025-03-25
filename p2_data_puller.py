import streamlit as st
from st_files_connection import FilesConnection
from sqlalchemy import create_engine

import requests
import urllib.parse
import boto3
import s3fs
import pandas as pd


#aws credentials
AWS_ACCESS_KEY = st.secrets['aws']['ACCESS_KEY_ID']
AWS_SECRET_KEY = st.secrets['aws']['SECRET_ACCESS_KEY']
AWS_REGION = st.secrets['aws']['DEFAULT_REGION']
PQ_STORAGE_OPTIONS = {"key":AWS_ACCESS_KEY, "secret": AWS_SECRET_KEY}
BUCKET_NAME = 'cosmed-metrics'
FOLDER_PATH = ''

#initial s3 client
@st.cache_resource
def connect_s3():
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)
    return s3
s3 = connect_s3()


@st.cache_data
def list_prefix(bucket:str, prefix:str="", delimiter:str="") -> list:
    """
    list all files in a bucket with a given prefix (aka folder)
    OR list folders in a bucket with a given prefix
    """
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter=delimiter)
    if delimiter:
        return [f.get('Prefix') for f in response.get('CommonPrefixes', [])]
    else:
        return [f.get('Key') for f in response.get('Contents', [])]


@st.cache_data
def get_data(bucket:str, prefixes:list) -> pd.DataFrame:
    """
    take a list of prefixes and keys and return a dataframe
    - bucket: the name of the bucket
    - prefix: user selected folder name(s)
    """
    key_list = []
    for prefix in prefixes:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        key_list.extend([f.get('Key') for f in response.get('Contents', [])])

    # s3.get_object(Bucket=bucket, Key=key_list[0])
    print(key_list)
    # pd.read_parquet(f's3://{bucket}/{key_list[0]}')
    


if st.experimental_user.is_logged_in:
    with st.sidebar:
        st.write("Sidebar")
        selected_schema = st.selectbox("Select data source", ["cosmed", "dexa"])
        st.write("Selected schema: ", selected_schema)


    sample_data = None

    if selected_schema == "cosmed":
        with st.container(height=400, key="cosmed-data-selection"):
            st.header("Accessing cosmed data")
            folders = list_prefix(BUCKET_NAME,'','/')
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
            selected_table = st.selectbox("Select a table", ["table1", "table2"])
            # st.write("Selected table: ", selected_table)
        
            if st.button(f"Get sample data from table {selected_table}"):
                sample_data = db.get_data(selected_table, 'dexa', 5)
                st.write(sample_data)

else:
    st.write("Please log in")