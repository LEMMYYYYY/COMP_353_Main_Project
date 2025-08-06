import streamlit as st
import pandas as pd
import db
import db_operations as ops

st.set_page_config(layout="wide")
st.title("Manage All People")

st.info("This is an admin-level page to view and manage every individual in the database, including club members, staff, and family contacts.")

all_people = db.execute_query(ops.search, params={"table_name": "person"})

if not all_people:
    st.warning("There are no people in the database.")
    st.stop()

df = pd.DataFrame(all_people)
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

st.header("🗑️ Delete a Person Record")
st.warning("Warning: Deleting a person is permanent. If they are an active club member or have other critical associations, the deletion will be blocked by the database.", icon="⚠️")

options = {f"#{p['person_id']} - {p['first_name']} {p['last_name']} ({p['email_address']})": p['person_id'] for p in all_people}
selected_label = st.selectbox("Select a person to permanently delete", options.keys())
selected_id = options[selected_label]

if st.button(f"Delete Person #{selected_id} from the System"):
    try:
        db.execute_change(ops.delete, params={"table_name": "person", "person_id": selected_id})
        st.success("Person record deleted successfully.")
        st.rerun()
    except db.RuleViolation as e:
        st.error(f"Could not delete person: {e}. (This often means they are still linked to a team, session, or other critical record that does not permit cascading deletes).")