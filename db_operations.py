import mysql.connector
from mysql.connector import Error
from db_connector import get_db_connection

# =================================================================
# GENERIC INSERT, UPDATE, AND DELETE FUNCTION
# =================================================================

def search(table_name, **criteria):
    """
    Performs a generic SELECT query on a table based on a set of criteria.
    
    Args:
        table_name (str): The name of the table to query.
        **criteria: Keyword arguments representing the WHERE clause (e.g., last_name='Smith').
        
    Returns:
        A list of dictionaries representing the matching rows.
    """
    conn = get_db_connection()
    if not conn: return []

    # Start with a base query
    query = f"SELECT * FROM {table_name}"
    params = []
    
    # Dynamically build the WHERE clause if criteria are provided
    if criteria:
        where_clauses = []
        for key, value in criteria.items():
            where_clauses.append(f"{key} = %s")
            params.append(value)
        query += " WHERE " + " AND ".join(where_clauses)
    
    results = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
    except Error as e:
        print(f"Error searching table {table_name}: {e}")
    finally:
        cursor.close()
        conn.close()
        
    return results

# --- Example Usage ---
# smiths_in_quebec = search('person', last_name='Smith', province='Quebec')
# all_locations = search('locations') # No criteria returns all rows
# head_location = search('locations', location_type='Head')

def update(table_name, criteria, new_data):
    """
    Performs a generic UPDATE on a table.
    
    Args:
        table_name (str): The name of the table to update.
        criteria (dict): A dictionary for the WHERE clause (e.g., {'person_id': 1}).
        new_data (dict): A dictionary of columns to update (e.g., {'phone_number': '...'}).
        
    Returns:
        True on success, False on failure.
    """
    conn = get_db_connection()
    # --- CRITICAL SAFETY CHECKS ---
    if not conn or not new_data or not criteria:
        print("Error: Update function requires criteria and new_data to proceed.")
        return False

    # Build the SET part of the query
    set_clauses = [f"{key} = %s" for key in new_data.keys()]
    set_string = ", ".join(set_clauses)
    
    # Build the WHERE part of the query
    where_clauses = [f"{key} = %s" for key in criteria.keys()]
    where_string = " AND ".join(where_clauses)

    query = f"UPDATE {table_name} SET {set_string} WHERE {where_string}"
    
    # The order of parameters is crucial: first the SET values, then the WHERE values.
    params = list(new_data.values()) + list(criteria.values())
    
    success = False
    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        conn.commit()
        # rowcount tells you how many rows were affected. Useful for verification.
        if cursor.rowcount > 0:
            print(f"Successfully updated {cursor.rowcount} row(s) in {table_name}.")
            success = True
        else:
            print(f"Warning: Update executed but no rows in {table_name} matched the criteria.")
    except Error as e:
        print(f"Error updating table {table_name}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        
    return success

# --- Example Usage ---
# update_success = update('person', {'person_id': 5}, {'phone_number': '514-111-2222'})

def delete(table_name, **criteria):
    """
    Performs a generic DELETE on a table based on a set of criteria.
    
    Args:
        table_name (str): The name of the table to delete from.
        **criteria: Keyword arguments representing the WHERE clause.
        
    Returns:
        True on success, False on failure.
    """
    conn = get_db_connection()
    # --- CRITICAL SAFETY CHECK ---
    if not conn or not criteria:
        print("Error: Delete function requires criteria to proceed to prevent deleting all rows.")
        return False
    
    query = f"DELETE FROM {table_name}"
    
    where_clauses = []
    params = []
    for key, value in criteria.items():
        where_clauses.append(f"{key} = %s")
        params.append(value)
    query += " WHERE " + " AND ".join(where_clauses)
    
    success = False
    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Successfully deleted {cursor.rowcount} row(s) from {table_name}.")
            success = True
        else:
            print(f"Warning: Delete executed but no rows in {table_name} matched the criteria.")
    except Error as e:
        print(f"Error deleting from table {table_name}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        
    return success

# --- Example Usage ---
# delete_success = delete('hobbies', hobby_name='Scuba Diving')

# =================================================================
# CREATE CORE ENTITIES
# =================================================================

def add_person(first_name, last_name, dob, gender, ssn=None, medicare_number=None, phone_number=None, address=None, city=None, province=None, postal_code=None, email_address=None):
    """Inserts a new person and returns their new person_id."""
    conn = get_db_connection()
    if not conn: return None
    
    sql = """INSERT INTO person (first_name, last_name, dob, gender, ssn, medicare_number, phone_number, address, city, province, postal_code, email_address)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    data = (first_name, last_name, dob, gender, ssn, medicare_number, phone_number, address, city, province, postal_code, email_address)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Successfully added Person: {first_name} {last_name} with ID: {new_id}")
        return new_id
    except Error as e:
        print(f"Error adding Person: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_club_member(club_member_id, join_date, height=None, weight=None, activity_status='Active'):
    """Inserts a new club_member, linking to an existing person_id."""
    conn = get_db_connection()
    if not conn: return False

    sql = """INSERT INTO club_member (club_member_id, height, weight, activity_status, join_date)
             VALUES (%s, %s, %s, %s, %s)"""
    data = (club_member_id, height, weight, activity_status, join_date)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print(f"Successfully converted Person ID: {club_member_id} into a Club Member.")
        return True
    except Error as e:
        print(f"Error adding Club Member: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def add_location(name, location_type, address=None, city=None, province=None, postal_code=None, web_address=None, max_capacity=None):
    """Inserts a new location and returns its new location_id."""
    conn = get_db_connection()
    if not conn: return None
    
    sql = """INSERT INTO locations (name, location_type, address, city, province, postal_code, web_address, max_capacity)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    data = (name, location_type, address, city, province, postal_code, web_address, max_capacity)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Successfully added Location: {name} with ID: {new_id}")
        return new_id
    except Error as e:
        print(f"Error adding Location: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_hobby(hobby_name, description=None):
    """Inserts a new hobby and returns its new hobby_id."""
    conn = get_db_connection()
    if not conn: return None
    
    sql = "INSERT INTO hobbies (hobby_name, description) VALUES (%s, %s)"
    data = (hobby_name, description)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Successfully added Hobby: {hobby_name} with ID: {new_id}")
        return new_id
    except Error as e:
        print(f"Error adding Hobby: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_payment(club_member_id, payment_date, amount, method, membership_year):
    """Inserts a new payment record and returns its new payment_id."""
    conn = get_db_connection()
    if not conn: return None

    sql = """INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year)
             VALUES (%s, %s, %s, %s, %s)"""
    data = (club_member_id, payment_date, amount, method, membership_year)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Successfully added Payment of ${amount} for member ID: {club_member_id}")
        return new_id
    except Error as e:
        print(f"Error adding Payment: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_team(name, home_location_id, team_gender):
    """Inserts a new team and returns its new team_id."""
    conn = get_db_connection()
    if not conn: return None

    sql = "INSERT INTO teams (name, home_location_id, team_gender) VALUES (%s, %s, %s)"
    data = (name, home_location_id, team_gender)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Successfully added Team: {name} with ID: {new_id}")
        return new_id
    except Error as e:
        print(f"Error adding Team: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_session(session_type, date_time, location_id, final_score=None):
    """Inserts a new session and returns its new session_id."""
    conn = get_db_connection()
    if not conn: return None

    sql = "INSERT INTO sessions (type, date_time, location_id, final_score) VALUES (%s, %s, %s, %s)"
    data = (session_type, date_time, location_id, final_score)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Successfully added {session_type} Session at {date_time} with ID: {new_id}")
        return new_id
    except Error as e:
        print(f"Error adding Session: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_formation(session_id, team_id, player_id, player_position):
    """Inserts a new player formation record."""
    conn = get_db_connection()
    if not conn: return False

    sql = "INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES (%s, %s, %s, %s)"
    data = (session_id, team_id, player_id, player_position)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print(f"Successfully added Player ID {player_id} to formation for Session ID {session_id}")
        return True
    except Error as e:
        print(f"Error adding Formation: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
        
def add_email(sender_name, receiver_email, subject, body=None, session_id=None):
    """Logs a sent email to the database."""
    conn = get_db_connection()
    if not conn: return False

    sql = "INSERT INTO emails (sender_name, receiver_email, email_subject, body, session_id) VALUES (%s, %s, %s, %s, %s)"
    data = (sender_name, receiver_email, subject, body, session_id)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print(f"Successfully logged email to {receiver_email}")
        return True
    except Error as e:
        print(f"Error logging Email: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# =================================================================
# ASSIGN RELATIONSHIPS (LINK TABLES)
# =================================================================

def link_family_to_member(club_member_id, family_member_id, relationship_type, contact_priority):
    """Creates a family link between a club member and a person."""
    conn = get_db_connection()
    if not conn: return False

    sql = """INSERT INTO club_member_family_link (club_member_id, family_member_id, relationship_type, contact_priority)
             VALUES (%s, %s, %s, %s)"""
    data = (club_member_id, family_member_id, relationship_type, contact_priority)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print(f"Successfully linked Member ID {club_member_id} to Family Member ID {family_member_id}")
        return True
    except Error as e:
        print(f"Error creating Family Link: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def assign_person_to_location(person_id, location_id, start_date, end_date=None, personnel_role=None, mandate=None):
    """Creates a location assignment for a person, optionally with a role."""
    conn = get_db_connection()
    if not conn: return False
    
    sql = """INSERT INTO location_assignment (person_id, location_id, start_date, end_date, personnel_role, mandate)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    data = (person_id, location_id, start_date, end_date, personnel_role, mandate)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Successfully assigned Person ID {person_id} to Location ID {location_id} with Assignment ID: {new_id}")
        return new_id
    except Error as e:
        print(f"Error creating Location Assignment: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_hobby_to_member(club_member_id, hobby_id):
    """Links a hobby to a club member."""
    conn = get_db_connection()
    if not conn: return False
    
    sql = "INSERT INTO club_member_hobbies (club_member_id, hobby_id) VALUES (%s, %s)"
    data = (club_member_id, hobby_id)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print(f"Successfully linked Hobby ID {hobby_id} to Member ID {club_member_id}")
        return True
    except Error as e:
        print(f"Error adding hobby to member: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
        
def add_team_to_session(session_id, team_id):
    """Links a team to a session."""
    conn = get_db_connection()
    if not conn: return False
    
    sql = "INSERT INTO session_teams (session_id, team_id) VALUES (%s, %s)"
    data = (session_id, team_id)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print(f"Successfully linked Team ID {team_id} to Session ID {session_id}")
        return True
    except Error as e:
        print(f"Error adding team to session: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def add_location_phone_number(location_id, phone_number):
    """Adds a phone number to a specific location."""
    conn = get_db_connection()
    if not conn: return False

    sql = "INSERT INTO location_phone_numbers (location_id, phone_number) VALUES (%s, %s)"
    data = (location_id, phone_number)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print(f"Successfully added phone number {phone_number} to Location ID {location_id}")
        return True
    except Error as e:
        print(f"Error adding location phone number: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
        
# =================================================================
# ENRICHED QUERY FUNCTIONS (for UI display)
# =================================================================

def get_all_locations_with_phones():
    """
    Retrieves all locations and aggregates their phone numbers into a single string.
    This is more efficient than running a separate query for each location's phones.
    """
    conn = get_db_connection()
    if not conn: return []
    
    # GROUP_CONCAT is a handy SQL function for this exact purpose.
    sql = """
        SELECT 
            l.*, 
            GROUP_CONCAT(lp.phone_number SEPARATOR ', ') AS phone_numbers
        FROM locations l
        LEFT JOIN location_phone_numbers lp ON l.location_id = lp.location_id
        GROUP BY l.location_id
        ORDER BY l.name;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting all locations: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all_members_with_details():
    """
    Retrieves a list of all club members with essential person details for display.
    This replaces the UI needing to do a complex JOIN.
    """
    conn = get_db_connection()
    if not conn: return []

    sql = """
        SELECT
            cm.club_member_id,
            p.first_name,
            p.last_name,
            p.email_address,
            cm.activity_status,
            l.name AS current_location
        FROM club_member cm
        JOIN person p ON cm.club_member_id = p.person_id
        LEFT JOIN location_assignment la ON p.person_id = la.person_id AND la.end_date IS NULL
        LEFT JOIN locations l ON la.location_id = l.location_id
        ORDER BY p.last_name, p.first_name;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting all members: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_member_profile(club_member_id):
    """Retrieves a full, detailed profile for a single member."""
    conn = get_db_connection()
    if not conn: return None
    
    sql = """
        SELECT
            p.person_id, p.first_name, p.last_name, p.dob, p.gender,
            p.email_address, p.phone_number, p.address, p.city, p.province, p.postal_code,
            p.ssn, p.medicare_number,
            cm.height, cm.weight, cm.activity_status, cm.join_date,
            l.name AS current_location
        FROM person p
        JOIN club_member cm ON p.person_id = cm.club_member_id
        LEFT JOIN location_assignment la ON p.person_id = la.person_id AND la.end_date IS NULL
        LEFT JOIN locations l ON la.location_id = l.location_id
        WHERE p.person_id = %s;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (club_member_id,))
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Error getting member profile: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_sessions_with_details():
    """Retrieves a summary of all sessions for display in a dropdown."""
    conn = get_db_connection()
    if not conn: return []

    sql = """
        SELECT
            s.session_id,
            s.type,
            s.date_time,
            l.name AS location_name
        FROM sessions s
        JOIN locations l ON s.location_id = l.location_id
        ORDER BY s.date_time DESC;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting all sessions: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_teams_for_session(session_id):
    """Retrieves the details of teams attached to a specific session."""
    conn = get_db_connection()
    if not conn: return []

    sql = "SELECT t.* FROM teams t JOIN session_teams st ON t.team_id = st.team_id WHERE st.session_id = %s"
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (session_id,))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting teams for session: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_roster_for_formation(session_id, team_id):
    """Retrieves the player roster for a specific team within a session."""
    conn = get_db_connection()
    if not conn: return []

    sql = """
        SELECT
            p.first_name,
            p.last_name,
            f.player_position
        FROM formations f
        JOIN person p ON f.player_id = p.person_id
        WHERE f.session_id = %s AND f.team_id = %s;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (session_id, team_id))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting roster for formation: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_eligible_players_for_team(team_id):
    """
    Finds all active club members whose gender matches the specified team's gender,
    making them eligible to be added to the roster.
    """
    conn = get_db_connection()
    if not conn: return []
    
    # This query first finds the gender of the target team in a subquery,
    # then finds all active members who match that gender.
    sql = """
        SELECT
            p.person_id AS club_member_id,
            p.first_name,
            p.last_name
        FROM club_member cm
        JOIN person p ON cm.club_member_id = p.person_id
        WHERE
            cm.activity_status = 'Active'
            AND p.gender = (SELECT team_gender FROM teams WHERE team_id = %s)
        ORDER BY p.last_name, p.first_name;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (team_id,))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting eligible players: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_payments_and_fees_for_member(club_member_id):
    """
    Calculates the total payments, required fees, and donations for a member
    across all years they have been active.
    """
    conn = get_db_connection()
    if not conn: return []

    # This query is complex. It calculates the required fee based on the member's age
    # IN THAT SPECIFIC YEAR, then aggregates payments and calculates donations.
    sql = """
        SELECT
            p.membership_year,
            TIMESTAMPDIFF(YEAR, pr.dob, MAKEDATE(p.membership_year, 1)) AS age_in_year,
            CASE
                WHEN TIMESTAMPDIFF(YEAR, pr.dob, MAKEDATE(p.membership_year, 1)) >= 18 THEN 200.00
                ELSE 100.00
            END AS required_fee,
            SUM(p.amount) AS total_paid,
            GREATEST(0, SUM(p.amount) - 
                CASE
                    WHEN TIMESTAMPDIFF(YEAR, pr.dob, MAKEDATE(p.membership_year, 1)) >= 18 THEN 200.00
                    ELSE 100.00
                END
            ) AS donation
        FROM payments p
        JOIN person pr ON p.club_member_id = pr.person_id
        WHERE p.club_member_id = %s
        GROUP BY p.membership_year, pr.dob
        ORDER BY p.membership_year DESC;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (club_member_id,))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting fee records for member: {e}")
        return []
    finally:
        cursor.close()
        conn.close()