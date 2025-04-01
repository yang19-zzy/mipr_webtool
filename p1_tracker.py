import streamlit as st
from datetime import datetime

# Constants
LOGGED_IN_USER = None
row_idx = 0
DEVICE_OPTIONS = ["Apple Watch", "Garmin Watch", "Galaxy Watch", "COSMED", "Dexa", "Inbody", "Other", None]
DEVICE_POSITIONS = ["Left wrist", "Right wrist", "Chest", "Over mouth", 'Other', None]
TODAY = datetime.today()


# Functions
def pop_tracker_status():
    st.toast("Form submitted!", icon="🎉")
    st.write(st.session_state)
    # TODO: Add code to save tracker data to database (e.g., S3 bucket)

def clear_form():
    for key in [
        "submit_owner", "submit_date", "submit_subid", "submit_testid",
        "submit_testtype", "submit_visitnum", "submit_aw", "submit_awmetadata",
        "submit_gar", "submit_garmetadata", "submit_gw", "submit_gwmetadata", "submit_notes"
    ]:
        st.session_state[key] = "" if "metadata" in key or "notes" in key else TODAY if key=='submit_date' else  LOGGED_IN_USER if key=='submit_owner' else None # Reset appropriately

def add_row():
    if "rows" not in st.session_state:
        st.session_state["rows"] = []
    st.session_state["rows"].append({
        "device_key": f"row_device_{len(st.session_state['rows'])}",
        "position_key": f"row_position_{len(st.session_state['rows'])}",
        "notes_key": f"row_notes_{len(st.session_state['rows'])}",
        "row_idx": len(st.session_state["rows"]),
        "other_device": None,
        "other_position": None
    })

def remove_last_row():
    if st.session_state.get("rows"):
        st.session_state["rows"].pop()

@st.dialog("Specify Other")
def specify_other(data_type):
    new_item = st.text_input("Please specify 'Other':")
    if st.button("Specify"):
    # if st.button("Specify"):
        key = f"{row_idx}_{data_type}"
        # if "other_specify" not in st.session_state:
        #     st.session_state["other_specify"] = {}
        # st.session_state["other_specify"][key] = new_item
        # st.session_state["dialog_open"] = False
        # st.session_state[key] = ""  # Reset the input field
        st.rerun()
        return key, new_item

# Check if the user is logged in
if not st.experimental_user.is_logged_in:
    st.warning("Please log in")
    st.stop()

# Set initial values
if "rows" not in st.session_state:
    st.session_state["rows"] = [{
        "device_key": "row_device_0",
        "position_key": "row_position_0",
        "notes_key": "row_notes_0",
        "row_idx": 0,
        "other_device": None,
        "other_position": None
    }]
if "submit_owner" not in st.session_state:
    LOGGED_IN_USER = st.experimental_user.email.split("@")[0] if st.experimental_user.is_logged_in else None
    st.session_state["submit_owner"] = LOGGED_IN_USER
if "other_specify" not in st.session_state:
    st.session_state["other_specify"] = {}

# Main container for the form
with st.container(border=True):
    st.markdown("#### Test Tracker")

    # with st.container():
    # First row: Owner & Subject ID
    col1, col2 = st.columns([1, 1])
    col1.text_input("Who is filling this form:", value=st.session_state["submit_owner"], key="submit_owner", disabled=True)
    col2.text_input("Subject ID:", key="submit_subid")

    # Date & Test ID
    col1, col2 = st.columns([1, 1])
    col1.date_input("Test date:", key="submit_date")
    col2.text_input("Test ID:", key="submit_testid")

    # Dropdown selections
    col1, col2 = st.columns([1, 1])
    col1.selectbox("Test type:", ["cosmedcpet-interval", "cosmedcpet-cycle", "dexa", "inbody", "other"], key="submit_testtype", index=None)
    col2.selectbox("Visit number:", [str(i) for i in range(1, 11)], key="submit_visitnum", index=None)

    st.divider()
    st.markdown("Device(s) worn during the test:")
    for row in st.session_state["rows"]:
        col1, col2, col3 = st.columns(3)
        device_selected = col1.selectbox("Device worn?", DEVICE_OPTIONS, key=row["device_key"], index=None)
        position_selected = col2.selectbox("Body part detected?", DEVICE_POSITIONS, key=row["position_key"], index=None)
        col3.text_input("Other notes?", key=row["notes_key"], placeholder="e.g., model, size")

        if device_selected == "Other" and not st.session_state.get("dialog_open", False):
            # specify_other(row["row_idx"], "device")
            specify_other("device")
            key = f"{row['row_idx']}_device"
            if key in st.session_state["other_specify"]:
                st.session_state[row["other_device"]] = st.session_state["other_specify"][key]
        # if position_selected == "Other":
        #     specify_other(row["row_idx"], "position")

        # if (row["row_idx"], "device") in st.session_state["other_specify"]:
        #     st.session_state[row["other_device"]] = st.session_state["other_specify"][(row["row_idx"], "device")]
        # if (row["row_idx"], "position") in st.session_state["other_specify"]:
        #     st.session_state[row["other_position"]] = st.session_state["other_specify"][(row["row_idx"], "position")]
            

    # Button to add a new row
    col1, col2 = st.columns([1,1])
    col2.button("➕", on_click=add_row, use_container_width=True, help="Add another device row")
    col1.button("➖", on_click=remove_last_row, use_container_width=True, help="Remove last device row")

    # Notes
    # st.text_area("Notes:", key="submit_notes")

    # Buttons
    st.divider()
    col1, col2 = st.columns([1, 1])
    col2.button("Submit", on_click=pop_tracker_status, use_container_width=True)
    col1.button("Clear form", on_click=clear_form, use_container_width=True)