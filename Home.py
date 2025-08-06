import streamlit as st
import db
import db_operations as ops

st.set_page_config(page_title="MVC Admin", layout="wide")

st.title("Montreal Volleyball Club - Admin Dashboard")

# --- NEW: DYNAMIC DASHBOARD METRICS ---
st.header("System at a Glance")

# Call our new backend function to get live data
metrics = db.execute_query(ops.get_dashboard_metrics)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Active Club Members", value=metrics.get('active_members', "N/A"))
with col2:
    st.metric(label="Total Club Locations", value=metrics.get('total_locations', "N/A"))
with col3:
    st.metric(label="Sessions in Next 7 Days", value=metrics.get('upcoming_sessions', "N/A"))

st.divider()

# --- REFINED GUIDE FOR DEMONSTRATION ---
st.header("Application Guide")
st.markdown(
    """
    This is a demonstration of the database application system for the Montréal Volleyball Club (MVC),
    built with a Python backend, a MySQL database, and a Streamlit user interface.
    """
)

st.subheader("Navigation")
st.markdown(
    """
    **Use the sidebar on the left to navigate the application's core modules:**

    - **`Locations`:** Manage the club's physical branches and their contact information.
    - **`Teams`:** Create and manage the master list of all teams in the club.
    - **`Club Members`:** A complete CRUD interface for registering members, updating profiles, and managing family links.
    - **`Personnel`:** Assign staff and coaches to locations and manage their roles.
    - **`Sessions & Rosters`:** A multi-step workflow to schedule sessions, attach teams, and build player rosters.
    - **`Payments`:** Record member payments and view their financial history.
    - **`Hobbies`:** Manage the master list of hobbies and assign them to members.
    - **`Emails`:** Generate and log weekly schedule emails for all members with upcoming sessions.
    - **`Reports`:** View pre-defined, complex reports on the club's operations.
    """
)

st.subheader("Demonstrating Database Integrity")
st.success(
    """
    This application is powered by a robust MySQL database with a series of **triggers and constraints** to enforce complex business rules.
    You can test these rules directly through the UI:
    """
)
st.markdown(
    """
    - **✅ SSN Checks:** On the `Club Members` or `Personnel` page, try to create a member or assign a staff role to a person without an SSN. The operation will be blocked by a trigger.
    - **✅ Session Time Conflicts:** On the `Sessions & Rosters` page, try to assign a player to two sessions that are less than 3 hours apart. The second assignment will be blocked.
    - **✅ Gender Consistency:** On the `Sessions & Rosters` page, try to assign a male player to a team designated as 'Female'. The trigger will prevent this.
    - **✅ Payment Limits:** On the `Payments` page, try to make more than 4 payments for a single member in the same year. The fifth payment will be rejected.
    - **✅ Team Limits:** On the `Sessions & Rosters` page, try to attach a third team to a session. The operation will fail.
    - **✅ Automatic Assignment End-Dating:** On the `Club Members` page, when you assign a member to a new location, the system automatically sets an `end_date` for their previous assignment.
    """
)