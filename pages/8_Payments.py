import streamlit as st
import pandas as pd
from datetime import date
import db
import db_operations as ops

st.set_page_config(layout="wide")
st.title("Manage Payments")

# --- CREATE ---
st.header("Record a New Payment")

members = db.execute_query(ops.get_all_members_with_details)
if not members:
    st.warning("No members found. Please add members on the 'Club Members' page first.")
    st.stop()

# Create a mapping for the member selection dropdown
member_map = {f"#{m['club_member_id']} - {m['first_name']} {m['last_name']} ({m['activity_status']})": m['club_member_id'] for m in members}
label = st.selectbox("Select Member", list(member_map.keys()))
mid = member_map[label]

# Form for new payment
with st.form("new_payment_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("Membership Year", min_value=2020, max_value=2100, value=date.today().year)
    with col2:
        amount = st.number_input("Payment Amount ($)", min_value=0.01, step=10.0, format="%.2f")
    with col3:
        method = st.selectbox("Payment Method", ["Cash", "Debit Card", "Credit Card"])
    
    submitted = st.form_submit_button("Record Payment")
    if submitted:
        try:
            params = {
                "club_member_id": mid, "payment_date": date.today(), "amount": amount,
                "method": method, "membership_year": year
            }
            db.execute_change(ops.add_payment, params=params)
            st.success("Payment recorded successfully. Member status may have been updated by a database trigger.")
            st.rerun()
        except db.RuleViolation as e:
            # This will catch our 4-installment limit trigger
            st.error(f"Could not record payment: {e}")

st.divider()

# --- READ ---
st.header("View Fee & Donation History")
st.write("This table shows a summary of payments, required fees, and calculated donations for the selected member for each year.")

# Use our dedicated backend function to get the fee history
fee_data = db.execute_query(ops.get_payments_and_fees_for_member, params={"club_member_id": mid})
if fee_data:
    df = pd.DataFrame(fee_data)
    # Reorder columns for better readability
    df = df[['membership_year', 'age_in_year', 'required_fee', 'total_paid', 'donation']]
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No payment records found for this member.")

st.divider()

# --- DEMO ACTION ---
st.header("System Actions")
st.subheader("Force Recalculate Member Status")
st.warning("For demo purposes. This action calls a stored procedure that iterates through ALL members and updates their `activity_status` based on their total payments for the selected year. This is useful for correcting any inconsistencies.", icon="⚙️")

recalc_year = st.number_input("Select Year to Recalculate", min_value=2020, max_value=2100, value=date.today().year, key="recalc_year")
if st.button("Run Status Recalculation"):
    with st.spinner(f"Recalculating statuses for {recalc_year}..."):
        try:
            db.execute_change(ops.recalculate_all_member_statuses, params={"membership_year": recalc_year})
            st.success(f"Recalculation complete for {recalc_year}! The member list on the 'Club Members' page is now up-to-date.")
            st.balloons()
        except db.RuleViolation as e:
            st.error(f"Could not run recalculation: {e}")