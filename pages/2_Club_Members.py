import streamlit as st
import pandas as pd
import db
import db_operations as ops
from datetime import date

st.set_page_config(layout="wide")
st.title("Manage Club Members")

# --- CREATE ---
with st.expander("➕ Register a New Club Member"):
    with st.form("new_member_form", clear_on_submit=True):
        st.subheader("New Member Registration")
        
        # Person Details
        st.write("##### Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name*")
            last_name = st.text_input("Last Name*")
            dob = st.date_input("Date of Birth*", min_value=date(1920, 1, 1))
            gender = st.selectbox("Gender*", ["Male", "Female"])
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
        with col2:
            ssn = st.text_input("SSN (Required)*", help="Must be provided for members and staff.")
            medicare = st.text_input("Medicare Number")
            address = st.text_input("Street Address")
            city = st.text_input("City")
            province = st.text_input("Province")
            postal_code = st.text_input("Postal Code")

        # Club Member Details
        st.write("##### Membership Information")
        col3, col4, col5 = st.columns(3)
        with col3:
            join_date = st.date_input("Join Date*", value=date.today())
        with col4:
            height = st.number_input("Height (cm)", min_value=0.0, step=1.0, format="%.2f")
        with col5:
            weight = st.number_input("Weight (kg)", min_value=0.0, step=1.0, format="%.2f")
        
        submitted = st.form_submit_button("Register Member")
        if submitted:
            if not all([first_name, last_name, dob, ssn, gender, join_date]):
                st.warning("Please fill in all required (*) fields.")
            else:
                person_data = {
                    "first_name": first_name, "last_name": last_name, "dob": dob, "gender": gender,
                    "ssn": ssn or None, "medicare_number": medicare or None, "phone_number": phone or None,
                    "address": address or None, "city": city or None, "province": province or None,
                    "postal_code": postal_code or None, "email_address": email or None
                }
                member_data = {
                    "join_date": join_date, "height": height or None, "weight": weight or None
                }
                try:
                    db.execute_change(ops.register_new_club_member, params={"person_data": person_data, "member_data": member_data})
                    st.success("New member registered successfully!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Error registering member: {e}")

st.divider()

# --- READ / UPDATE / DELETE ---
st.header("View and Edit Existing Members")

members = db.execute_query(ops.get_all_members_with_details)
if not members:
    st.info("No members found. Use the form above to register one.")
    st.stop()

st.dataframe(pd.DataFrame(members), use_container_width=True, hide_index=True)

st.subheader("Select a Member to Manage")
member_options = {f"#{m['club_member_id']} - {m['first_name']} {m['last_name']}": m['club_member_id'] for m in members}
selected_label = st.selectbox("Select Member", member_options.keys())
selected_id = member_options[selected_label]

profile = db.execute_query(ops.get_member_profile, params={"club_member_id": selected_id})

if profile:
    st.write("#### Member Profile")
    st.json(profile)

# --- UPDATE ---
with st.expander("✏️ Update Member's Profile"):
    with st.form("update_member_form"):
        st.write(f"Now editing: **{profile['first_name']} {profile['last_name']}**")
        
        col1, col2 = st.columns(2)
        with col1:
            update_email = st.text_input("Email Address", value=profile['email_address'] or "")
            update_address = st.text_input("Address", value=profile['address'] or "")
            update_province = st.text_input("Province", value=profile['province'] or "")
            update_height = st.number_input("Height (cm)", value=float(profile['height'] or 0.0), format="%.2f")

        with col2:
            update_phone = st.text_input("Phone Number", value=profile['phone_number'] or "")
            update_city = st.text_input("City", value=profile['city'] or "")
            update_postal_code = st.text_input("Postal Code", value=profile['postal_code'] or "")
            update_weight = st.number_input("Weight (kg)", value=float(profile['weight'] or 0.0), format="%.2f")

        update_submitted = st.form_submit_button("Save Profile Changes")
        if update_submitted:
            person_updates = {
                "email_address": update_email or None, "phone_number": update_phone or None,
                "address": update_address or None, "city": update_city or None,
                "province": update_province or None, "postal_code": update_postal_code or None
            }
            member_updates = {"height": update_height or None, "weight": update_weight or None}
            try:
                db.execute_change(ops.update_member_profile, params={
                    "club_member_id": selected_id, "person_data": person_updates, "member_data": member_updates
                })
                st.success("Profile updated!")
                st.rerun()
            except db.RuleViolation as e:
                st.error(f"Error updating profile: {e}")

# --- LOCATION ASSIGNMENT ---
with st.expander("📍 Manage Location Assignment"):
    st.write("##### Location History")
    # Use generic search to get all assignments for this person
    history = db.execute_query(ops.search, params={"table_name": "location_assignment", "person_id": selected_id})
    st.table(pd.DataFrame(history))

    st.write("##### Assign to a New Location")
    st.info("Assigning a new location will automatically end the previous one if it's currently active. This is handled by a database trigger.", icon="ℹ️")
    
    locations = db.execute_query(ops.get_all_locations_with_phones)
    if not locations:
        st.warning("No locations available to assign.")
    else:
        loc_map = {f"{l['name']} ({l['city']})": l['location_id'] for l in locations}
        
        with st.form("new_location_assignment_form", clear_on_submit=True):
            loc_label = st.selectbox("Select New Location*", loc_map.keys())
            start_date = st.date_input("Assignment Start Date*", value=date.today())
            
            submitted = st.form_submit_button("Assign to Location")
            if submitted:
                try:
                    # Call our existing assignment function, but WITHOUT role/mandate
                    db.execute_change(ops.assign_person_to_location, params={
                        "person_id": selected_id,
                        "location_id": loc_map[loc_label],
                        "start_date": start_date
                    })
                    st.success("Member successfully assigned to new location.")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Could not assign location: {e}")
                    
# --- FAMILY LINKS ---
with st.expander("👨‍👩‍👧 Manage Family Links"):
    st.write("##### Existing Family Links")
    links = db.execute_query(ops.get_family_links_for_member, params={"club_member_id": selected_id})
    
    if not links:
        st.info("No family links exist for this member.")
    else:
        header_cols = st.columns((2, 2, 2, 2, 1))
        header_cols[0].write("**Name**")
        header_cols[1].write("**Relationship**")
        header_cols[2].write("**Priority**")
        for link in links:
            row_cols = st.columns((2, 2, 2, 2, 1))
            row_cols[0].write(f"{link['first_name']} {link['last_name']}")
            row_cols[1].write(link['relationship_type'])
            row_cols[2].write(link['contact_priority'])
            if row_cols[4].button("🗑️", key=f"del_{link['family_member_id']}"):
                try:
                    db.execute_change(ops.delete, params={
                        "table_name": "club_member_family_link",
                        "club_member_id": selected_id,
                        "family_member_id": link['family_member_id']
                    })
                    st.success(f"Link to {link['first_name']} {link['last_name']} removed.")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Could not remove link: {e}")

    st.write("##### Create a New Person and Link as Family")
    with st.form("new_family_member_form", clear_on_submit=True):
        st.write("Use this form to add a new contact who is not yet in the system. SSN is not required for contacts.")
        col1, col2 = st.columns(2)
        with col1:
            fm_first_name = st.text_input("First Name*")
            fm_last_name = st.text_input("Last Name*")
            fm_dob = st.date_input("Date of Birth*", min_value=date(1920, 1, 1), key="fm_dob")
            fm_gender = st.selectbox("Gender*", ["Male", "Female"], key="fm_gender")
        with col2:
            fm_phone = st.text_input("Phone Number")
            fm_email = st.text_input("Email Address")
            fm_address = st.text_input("Street Address", key="fm_address")
            fm_city = st.text_input("City", key="fm_city")

        fm_rel_type = st.selectbox("Relationship*", ["Father", "Mother", "Guardian", "Tutor", "Friend", "Other"], key="fm_rel_type")
        fm_priority = st.selectbox("Contact Priority*", ["Primary", "Secondary"], key="fm_priority")
        
        create_and_link_submitted = st.form_submit_button("Create Person and Link")
        if create_and_link_submitted:
            if not all([fm_first_name, fm_last_name, fm_dob, fm_gender]):
                st.warning("Please fill in all required (*) fields for the new person.")
            else:
                person_data = {
                    "first_name": fm_first_name, "last_name": fm_last_name, "dob": fm_dob, "gender": fm_gender,
                    "phone_number": fm_phone or None, "email_address": fm_email or None,
                    "address": fm_address or None, "city": fm_city or None
                }
                link_data = {"relationship_type": fm_rel_type, "contact_priority": fm_priority}
                try:
                    db.execute_change(ops.create_and_link_family_member, params={
                        "club_member_id": selected_id, "person_data": person_data, "link_data": link_data
                    })
                    st.success("New family member created and linked successfully!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Error creating and linking family member: {e}")

    st.divider()
    st.write("##### Link an Existing Person")
    
    all_people = db.execute_query(ops.search, params={"table_name": "person"})
    # Exclude the member themselves and already linked family members from the list
    linked_ids = {link['family_member_id'] for link in links}
    people_options = {
        f"#{p['person_id']} - {p['first_name']} {p['last_name']}": p['person_id'] 
        for p in all_people if p['person_id'] != selected_id and p['person_id'] not in linked_ids
    }
    
    if people_options:
        col1, col2, col3 = st.columns(3)
        with col1:
            family_label = st.selectbox("Select Existing Person to Link", people_options.keys())
        with col2:
            rel_type = st.selectbox("Relationship", ["Father", "Mother", "Guardian", "Tutor", "Friend", "Other"])
        with col3:
            priority = st.selectbox("Contact Priority", ["Primary", "Secondary"])

        if st.button("Create Family Link"):
            try:
                db.execute_change(ops.link_family_to_member, params={
                    "club_member_id": selected_id,
                    "family_member_id": people_options[family_label],
                    "relationship_type": rel_type,
                    "contact_priority": priority
                })
                st.success("Family link created!")
                st.rerun()
            except db.RuleViolation as e:
                st.error(f"Error creating link: {e}. (A member can only have one Primary and one Secondary contact).")
    else:
        st.info("No other people available to link.")  

# --- DELETE ---
with st.expander("🗑️ Delete Member"):
    st.warning(f"Warning: This will permanently delete {profile['first_name']} {profile['last_name']} and all their associated records (payments, assignments, etc.) due to cascading database rules.", icon="⚠️")
    
    if st.button(f"Permanently Delete Member #{selected_id}"):
        try:
            # Deleting the 'person' record will cascade to all other tables.
            db.execute_change(ops.delete, params={"table_name": "person", "person_id": selected_id})
            st.success("Member deleted successfully.")
            st.rerun()
        except db.RuleViolation as e:
            st.error(f"Could not delete member: {e}")