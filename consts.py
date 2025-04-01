from datetime import datetime
import streamlit as st

#tracker form constants
LOGGED_IN_USER = None
DEVICE_OPTIONS = ["Apple Watch", "Garmin Watch", "Galaxy Watch", "COSMED", "Dexa", "Inbody", "Other", "Other-specified"]
DEVICE_POSITIONS = ["Left wrist", "Right wrist", "Chest", "Over mouth", 'Other', "Other-specified"]
DEVICE_ROW_STARTER = [{
        "device_key": "row_device_0",
        "position_key": "row_position_0",
        "notes_key": "row_notes_0",
        "row_idx": 0,
        "other_device": None,
        "other_position": None,
        "row_device_0": None,
        "row_position_0": None,
        "row_notes_0": None
    }]
TODAY = datetime.today()


#aws credentials
AWS_CREDENTIALS = st.secrets['aws']
WHITELIST_SECRET_NAME = AWS_CREDENTIALS['WHITELIST_SECRET_NAME']
REGION_NAME = AWS_CREDENTIALS['DEFAULT_REGION']
AWS_ACCESS_KEY = AWS_CREDENTIALS['ACCESS_KEY_ID']
AWS_SECRET_KEY = AWS_CREDENTIALS['SECRET_ACCESS_KEY']
AWS_REGION = AWS_CREDENTIALS['DEFAULT_REGION']
PQ_STORAGE_OPTIONS = {"key":AWS_ACCESS_KEY, "secret": AWS_SECRET_KEY}
BUCKET_NAME = 'primelab-calculated-metrics'
FOLDER_PATH = ''


#session management
SESSION_TIMEOUT = 300  # 5 minutes


#app description
APP_DESCRIPTION = """
This is a demo of a Streamlit app that allows users to log in and access a database.

The app is divided into two sections:
- Test Tracker / File Submission Tracker
- Database Acess
- Data Visualization
"""