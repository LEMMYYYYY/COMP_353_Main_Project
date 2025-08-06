import streamlit as st
import pandas as pd
import db
import db_operations as ops

st.set_page_config(layout="wide")
st.title("Manage Teams")

# --- Dependency Check: Make sure locations exist before trying to create a team ---
locations = db.execute_query(ops.get_all_locations_with_phones)
if not locations:
    st.warning("You must create at least one location before you can create a team.", icon="⚠️")
    st.stop()

# --- CREATE ---
with st.expander("➕ Create a New Team"):
    with st.form("new_team_form", clear_on_submit=True):
        st.subheader("New Team Details")
        
        team_name = st.text_input("Team Name*")
        
        col1, col2 = st.columns(2)
        with col1:
            team_gender = st.selectbox("Team Gender*", ["Male", "Female"])
        with col2:
            # Create a mapping of location names to their IDs for the dropdown
            loc_options = {f"{l['name']} ({l['city']})": l['location_id'] for l in locations}
            selected_loc_name = st.selectbox("Home Location*", loc_options.keys())
        
        submitted = st.form_submit_button("Create Team")
        if submitted:
            if not team_name:
                st.warning("Team Name is required.")
            else:
                try:
                    db.execute_change(ops.add_team, params={
                        "name": team_name,
                        "team_gender": team_gender,
                        "home_location_id": loc_options[selected_loc_name]
                    })
                    st.success(f"Team '{team_name}' created successfully!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Error creating team: {e}")

st.divider()

# --- READ / UPDATE / DELETE ---
st.header("View and Edit Existing Teams")

# Use our new backend function to get the team list
teams = db.execute_query(ops.get_all_teams_with_details)
if not teams:
    st.info("No teams found. Use the form above to create one.")
    st.stop()

df = pd.DataFrame(teams)
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Select a Team to Update or Delete")

# Create options for the selection dropdown
team_options = {f"#{t['team_id']} - {t['name']} ({t['team_gender']})": t['team_id'] for t in teams}
selected_team_label = st.selectbox("Select Team", team_options.keys())
selected_id = team_options[selected_team_label]

# Get the full details of the selected team
selected_team_data = next((t for t in teams if t['team_id'] == selected_id), None)

if selected_team_data:
    # --- UPDATE ---
    with st.expander("✏️ Update Selected Team's Details"):
        with st.form("update_team_form"):
            st.write(f"Now editing: **{selected_team_data['name']}**")
            
            update_name = st.text_input("Team Name", value=selected_team_data['name'])
            
            # For dropdowns, we need to find the index of the current value to pre-select it
            gender_options = ["Male", "Female"]
            current_gender_index = gender_options.index(selected_team_data['team_gender'])
            update_gender = st.selectbox("Team Gender", gender_options, index=current_gender_index)
            
            loc_options_list = list(loc_options.keys())
            # Find the key that corresponds to the current home_location_id
            current_loc_key = next((key for key, val in loc_options.items() if val == selected_team_data['home_location_id']), None)
            current_loc_index = loc_options_list.index(current_loc_key) if current_loc_key else 0
            update_loc_name = st.selectbox("Home Location", loc_options_list, index=current_loc_index)
            
            update_submitted = st.form_submit_button("Save Changes")
            if update_submitted:
                update_data = {
                    "name": update_name,
                    "team_gender": update_gender,
                    "home_location_id": loc_options[update_loc_name]
                }
                criteria = {"team_id": selected_id}
                try:
                    db.execute_change(ops.update, params={"table_name": "teams", "criteria": criteria, "new_data": update_data})
                    st.success("Team details updated!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Error updating team: {e}")

    # --- DELETE ---
    st.subheader("🗑️ Delete Selected Team")
    st.warning(f"Warning: Deleting a team is permanent. If this team is already part of a session, the database will block the deletion to maintain data integrity.", icon="⚠️")
    
    if st.button(f"Delete Team #{selected_id} - {selected_team_data['name']}"):
        try:
            db.execute_change(ops.delete, params={"table_name": "teams", "team_id": selected_id})
            st.success("Team deleted successfully!")
            st.rerun()
        except db.RuleViolation as e:
            st.error(f"Could not delete team: {e}. (This is likely because the team is assigned to a past or future session).")