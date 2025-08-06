import streamlit as st
import pandas as pd
import db
import db_operations as ops

st.set_page_config(layout="wide")
st.title("Manage Hobbies and Assignments")

# =================================================================
# PART 1: CRUD for the Master Hobbies List
# =================================================================
st.header("Master Hobby List")

# --- CREATE ---
with st.expander("➕ Add a New Hobby to the Master List"):
    with st.form("new_hobby_form", clear_on_submit=True):
        hobby_name = st.text_input("Hobby Name*")
        description = st.text_area("Description (Optional)")
        
        submitted = st.form_submit_button("Create Hobby")
        if submitted:
            if not hobby_name:
                st.warning("Hobby Name is required.")
            else:
                try:
                    db.execute_change(ops.add_hobby, params={"hobby_name": hobby_name, "description": description})
                    st.success(f"Hobby '{hobby_name}' created successfully!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Error creating hobby: {e}")

# --- READ / UPDATE / DELETE ---
hobbies = db.execute_query(ops.search, params={"table_name": "hobbies"})
if not hobbies:
    st.info("No hobbies found. Use the form above to create one.")
else:
    st.dataframe(pd.DataFrame(hobbies), use_container_width=True, hide_index=True)

    st.subheader("Select a Hobby to Update or Delete")
    hobby_options = {f"#{h['hobby_id']} - {h['hobby_name']}": h['hobby_id'] for h in hobbies}
    selected_label = st.selectbox("Select Hobby", hobby_options.keys())
    selected_id = hobby_options[selected_label]
    selected_hobby_data = next((h for h in hobbies if h['hobby_id'] == selected_id), None)

    if selected_hobby_data:
        # --- UPDATE ---
        with st.expander("✏️ Update Selected Hobby"):
            with st.form("update_hobby_form"):
                update_name = st.text_input("Hobby Name", value=selected_hobby_data['hobby_name'])
                update_desc = st.text_area("Description", value=selected_hobby_data['description'])
                if st.form_submit_button("Save Changes"):
                    update_data = {"hobby_name": update_name, "description": update_desc}
                    criteria = {"hobby_id": selected_id}
                    try:
                        db.execute_change(ops.update, params={"table_name": "hobbies", "criteria": criteria, "new_data": update_data})
                        st.success("Hobby updated!")
                        st.rerun()
                    except db.RuleViolation as e:
                        st.error(f"Error updating hobby: {e}")

        # --- DELETE ---
        with st.expander("🗑️ Delete Selected Hobby"):
            st.warning(f"Warning: Deleting a hobby is permanent. It will be un-assigned from all members who have it.", icon="⚠️")
            if st.button(f"Permanently Delete '{selected_hobby_data['hobby_name']}'"):
                try:
                    # ON DELETE CASCADE in the database will handle removing the links
                    db.execute_change(ops.delete, params={"table_name": "hobbies", "hobby_id": selected_id})
                    st.success("Hobby deleted successfully.")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Could not delete hobby: {e}")

st.divider()

# =================================================================
# PART 2: Assign Hobbies to Club Members
# =================================================================
st.header("Assign Hobbies to Members")

members = db.execute_query(ops.get_all_members_with_details)
if not members:
    st.warning("No members exist to assign hobbies to. Please create a member first.", icon="⚠️")
    st.stop()

member_options = {f"#{m['club_member_id']} - {m['first_name']} {m['last_name']}": m['club_member_id'] for m in members}
selected_member_label = st.selectbox("Select a Club Member to Manage Their Hobbies", member_options.keys())
selected_member_id = member_options[selected_member_label]

if selected_member_id:
    st.subheader(f"Hobbies for {selected_member_label.split(' - ')[1]}")
    
    # Use our new backend function to get the member's current hobbies
    member_hobbies = db.execute_query(ops.get_hobbies_for_member, params={"club_member_id": selected_member_id})
    
    if not member_hobbies:
        st.info("This member has no assigned hobbies.")
    else:
        # Display current hobbies with a button to remove each one
        for hobby in member_hobbies:
            col1, col2 = st.columns([4, 1])
            col1.write(f"- {hobby['hobby_name']}")
            if col2.button("Remove", key=f"del_link_{hobby['hobby_id']}"):
                try:
                    db.execute_change(ops.delete, params={
                        "table_name": "club_member_hobbies",
                        "club_member_id": selected_member_id,
                        "hobby_id": hobby['hobby_id']
                    })
                    st.success(f"Removed hobby '{hobby['hobby_name']}'.")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Could not remove hobby: {e}")

    st.write("---")
    st.write("##### Assign a New Hobby")
    
    # Filter the master hobby list to show only hobbies the member DOES NOT have
    member_hobby_ids = {h['hobby_id'] for h in member_hobbies}
    available_hobbies = [h for h in hobbies if h['hobby_id'] not in member_hobby_ids]
    
    if not available_hobbies:
        st.info("This member has been assigned all available hobbies.")
    else:
        hobby_to_add_options = {h['hobby_name']: h['hobby_id'] for h in available_hobbies}
        selected_hobby_to_add = st.selectbox("Select a hobby to add", hobby_to_add_options.keys())
        
        if st.button("Assign Selected Hobby"):
            try:
                db.execute_change(ops.add_hobby_to_member, params={
                    "club_member_id": selected_member_id,
                    "hobby_id": hobby_to_add_options[selected_hobby_to_add]
                })
                st.success("Hobby assigned!")
                st.rerun()
            except db.RuleViolation as e:
                st.error(f"Could not assign hobby: {e}")