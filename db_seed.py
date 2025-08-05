import db_operations as db
from datetime import date


def seed_database():
    print("--- Seeding Database ---")
    
    # Add people
    person1_id = db.add_person('John', 'Doe', date(1990, 5, 15), ssn='11122333', email_address='john.doe@example.com')
    person2_id = db.add_person('Jane', 'Smith', date(2008, 8, 20), ssn='44455666', email_address='jane.smith@example.com')
    person3_id = db.add_person('Peter', 'Jones', date(1985, 2, 10), ssn='77788999', email_address='peter.jones@example.com')
    
    # Secondary contact
    person4_id = db.add_person('Mary', 'Smith', date(1980, 1, 1), phone_number='514-555-1234', email_address='mary.smith@example.com')
    
    print("--- Seeding Complete ---")
    
if __name__ == '__main__':
    seed_database()