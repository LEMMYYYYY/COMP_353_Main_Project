import streamlit as st
import pandas as pd
from datetime import date, timedelta
import db
import db_operations as ops

st.title("Weekly Emails")

# The Stored Procedure logic can remain, but we'll call it via our bridge
def execute_sp(start, end, sender):
    # This is a special case where we need to execute a raw CALL statement
    # We can use a simple helper for this one-off case
    from db_connector import get_db_connection
    conn = get_db_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        cursor.callproc('sp_generate_emails_for_period', (start, end, sender))
        conn.commit()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("Start Date", value=date.today())
with col2:
    end_date = st.date_input("End Date", value=date.today() + timedelta(days=7))
with col3:
    sender_id = st.number_input("Sender Location ID", min_value=1, step=1)

if st.button("Generate Weekly Emails"):
    try:
        execute_sp(start_date, end_date, sender_id)
        st.success("Email generation procedure executed successfully.")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Failed to execute procedure: {e}")

st.subheader("Email Log")
# NEW: Use our generic search to view the log
emails = db.execute_query(ops.search, params={"table_name": "emails"})
if emails:
    st.dataframe(pd.DataFrame(emails), use_container_width=True)
else:
    st.info("Email log is empty.")