import streamlit as st
import pandas as pd
from datetime import date
import db
import db_operations as ops

st.title("Record Payments")

# NEW: Use our enriched member details getter
members = db.execute_query(ops.get_all_members_with_details)
if not members:
    st.warning("No members found. Please add members first.")
    st.stop()
    
member_map = {f"#{m['club_member_id']} - {m['first_name']} {m['last_name']} ({m['activity_status']})": m['club_member_id'] for m in members}
label = st.selectbox("Select Member", list(member_map.keys()))
mid = member_map[label]

col1, col2, col3 = st.columns(3)
with col1:
    year = st.number_input("Membership Year", min_value=2020, max_value=2100, value=date.today().year)
with col2:
    amount = st.number_input("Payment Amount", min_value=0.0, step=10.0)
with col3:
    method = st.selectbox("Payment Method", ["Cash", "Debit Card", "Credit Card"])

if st.button("Record Payment"):
    try:
        # NEW: Call our specific backend function
        params = {
            "club_member_id": mid,
            "payment_date": date.today(),
            "amount": amount,
            "method": method,
            "membership_year": year
        }
        db.execute_change(ops.add_payment, params=params)
        st.success("Payment recorded. Member status may have been updated by a database trigger.")
        st.experimental_rerun()
    except db.RuleViolation as e:
        st.error(f"Could not record payment: {e}")

st.divider()
st.subheader("Fee & Donation History")
if mid:
    # NEW: Call our dedicated fee calculation function
    fee_data = db.execute_query(ops.get_payments_and_fees_for_member, params={"club_member_id": mid})
    if fee_data:
        df = pd.DataFrame(fee_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No payment records found for this member.")