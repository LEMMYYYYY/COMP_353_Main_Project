import streamlit as st
import pandas as pd
import db
import db_operations as ops

st.title("Locations")

# NEW: Use our enriched query function from the backend
rows = db.execute_query(ops.get_all_locations_with_phones)
df = pd.DataFrame(rows)

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No locations have been added yet.")
    st.stop()

st.subheader("Manage Phone Numbers")

# Create a mapping of display names to IDs for the dropdown
options = {f"{row['name']} ({row['city']})": row['location_id'] for index, row in df.iterrows()}
selected_name = st.selectbox("Select a Location", options.keys())
location_id = options[selected_name]

# NEW: Use our generic search to get phones for the selected location
phones = db.execute_query(ops.search, params={"table_name": "location_phone_numbers", "location_id": location_id})
st.write("Existing Numbers:", [p['phone_number'] for p in phones])

with st.form("add_phone", clear_on_submit=True):
    phone = st.text_input("Add New Phone Number")
    submitted = st.form_submit_button("Add")
    if submitted and phone:
        try:
            # NEW: Call the specific backend function via our bridge
            db.execute_change(ops.add_location_phone_number, params={"location_id": location_id, "phone_number": phone})
            st.success("Added phone number.")
            st.experimental_rerun()
        except db.RuleViolation as e:
            st.error(f"Could not add phone number: {e}")

if phones:
    del_phone = st.selectbox("Select a phone number to delete", [p['phone_number'] for p in phones])
    if st.button("Delete This Phone Number"):
        try:
            # NEW: Call the generic delete function from the backend
            params = {"table_name": "location_phone_numbers", "location_id": location_id, "phone_number": del_phone}
            db.execute_change(ops.delete, params=params)
            st.success("Deleted phone number.")
            st.experimental_rerun()
        except db.RuleViolation as e:
            st.error(f"Could not delete phone: {e}")