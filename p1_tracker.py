import streamlit as st
from datetime import datetime
from funcs import *
from consts import *

# Constants - imported from consts.py


# Functions - imported from funcs.py


# Check if the user is logged in
if not st.experimental_user.is_logged_in:
    st.warning("Please log in")
    st.stop()

# Set initial values
if "rows" not in st.session_state:
    st.session_state["rows"] = DEVICE_ROW_STARTER
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
    for idx, row in enumerate(st.session_state["rows"]):
        col1, col2, col3 = st.columns(3)
        device_selected = col1.selectbox("Device worn?", DEVICE_OPTIONS, key=row["device_key"], index=None)
        position_selected = col2.selectbox("Body part detected?", DEVICE_POSITIONS, key=row["position_key"], index=None)
        other_notes = col3.text_input("Other notes?", key=row["notes_key"], placeholder="e.g., model, size")

        # Save the selections to session state
        st.session_state["rows"][idx][row["device_key"]] = device_selected
        st.session_state["rows"][idx][row["position_key"]] = position_selected
        st.session_state["rows"][idx][row["notes_key"]] = other_notes

        #pop up window to specify other device or position if 'Other' is selected
        if device_selected == "Other":
            specify_other(row, "device")
            other_device_key = f"other_device_{row['row_idx']}_device"
            if other_device_key in st.session_state:
                st.write(f"You specified: {st.session_state[other_device_key]} for row device")

        if position_selected == "Other":
            specify_other(row, "position")
            other_position_key = f"other_position_{row['row_idx']}_position"
            if other_position_key in st.session_state:
                st.write(f"You specified: {st.session_state[other_position_key]} for row position")


    # Button to add a new row
    col1, col2 = st.columns([1,1])
    col2.button("➕ Add another device", on_click=add_row, use_container_width=True, help="Add another device")
    col1.button("➖ Remove last device", on_click=remove_last_row, use_container_width=True, help="Remove last device")

    # Notes
    # st.text_area("Notes:", key="submit_notes")

    # Buttons
    st.divider()
    col1, col2 = st.columns([1, 1])
    col2.button("Submit", on_click=pop_tracker_status, use_container_width=True)
    col1.button("Clear form", on_click=clear_form, use_container_width=True)


# st.write(st.session_state)