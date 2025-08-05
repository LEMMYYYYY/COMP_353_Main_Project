import mysql.connector
from mysql.connector import Error
from db_connector import get_db_connection  # Assumes you have your db_connector.py file

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