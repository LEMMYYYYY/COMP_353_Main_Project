import streamlit as st
import db
import db_operations as ops
from datetime import datetime

st.title("Sessions, Teams & Rosters")

# --- Step 1: Create a Session ---
with st.expander("Step 1: Create a New Session", expanded=True):
    locations = db.execute_query(ops.get_all_locations_with_phones)
    if not locations:
        st.warning("No locations found. Please add a location first.")
        st.stop()
        
    loc_map = {f"{l['name']} ({l['city']})": l['location_id'] for l in locations}
    
    col1, col2 = st.columns(2)
    with col1:
        session_type = st.selectbox("Session Type", ["Game", "Training"])
        loc_label = st.selectbox("Location", list(loc_map.keys()))
    with col2:
        date_time = st.datetime_input("Start Date & Time", value=datetime.now())

    if st.button("Create Session"):
        try:
            # NEW: Call our specific add_session function
            new_session_id = db.execute_change(ops.add_session, params={
                "session_type": session_type,
                "date_time": date_time,
                "location_id": loc_map[loc_label]
            })
            st.success(f"Session created with ID: {new_session_id}. Please select it below to continue.")
            st.experimental_rerun()
        except db.RuleViolation as e:
            st.error(f"Could not create session: {e}")

st.divider()

# --- Step 2: Manage an Existing Session ---
sessions = db.execute_query(ops.get_all_sessions_with_details)
if not sessions:
    st.info("No sessions created yet.")
    st.stop()

session_options = {f"#{s['session_id']} - {s['type']} @ {s['date_time']} ({s['location_name']})": s['session_id'] for s in sessions}
selected_session_label = st.selectbox("Select a Session to Manage", session_options.keys())
sid = session_options[selected_session_label]

st.subheader(f"Managing Session #{sid}")

# --- Part 2a: Attach Teams ---
st.markdown("#### Attach Teams")
teams_in_session = db.execute_query(ops.get_teams_for_session, params={"session_id": sid})
if teams_in_session:
    st.write("Teams already in session:", [t['name'] for t in teams_in_session])
else:
    st.write("No teams attached yet.")

with st.form("add_team_form"):
    team_name = st.text_input("New Team Name")
    team_gender = st.selectbox("Team Gender", ["Male", "Female"])
    submitted = st.form_submit_button("Create & Attach Team")
    if submitted:
        try:
            # NEW: Use a transactional approach. Create the team, then link it.
            # We assume the home location is the same as the session location for simplicity here.
            session_info = db.execute_query(ops.search, params={"table_name": "sessions", "session_id": sid})[0]
            
            new_team_id = db.execute_change(ops.add_team, params={
                "name": team_name,
                "home_location_id": session_info['location_id'],
                "team_gender": team_gender
            })
            
            db.execute_change(ops.add_team_to_session, params={"session_id": sid, "team_id": new_team_id})
            st.success(f"Team '{team_name}' created and attached to session.")
            st.experimental_rerun()
        except db.RuleViolation as e:
            st.error(f"Could not add team: {e}")

# --- Part 2b: Manage Roster ---
st.markdown("#### Manage Roster")
teams_in_session = db.execute_query(ops.get_teams_for_session, params={"session_id": sid})
if len(teams_in_session) > 0:
    team_map = {t['name']: t['team_id'] for t in teams_in_session}
    selected_team_name = st.selectbox("Select Team to Add Players To", team_map.keys())
    selected_team_id = team_map[selected_team_name]

    st.markdown("##### Current Roster")
    roster = db.execute_query(ops.get_roster_for_formation, params={"session_id": sid, "team_id": selected_team_id})
    st.table(roster)

    st.markdown("##### Add Player to Roster")
    eligible_players = db.execute_query(ops.get_eligible_players_for_team, params={"team_id": selected_team_id})
    if eligible_players:
        player_map = {f"{p['first_name']} {p['last_name']}": p['club_member_id'] for p in eligible_players}
        player_name = st.selectbox("Eligible Player", player_map.keys())
        player_pos = st.selectbox("Position", ["Setter", "Outside Hitter", "Opposite Hitter", "Middle Blocker", "Defensive Specialist", "Libero"])
        
        if st.button("Add Player"):
            try:
                db.execute_change(ops.add_formation, params={
                    "session_id": sid,
                    "team_id": selected_team_id,
                    "player_id": player_map[player_name],
                    "player_position": player_pos
                })
                st.success(f"Added {player_name} to the roster.")
                st.experimental_rerun()
            except db.RuleViolation as e:
                st.error(f"Could not add player: {e}")
    else:
        st.info("No eligible players found for this team (check gender or activity status).")
else:
    st.info("Attach at least one team to manage its roster.")