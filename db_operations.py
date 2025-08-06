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

def assign_person_to_location(person_id, location_id, start_date, personnel_role=None, mandate=None):
    """
    Creates a new location assignment for a person.
    This is a transactional function that first ends any previous active assignment
    for the person before creating the new one.
    """
    conn = get_db_connection()
    if not conn: return None
    
    try:
        cursor = conn.cursor()
        conn.start_transaction()

        # Step 1: End the previous active assignment for this person, if one exists.
        # The end date is set to the day before the new assignment starts.
        sql_update = """
            UPDATE location_assignment
            SET end_date = DATE_SUB(%s, INTERVAL 1 DAY)
            WHERE person_id = %s AND end_date IS NULL;
        """
        cursor.execute(sql_update, (start_date, person_id))
        
        # Step 2: Insert the new assignment record.
        sql_insert = """
            INSERT INTO location_assignment (person_id, location_id, start_date, end_date, personnel_role, mandate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (person_id, location_id, start_date, None, personnel_role, mandate)
        cursor.execute(sql_insert, data)
        new_id = cursor.lastrowid

        # If both steps succeed, commit the transaction.
        conn.commit()
        print(f"Successfully created new assignment {new_id} and ended previous assignment for Person ID {person_id}.")
        return new_id
    except Error as e:
        print(f"Error during location assignment transaction: {e}")
        conn.rollback()
        # Re-raise the error so the Streamlit UI can catch and display it
        raise e
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
# QUERY FUNCTIONS (for UI display)
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

def register_new_club_member(person_data, member_data):
    """
    Handles the full registration of a new club member within a single database transaction.
    1. Creates a 'person' record.
    2. Creates a 'club_member' record using the new person's ID.
    If either step fails, the entire operation is rolled back.
    
    Args:
        person_data (dict): Dictionary with keys matching 'person' table columns.
        member_data (dict): Dictionary with keys matching 'club_member' table columns.
        
    Returns:
        The new club_member_id on success, None on failure.
    """
    conn = get_db_connection()
    if not conn: return None

    try:
        cursor = conn.cursor()
        # Start a transaction to ensure both inserts succeed or neither do.
        conn.start_transaction()

        # Step 1: Create the Person record
        p_cols = ', '.join(person_data.keys())
        p_placeholders = ', '.join(['%s'] * len(person_data))
        person_sql = f"INSERT INTO person ({p_cols}) VALUES ({p_placeholders})"
        cursor.execute(person_sql, tuple(person_data.values()))
        new_person_id = cursor.lastrowid
        
        # Step 2: Create the Club Member record
        member_data['club_member_id'] = new_person_id # Use the ID from the new person
        m_cols = ', '.join(member_data.keys())
        m_placeholders = ', '.join(['%s'] * len(member_data))
        member_sql = f"INSERT INTO club_member ({m_cols}) VALUES ({m_placeholders})"
        cursor.execute(member_sql, tuple(member_data.values()))

        # If we reach here, both inserts were successful. Commit the transaction.
        conn.commit()
        print(f"Successfully registered new member with ID: {new_person_id}")
        return new_person_id

    except Error as e:
        print(f"Error during member registration transaction: {e}")
        # If any error occurs, roll back all changes from this transaction.
        conn.rollback()
        # We can re-raise the error to be caught by the bridge file
        raise e
    finally:
        cursor.close()
        conn.close()

def update_member_profile(club_member_id, person_data, member_data):
    """
    Updates a member's profile across both the person and club_member tables.
    """
    # We can reuse our generic update function for this!
    person_success = True
    member_success = True
    
    # Update the person table if there's data for it
    if person_data:
        person_success = update("person", {"person_id": club_member_id}, person_data)
        
    # Update the club_member table if there's data for it
    if member_data:
        member_success = update("club_member", {"club_member_id": club_member_id}, member_data)
        
    return person_success and member_success

def get_family_links_for_member(club_member_id):
    """Retrieves a list of all family members linked to a club member."""
    conn = get_db_connection()
    if not conn: return []
    
    sql = """
        SELECT 
            p.person_id AS family_member_id,
            p.first_name,
            p.last_name,
            cfl.relationship_type,
            cfl.contact_priority
        FROM club_member_family_link cfl
        JOIN person p ON cfl.family_member_id = p.person_id
        WHERE cfl.club_member_id = %s;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (club_member_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error getting family links: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
        
def create_and_link_family_member(club_member_id, person_data, link_data):
    """
    Creates a new person and immediately links them as a family member to an existing club member.
    This is a transactional operation.
    
    Args:
        club_member_id (int): The ID of the member to link to.
        person_data (dict): Dictionary of details for the new person to create.
        link_data (dict): Dictionary with 'relationship_type' and 'contact_priority'.
        
    Returns:
        The new person_id on success, None on failure.
    """
    conn = get_db_connection()
    if not conn: return None

    try:
        cursor = conn.cursor()
        conn.start_transaction()

        # Step 1: Create the new Person (the family member)
        p_cols = ', '.join(person_data.keys())
        p_placeholders = ', '.join(['%s'] * len(person_data))
        person_sql = f"INSERT INTO person ({p_cols}) VALUES ({p_placeholders})"
        cursor.execute(person_sql, tuple(person_data.values()))
        new_family_member_id = cursor.lastrowid
        
        # Step 2: Create the link
        link_sql = """INSERT INTO club_member_family_link 
                      (club_member_id, family_member_id, relationship_type, contact_priority)
                      VALUES (%s, %s, %s, %s)"""
        link_tuple = (club_member_id, new_family_member_id, link_data['relationship_type'], link_data['contact_priority'])
        cursor.execute(link_sql, link_tuple)

        conn.commit()
        print(f"Successfully created and linked new family member with ID: {new_family_member_id}")
        return new_family_member_id

    except Error as e:
        print(f"Error during create-and-link transaction: {e}")
        conn.rollback()
        raise e  # Re-raise the error so the UI can catch it
    finally:
        cursor.close()
        conn.close()
        
def get_all_teams_with_details():
    """
    Retrieves all teams and joins with the locations table to get the
    name of the team's home location for a user-friendly display.
    """
    conn = get_db_connection()
    if not conn: return []

    sql = """
        SELECT
            t.team_id,
            t.name,
            t.team_gender,
            t.home_location_id,
            l.name AS home_location_name
        FROM teams t
        JOIN locations l ON t.home_location_id = l.location_id
        ORDER BY t.name;
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting all teams with details: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
        
def get_all_sessions_for_dashboard():
    """
    Retrieves all sessions with crucial joined data for the main dashboard view.
    Includes team names for quick identification.
    """
    conn = get_db_connection()
    if not conn: return []
    
    # This query uses GROUP_CONCAT to list the teams involved in each session.
    sql = """
        SELECT
            s.session_id,
            s.type,
            s.date_time,
            s.final_score,
            l.name AS location_name,
            GROUP_CONCAT(t.name ORDER BY t.name SEPARATOR ' vs ') AS teams_involved
        FROM sessions s
        JOIN locations l ON s.location_id = l.location_id
        LEFT JOIN session_teams st ON s.session_id = st.session_id
        LEFT JOIN teams t ON st.team_id = t.team_id
        GROUP BY s.session_id, l.name
        ORDER BY s.date_time DESC;
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        print(f"Error getting sessions for dashboard: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def detach_team_from_session(session_id, team_id):
    """
    Safely detaches a team from a session. Also deletes any formations
    associated with that team in that session to maintain data integrity.
    This is a transactional operation.
    """
    conn = get_db_connection()
    if not conn: return False
    
    try:
        cursor = conn.cursor()
        conn.start_transaction()

        # Step 1: Delete player formations for this team in this session
        cursor.execute("DELETE FROM formations WHERE session_id = %s AND team_id = %s", (session_id, team_id))
        
        # Step 2: Delete the link in session_teams
        cursor.execute("DELETE FROM session_teams WHERE session_id = %s AND team_id = %s", (session_id, team_id))
        
        conn.commit()
        print(f"Successfully detached Team ID {team_id} from Session ID {session_id}")
        return True
    except Error as e:
        print(f"Error detaching team from session: {e}")
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
        
def get_current_personnel_assignments():
    """
    Retrieves a list of all current personnel assignments (where end_date is NULL)
    and joins with person and locations to get user-friendly names.
    """
    conn = get_db_connection()
    if not conn: return []
    
    sql = """
        SELECT
            la.assignment_id,
            la.person_id,
            p.first_name,
            p.last_name,
            la.location_id,
            l.name AS location_name,
            la.personnel_role,
            la.mandate,
            la.start_date
        FROM location_assignment la
        JOIN person p ON la.person_id = p.person_id
        JOIN locations l ON la.location_id = l.location_id
        WHERE la.end_date IS NULL AND la.personnel_role IS NOT NULL
        ORDER BY l.name, p.last_name;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting current personnel assignments: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
        
def get_hobbies_for_member(club_member_id):
    """
    Retrieves a list of all hobbies (ID and name) currently assigned
    to a specific club member.
    """
    conn = get_db_connection()
    if not conn: return []
    
    sql = """
        SELECT
            h.hobby_id,
            h.hobby_name,
            h.description
        FROM hobbies h
        JOIN club_member_hobbies cmh ON h.hobby_id = cmh.hobby_id
        WHERE cmh.club_member_id = %s
        ORDER BY h.hobby_name;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (club_member_id,))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error getting hobbies for member: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def generate_and_log_weekly_emails(start_date, end_date):
    """
    Finds all players scheduled in sessions within a date range, generates
    the email content for each, and logs these emails to the database.
    This is now a single, atomic transaction.
    
    Returns:
        The number of emails generated and logged.
    """
    conn = get_db_connection()
    if not conn: return 0

    sql_select = """
        SELECT
            p.first_name, p.last_name, p.email_address,
            f.player_position,
            s.session_id, s.type AS session_type, s.date_time,
            loc.name AS location_name,
            t.name AS team_name,  -- Added team name for the subject
            hc_person.first_name AS coach_first_name,
            hc_person.last_name AS coach_last_name,
            hc_person.email_address AS coach_email
        FROM formations f
        JOIN sessions s ON f.session_id = s.session_id
        JOIN teams t ON f.team_id = t.team_id
        JOIN person p ON f.player_id = p.person_id
        JOIN locations loc ON s.location_id = loc.location_id
        LEFT JOIN (
            SELECT la.location_id, la.person_id
            FROM location_assignment la
            WHERE la.personnel_role = 'Coach' AND la.end_date IS NULL
        ) AS hc_assign ON t.home_location_id = hc_assign.location_id
        LEFT JOIN person hc_person ON hc_assign.person_id = hc_person.person_id
        WHERE DATE(s.date_time) BETWEEN %s AND %s;
    """
    
    try:
        cursor = conn.cursor(dictionary=True)
        # --- Start the transaction ONCE at the beginning ---
        conn.start_transaction()

        # Step 1: Perform the SELECT to get all necessary data
        cursor.execute(sql_select, (start_date, end_date))
        schedule_data = cursor.fetchall()
        
        if not schedule_data:
            print("No scheduled sessions found in the date range. No emails to generate.")
            conn.rollback() # It's good practice to rollback even if we did nothing
            return 0

        # Step 2: Process data and generate email content in Python
        email_log_data = []
        for row in schedule_data:
            session_time_str = row['date_time'].strftime("%A %d-%b-%Y %I:%M %p")
            subject = f"{row['location_name']} {row['team_name']} {session_time_str} {row['session_type']} session"
            body = (
                f"Hi {row['first_name']} {row['last_name']},\n\n"
                f"This is a reminder for your upcoming {row['session_type']} session.\n"
                f"Your role: {row['player_position']}\n"
                f"Date & Time: {session_time_str}\n"
                f"Location: {row['location_name']}\n"
                f"Head Coach: {row.get('coach_first_name', 'N/A')} {row.get('coach_last_name', '')} ({row.get('coach_email', 'N/A')})\n\n"
                f"Thank you,\nMVC Admin"
            )
            email_log_data.append((
                row['session_id'], row['location_name'], row['email_address'],
                subject, body[:100]
            ))

        # Step 3: Perform the batch INSERT for all generated emails
        sql_insert = """
            INSERT INTO emails (session_id, sender_name, receiver_email, email_subject, body)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(sql_insert, email_log_data)
        
        # --- If ALL steps above succeed, commit the transaction ONCE at the end ---
        conn.commit()
        print(f"Successfully logged {len(email_log_data)} emails to the database.")
        return len(email_log_data)
        
    except Error as e:
        print(f"An error occurred during email generation transaction: {e}")
        # --- If ANY step fails, roll back the entire operation ---
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
        
def get_dashboard_metrics():
    """
    Retrieves key metrics for the main admin dashboard in a single database call for efficiency.
    """
    conn = get_db_connection()
    if not conn:
        return {"active_members": "Error", "total_locations": "Error", "upcoming_sessions": "Error"}

    # Define the queries for each metric
    sql_members = "SELECT COUNT(*) AS count FROM club_member WHERE activity_status = 'Active';"
    sql_locations = "SELECT COUNT(*) AS count FROM locations;"
    sql_sessions = "SELECT COUNT(*) AS count FROM sessions WHERE date_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 7 DAY);"
    
    metrics = {}
    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(sql_members)
        metrics['active_members'] = cursor.fetchone()['count']
        
        cursor.execute(sql_locations)
        metrics['total_locations'] = cursor.fetchone()['count']
        
        cursor.execute(sql_sessions)
        metrics['upcoming_sessions'] = cursor.fetchone()['count']
        
        return metrics
    except Error as e:
        print(f"Error getting dashboard metrics: {e}")
        # Return N/A on error so the UI doesn't crash
        return {"active_members": "N/A", "total_locations": "N/A", "upcoming_sessions": "N/A"}
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()