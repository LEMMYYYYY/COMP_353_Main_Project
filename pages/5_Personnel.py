import streamlit as st
import pandas as pd
import db
import db_operations as ops
from datetime import date

st.set_page_config(layout="wide")
st.title("Manage Personnel Assignments")

# --- CREATE (Assign a new role to a person) ---
with st.expander("➕ Assign a New Role to a Person"):
    with st.form("new_assignment_form", clear_on_submit=True):
        st.subheader("New Assignment Details")
        
        # Dependency Checks: Need people and locations to make an assignment
        all_people = db.execute_query(ops.search, params={"table_name": "person"})
        all_locations = db.execute_query(ops.get_all_locations_with_phones)

        if not all_people or not all_locations:
            st.error("You must have at least one person and one location in the system to create an assignment.")
        else:
            person_options = {f"#{p['person_id']} - {p['first_name']} {p['last_name']}": p['person_id'] for p in all_people}
            location_options = {f"{l['name']} ({l['city']})": l['location_id'] for l in all_locations}
            role_options = ["Administrator", "Captain", "Coach", "Assistant Coach", "Manager", "General Manager", "Deputy Manager", "Treasurer", "Secretary"]
            mandate_options = ["Volunteer", "Salaried"]

            col1, col2 = st.columns(2)
            with col1:
                person_label = st.selectbox("Select Person*", person_options.keys())
                role = st.selectbox("Assign Role*", role_options)
                start_date = st.date_input("Start Date*", value=date.today())
            with col2:
                location_label = st.selectbox("Select Location*", location_options.keys())
                mandate = st.selectbox("Select Mandate*", mandate_options)

            submitted = st.form_submit_button("Create Assignment")
            if submitted:
                try:
                    db.execute_change(ops.assign_person_to_location, params={
                        "person_id": person_options[person_label],
                        "location_id": location_options[location_label],
                        "start_date": start_date,
                        "personnel_role": role,
                        "mandate": mandate
                    })
                    st.success("Personnel assignment created successfully!")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Error creating assignment: {e}")

st.divider()

# --- READ / UPDATE (End Assignment) ---
st.header("Current Active Personnel Assignments")
st.info("To edit an assignment, end the current one and create a new one with the updated details. This preserves the work history.")

assignments = db.execute_query(ops.get_current_personnel_assignments)

if not assignments:
    st.info("No active personnel assignments found.")
else:
    df = pd.DataFrame(assignments)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("End an Assignment")
    assignment_options = {f"#{a['assignment_id']}: {a['first_name']} {a['last_name']} @ {a['location_name']} (as {a['personnel_role']})": a['assignment_id'] for a in assignments}
    selected_label = st.selectbox("Select assignment to end", assignment_options.keys())
    selected_id = assignment_options[selected_label]

    if st.button("End This Assignment"):
        try:
            update_data = {"end_date": date.today()}
            criteria = {"assignment_id": selected_id}
            db.execute_change(ops.update, params={"table_name": "location_assignment", "criteria": criteria, "new_data": update_data})
            st.success("Assignment ended successfully.")
            st.rerun()
        except db.RuleViolation as e:
            st.error(f"Could not end assignment: {e}")