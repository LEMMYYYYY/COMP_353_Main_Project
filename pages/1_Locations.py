import streamlit as st
import pandas as pd
import db
import db_operations as ops

st.set_page_config(layout="wide")
st.title("Manage Locations")

# --- CREATE ---
with st.expander("➕ Add a New Location"):
    with st.form("new_location_form", clear_on_submit=True):
        st.subheader("New Location Details")
        
        col1, col2 = st.columns(2)
        with col1:
            loc_name = st.text_input("Location Name*", help="e.g., 'MVC Downtown'")
            loc_address = st.text_input("Address")
            loc_province = st.text_input("Province")
            loc_web = st.text_input("Web Address", help="e.g., https://mvc.example.com")
        with col2:
            loc_type = st.selectbox("Location Type*", ["Branch", "Head"])
            loc_city = st.text_input("City")
            loc_postal = st.text_input("Postal Code")
            loc_capacity = st.number_input("Max Capacity", min_value=0, step=10)
            
        submitted = st.form_submit_button("Create Location")
        if submitted:
            if not loc_name or not loc_type:
                st.warning("Location Name and Type are required.")
            else:
                try:
                    db.execute_change(ops.add_location, params={
                        "name": loc_name, "location_type": loc_type, "address": loc_address,
                        "city": loc_city, "province": loc_province, "postal_code": loc_postal or None,
                        "web_address": loc_web or None, "max_capacity": loc_capacity or None
                    })
                    st.success("Location created successfully!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Error creating location: {e}")

st.divider()

# --- READ / UPDATE / DELETE ---
st.header("View and Edit Existing Locations")

locations = db.execute_query(ops.get_all_locations_with_phones)
if not locations:
    st.info("No locations found. Add one using the form above.")
    st.stop()

df = pd.DataFrame(locations)
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Select a Location to Manage")

options = {f"#{row['location_id']} - {row['name']} ({row['city']})": row['location_id'] for index, row in df.iterrows()}
selected_name = st.selectbox("Select a Location", options.keys())
selected_id = options[selected_name]

selected_location_data = next((loc for loc in locations if loc['location_id'] == selected_id), None)

if selected_location_data:
    # --- UPDATE ---
    with st.expander("✏️ Update Location Details"):
        with st.form("update_location_form"):
            st.write(f"Now editing: **{selected_location_data['name']}**")
            
            col1, col2 = st.columns(2)
            with col1:
                update_name = st.text_input("Location Name", value=selected_location_data['name'])
                update_address = st.text_input("Address", value=selected_location_data['address'])
                update_postal_code = st.text_input("Postal Code", value=selected_location_data['postal_code'])
            with col2:
                update_web = st.text_input("Web Address", value=selected_location_data['web_address'])
                update_capacity = st.number_input("Max Capacity", value=selected_location_data['max_capacity'] or 0)
            
            update_submitted = st.form_submit_button("Save Changes")
            if update_submitted:
                update_data = {
                    "name": update_name,
                    "address": update_address,
                    "web_address": update_web,
                    "max_capacity": update_capacity,
                    "postal_code": update_postal_code
                }
                criteria = {"location_id": selected_id}
                try:
                    db.execute_change(ops.update, params={"table_name": "locations", "criteria": criteria, "new_data": update_data})
                    st.success("Location details updated!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Error updating location: {e}")

    # --- MANAGE PHONE NUMBERS ---
    with st.expander("📞 Manage Phone Numbers"):
        st.write(f"##### Phone Numbers for **{selected_location_data['name']}**")
        current_phones = db.execute_query(ops.search, params={"table_name": "location_phone_numbers", "location_id": selected_id})
        phone_list = [p['phone_number'] for p in current_phones]
        
        if not phone_list:
            st.info("This location has no phone numbers.")
        else:
            st.write(phone_list)

        with st.form("add_phone_form", clear_on_submit=True):
            new_phone = st.text_input("Add New Phone Number")
            add_phone_submitted = st.form_submit_button("Add Phone")
            if add_phone_submitted and new_phone:
                try:
                    db.execute_change(ops.add_location_phone_number, params={"location_id": selected_id, "phone_number": new_phone})
                    st.success("Phone number added!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Could not add phone number: {e}")

        if phone_list:
            st.write("---")
            phone_to_delete = st.selectbox("Select phone number to delete", phone_list)
            if st.button("Delete Selected Phone Number"):
                try:
                    db.execute_change(ops.delete, params={"table_name": "location_phone_numbers", "location_id": selected_id, "phone_number": phone_to_delete})
                    st.success("Phone number deleted.")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Could not delete phone number: {e}")

    # --- DELETE LOCATION ---
    with st.expander("🗑️ Delete Location"):
        st.warning(f"Warning: Deleting a location is permanent. If any teams or staff are assigned, the deletion may be blocked by the database to preserve data integrity.", icon="⚠️")
        
        if st.button(f"Permanently Delete Location #{selected_id} - {selected_location_data['name']}"):
            try:
                db.execute_change(ops.delete, params={"table_name": "locations", "location_id": selected_id})
                st.success("Location deleted successfully!")
                st.rerun()
            except db.RuleViolation as e:
                st.error(f"Could not delete location: {e}. (This is likely because it is still in use).")