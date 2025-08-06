import db_operations as ops
from mysql.connector import Error as DB_Error

class RuleViolation(Exception):
    pass

def execute_query(query_func, params=None):
    """A wrapper for all SELECT operations."""
    try:
        if params:
            return query_func(**params)
        else:
            return query_func()
    except DB_Error as e:
        raise e

def execute_change(operation_func, params=None):
    """A wrapper for all INSERT, UPDATE, DELETE operations."""
    try:
        if params:
            return operation_func(**params)
        else:
            return operation_func()
    except DB_Error as e:
        raise RuleViolation(str(e)) from e
    except Exception as e:
        raise e

def execute_raw_sql(sql, params=None):
    """A special function to run raw SQL for complex, one-off reports."""
    from db_connector import get_db_connection
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        return results
    except DB_Error as e:
        raise e
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()