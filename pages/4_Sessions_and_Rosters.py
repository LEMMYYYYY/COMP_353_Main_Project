# pages/4_Sessions_and_Rosters.py (Corrected)

import streamlit as st
import pandas as pd
import db
import db_operations as ops
from datetime import datetime, date, time

st.set_page_config(layout="wide")
st.title("Manage Sessions, Teams, and Rosters")

# --- CREATE NEW SESSION ---
with st.expander("➕ Create a New Session"):
    with st.form("new_session_form", clear_on_submit=True):
        locations = db.execute_query(ops.get_all_locations_with_phones)
        if not locations:
            st.error("Cannot create a session without at least one location. Please add a location first.")
        else:
            loc_map = {f"{l['name']} ({l['city']})": l['location_id'] for l in locations}
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                session_type = st.selectbox("Session Type", ["Game", "Training"])
            with col2:
                loc_label = st.selectbox("Location", loc_map.keys())
            with col3:
                start_date_val = st.date_input("Start Date", value=date.today())
            with col4:
                start_time_val = st.time_input("Start Time", value=datetime.now().time())
            
            date_time = datetime.combine(start_date_val, start_time_val)

            submitted = st.form_submit_button("Create Session")
            if submitted:
                try:
                    db.execute_change(ops.add_session, params={
                        "session_type": session_type, "date_time": date_time, "location_id": loc_map[loc_label]
                    })
                    st.success("Session created successfully! Select it from the list below to manage it.")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Could not create session: {e}")

st.divider()

# --- READ (Master List) ---
st.header("Master Session List")
sessions = db.execute_query(ops.get_all_sessions_for_dashboard)
if not sessions:
    st.info("No sessions found. Use the form above to create one.")
    st.stop()

st.dataframe(pd.DataFrame(sessions), use_container_width=True, hide_index=True)

# --- MANAGE A SPECIFIC SESSION ---
st.header("Manage a Specific Session")
session_options = {f"#{s['session_id']} - {s['teams_involved'] or 'No Teams'} @ {s['date_time']}": s['session_id'] for s in sessions}
selected_label = st.selectbox("Select a Session to Manage", session_options.keys())
sid = session_options[selected_label]

st.subheader(f"Dashboard for Session #{sid}")

tab1, tab2, tab3 = st.tabs(["👥 Teams", "📝 Rosters & Formations", "⚙️ Details & Score"])

# --- Tab 1: Manage Teams ---
with tab1:
    st.write("#### Manage Teams for this Session")
    teams_in_session = db.execute_query(ops.get_teams_for_session, params={"session_id": sid})
    
    if not teams_in_session:
        st.info("No teams are attached to this session yet.")
    else:
        for team in teams_in_session:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{team['name']}** ({team['team_gender']})")
            with col2:
                if st.button("Detach", key=f"detach_{team['team_id']}"):
                    try:
                        db.execute_change(ops.detach_team_from_session, params={"session_id": sid, "team_id": team['team_id']})
                        st.success(f"Team '{team['name']}' detached.")
                        st.rerun()
                    except db.RuleViolation as e:
                        st.error(f"Could not detach team: {e}")
    
    st.write("##### Attach a New Team")
    all_teams = db.execute_query(ops.get_all_teams_with_details)
    attached_team_ids = {t['team_id'] for t in teams_in_session}
    
    available_teams = [t for t in all_teams if t['team_id'] not in attached_team_ids]
    
    if not available_teams:
        st.warning("No other available teams to attach. Create a new team on the 'Teams' page.")
    else:
        team_map = {f"#{t['team_id']} - {t['name']}": t['team_id'] for t in available_teams}
        team_to_add_label = st.selectbox("Select a team to attach", team_map.keys())
        
        if st.button("Attach Team to Session"):
            try:
                db.execute_change(ops.add_team_to_session, params={"session_id": sid, "team_id": team_map[team_to_add_label]})
                st.success("Team attached.")
                st.rerun()
            except db.RuleViolation as e:
                st.error(f"Could not attach team: {e}")

# --- Tab 2: Manage Rosters & Formations ---
with tab2:
    st.write("#### Manage Player Formations")
    teams_in_session = db.execute_query(ops.get_teams_for_session, params={"session_id": sid})
    if len(teams_in_session) == 0:
        st.info("You must attach at least one team to manage its roster.")
    else:
        team_map = {t['name']: t['team_id'] for t in teams_in_session}
        team_name = st.selectbox("Select Team Roster", team_map.keys(), key="roster_team_select")
        tid = team_map[team_name]

        st.write(f"##### Roster for **{team_name}**")
        roster = db.execute_query(ops.get_roster_for_formation, params={"session_id": sid, "team_id": tid})
        st.table(roster)

        st.write("##### Add Player to Roster")
        eligible_players = db.execute_query(ops.get_eligible_players_for_team, params={"team_id": tid})
        if not eligible_players:
            st.warning("No eligible players found for this team. Check player gender and member status.")
        else:
            player_map = {f"{p['first_name']} {p['last_name']}": p['club_member_id'] for p in eligible_players}
            player_label = st.selectbox("Select Eligible Player", player_map.keys())
            position = st.selectbox("Assign Position", ["Setter", "Outside Hitter", "Opposite Hitter", "Middle Blocker", "Defensive Specialist", "Libero"])
            
            if st.button("Add Player to Formation"):
                try:
                    db.execute_change(ops.add_formation, params={
                        "session_id": sid, "team_id": tid, "player_id": player_map[player_label], "player_position": position
                    })
                    st.success("Player added to formation.")
                    st.rerun()
                except db.RuleViolation as e:
                    st.error(f"Could not add player: {e}")

# --- Tab 3: Edit Details & Score ---
with tab3:
    st.write("#### Edit Session Details")
    session_data = db.execute_query(ops.search, params={"table_name": "sessions", "session_id": sid})[0]
    
    with st.form("update_session_form"):
        col_d, col_t = st.columns(2)
        with col_d:
            new_date = st.date_input("New Date", value=session_data['date_time'].date())
        with col_t:
            new_time = st.time_input("New Time", value=session_data['date_time'].time())
        new_datetime = datetime.combine(new_date, new_time)
        
        final_score = st.text_input("Final Score", value=session_data['final_score'], help="e.g., '3-1' or '25-23, 25-21'")
        
        submitted = st.form_submit_button("Save Session Details")
        if submitted:
            try:
                db.execute_change(ops.update, params={
                    "table_name": "sessions",
                    "criteria": {"session_id": sid},
                    "new_data": {"date_time": new_datetime, "final_score": final_score}
                })
                st.success("Session details updated.")
                st.rerun()
            except db.RuleViolation as e:
                st.error(f"Could not update details: {e}")