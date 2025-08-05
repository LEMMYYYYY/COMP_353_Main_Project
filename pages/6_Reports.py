import streamlit as st
import pandas as pd
import db # Use our new bridge

st.title("Reports")

st.subheader("Location Overview")
# NEW: Execute the raw SQL from the UI file via our bridge
sql1 = """
SELECT l.province, l.city, l.name,
       SUM(CASE WHEN TIMESTAMPDIFF(YEAR, p.dob, CURDATE()) < 18 THEN 1 ELSE 0 END) AS minors,
       SUM(CASE WHEN TIMESTAMPDIFF(YEAR, p.dob, CURDATE()) >= 18 THEN 1 ELSE 0 END) AS majors,
       (SELECT COUNT(DISTINCT st.team_id) FROM session_teams st JOIN sessions s ON s.session_id = st.session_id WHERE s.location_id = l.location_id) AS teams_here
FROM locations l
LEFT JOIN location_assignment la ON la.location_id = l.location_id AND la.end_date IS NULL
LEFT JOIN club_member m ON m.club_member_id = la.person_id
LEFT JOIN person p ON p.person_id = m.person_id
GROUP BY l.location_id
ORDER BY l.province, l.city, l.name;
"""
try:
    df1 = pd.DataFrame(db.execute_raw_sql(sql1))
    st.dataframe(df1, use_container_width=True)
except Exception as e:
    st.error(f"Error running location report: {e}")

st.subheader("Sessions in Period Report")
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Report Start Date")
with col2:
    end = st.date_input("Report End Date")

# This query is highly specific for reporting, so keeping it here is fine.
sql2 = """
SELECT s.session_id, s.type as session_type, s.date_time, s.final_score,
       t.name AS team_name, t.team_gender,
       p.first_name, p.last_name, f.player_position
FROM sessions s
JOIN session_teams st ON s.session_id = st.session_id
JOIN teams t ON st.team_id = t.team_id
LEFT JOIN formations f ON s.session_id = f.session_id AND t.team_id = f.team_id
LEFT JOIN person p ON f.player_id = p.person_id
WHERE DATE(s.date_time) BETWEEN %(start)s AND %(end)s
ORDER BY s.date_time, t.name, p.last_name;
"""

if st.button("Run Sessions Report"):
    try:
        # Use the raw SQL executor from our bridge
        df2 = pd.DataFrame(db.execute_raw_sql(sql2, {"start": start, "end": end}))
        st.dataframe(df2, use_container_width=True)
    except Exception as e:
        st.error(f"Error running sessions report: {e}")