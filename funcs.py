import boto3
from botocore.exceptions import ClientError
import pandas as pd
import json
from consts import *

import streamlit as st

# ----------------------
# Data Handling Functions
# ----------------------
def form_data_parser(form_data):
    """Parse the form data and return a dictionary with relevant information."""


    return {}  # Placeholder, implement actual parsing logic as needed.

# ----------------------
# S3 Connection and Data Retrieval
# ----------------------
@st.cache_resource
def connect_s3():
    """Initialize S3 client."""
    return boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

s3 = connect_s3()

@st.cache_data
def list_prefix(bucket: str, prefix: str = "", delimiter: str = "") -> list:
    """List all files or folders in a given S3 bucket prefix."""
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter=delimiter)
    return [f.get('Prefix') if delimiter else f.get('Key') for f in response.get('CommonPrefixes', []) or response.get('Contents', [])]

@st.cache_data
def get_data(bucket: str, prefixes: list) -> pd.DataFrame:
    """Retrieve and return data from S3 bucket based on given prefixes."""
    key_list = []
    for prefix in prefixes:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        key_list.extend([f.get('Key') for f in response.get('Contents', [])])
    return key_list  # Modify to return actual DataFrame when needed.


@st.cache_resource
@st.cache_data
def get_secret():
    """Fetch the whitelist from AWS Secrets Manager."""
    # session = boto3.session.Session()
    # client = session.client(service_name='secretsmanager', region_name=REGION_NAME)
    client = boto3.client(service_name='secretsmanager', region_name=REGION_NAME, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        response = client.get_secret_value(SecretId=WHITELIST_SECRET_NAME)
    except ClientError as e:
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    secret = response['SecretString']
    secret = json.loads(secret)
    print(secret)
    print(type(secret))
    return secret.get('umid', [])

# ----------------------
# Form Action Functions
# ----------------------
def pop_tracker_status():
    """Display success toast and log form submission."""
    st.toast("Form submitted!", icon="🎉")
    st.write(st.session_state)
    # TODO: Add code to save tracker data to database (e.g., S3 bucket)


def clear_form():
    """Reset form fields and clear row selections."""
    if "rows" in st.session_state:
        for row in st.session_state["rows"]:
            st.session_state[row["device_key"]] = None
            st.session_state[row["position_key"]] = None
            st.session_state[row["notes_key"]] = None

    st.session_state["rows"] = DEVICE_ROW_STARTER.copy()
    st.session_state.update({
        "submit_owner": LOGGED_IN_USER,
        "submit_date": TODAY,
        "submit_subid": None,
        "submit_testid": None,
        "submit_testtype": None,
        "submit_visitnum": None
    })


def add_row():
    """Add a new row to the session state."""
    if "rows" not in st.session_state:
        st.session_state["rows"] = []

    row_idx = len(st.session_state["rows"])
    new_row = {
        "device_key": f"row_device_{row_idx}",
        "position_key": f"row_position_{row_idx}",
        "notes_key": f"row_notes_{row_idx}",
        "row_idx": row_idx,
        "other_device": None,
        "other_position": None
    }

    st.session_state["rows"].append(new_row)


def remove_last_row():
    """Remove the last row if available."""
    if st.session_state.get("rows") and st.session_state["rows"]:
        st.session_state["rows"].pop()


@st.dialog("Specify Other")
def specify_other(row, data_type):
    """Handle 'Other' specification through dialog."""
    row_idx = row['row_idx']
    new_item = st.text_input(f"Please specify 'Other':")
    if st.button("Specify", key=f"specify_button_{row_idx}_{data_type}"):
        st.session_state["rows"][row_idx][f"other_{data_type}"] = new_item
        st.session_state[f"row_{data_type}_{row_idx}"] = "Other-specified"
        st.rerun()
