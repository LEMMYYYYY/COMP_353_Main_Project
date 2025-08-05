import streamlit as st
import pandas as pd
import db
import db_operations as ops

st.title("Members")

# NEW: Use our enriched function to get the member list
data = db.execute_query(ops.get_all_members_with_details)
st.dataframe(pd.DataFrame(data), use_container_width=True)

st.subheader("View Member Profile")
mid = st.number_input("Enter Membership #", min_value=1, step=1, key="profile_mid")
if st.button("Load Profile"):
    # NEW: Use our dedicated profile getter
    profile = db.execute_query(ops.get_member_profile, params={"club_member_id": mid})
    if profile:
        st.json(profile)
    else:
        st.warning("Member not found.")

st.subheader("Assign Member to a New Location")
assign_mid = st.number_input("Enter Membership # to move", min_value=1, step=1, key="assign_mid")

# NEW: Use our locations getter for the dropdown
locations = db.execute_query(ops.get_all_locations_with_phones)
if locations:
    loc_map = {f"{l['name']} ({l['city']})": l['location_id'] for l in locations}
    sel_loc = st.selectbox("Select New Location", list(loc_map.keys()))
    start_date = st.date_input("Start Date of Assignment")

    if st.button("Apply Location Change"):
        try:
            # NEW: Call our specific assignment function
            params = {
                "person_id": assign_mid,
                "location_id": loc_map[sel_loc],
                "start_date": start_date
            }
            db.execute_change(ops.assign_person_to_location, params=params)
            st.success("Location assignment added successfully.")
        except db.RuleViolation as e:
            st.error(f"Could not assign location: {e}")
else:
    st.info("No locations available to assign to.")