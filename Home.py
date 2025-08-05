import streamlit as st

st.set_page_config(page_title="MVC Admin", layout="wide")
st.title("Montreal Volleyball Club - Admin")
st.markdown(
    """
This is a demonstration of the database application system for the Montréal Volleyball Club (MVC).

**Use the sidebar to navigate the application:**

- **Locations:** View all club locations and manage their phone numbers.
- **Members:** View a list of all members, search for a specific member profile, and manage their location assignments.
- **Sessions:** A multi-step workflow to create new sessions, create and attach teams, and build a roster for a game or training.
- **Payments:** Record new payments for members and view their fee and donation history.
- **Emails:** Generate weekly schedule emails and view the email log.
- **Reports:** View pre-defined complex reports about the club's operations.

This UI is connected to a robust Python backend that interacts with a MySQL database.
Database triggers are used to enforce complex business rules. You can test these rules directly through the UI:

- **SSN Checks:** Try to create a member or assign a personnel role without an SSN.
- **Session Time Conflicts:** Try to assign a player to two sessions less than 3 hours apart.
- **Gender Consistency:** Try to assign a male player to a female team.
- **Payment Limits:** Try to make more than 4 payments for a member in a single year.
- **Team Limits:** Try to attach more than two teams to a single session.
"""
)