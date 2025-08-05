from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

# =================================================================
# ENUM DEFINITIONS
# =================================================================

class Gender(Enum): # Also used for team_gender
    MALE = 'Male'
    FEMALE = 'Female'

class ActivityStatus(Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    
class RelationshipType(Enum):
    FATHER = 'Father'
    MOTHER = 'Mother'
    GRANDFATHER = 'Grandfather'
    GRANDMOTHER = 'Grandmother'
    TUTOR = 'Tutor'
    PARTNER = 'Partner'
    FRIEND = 'Friend'
    OTHER = 'Other'
    
class ContactPriority(Enum):
    PRIMARY = 'Primary'
    SECONDARY = 'Secondary'
    
class LocationType(Enum):
    HEAD = 'Head'
    BRANCH = 'Branch'
    
class PersonnelRole(Enum):
    ADMINISTRATOR = "Administrator"
    CAPTAIN = 'Captain'
    COACH = 'Coach'
    ASSISTANT_COACH = 'Assistant Coach'
    MANAGER = 'Manager'
    GENERAL_MANAGER = 'General Manager'
    DEPUTY_MANAGER = 'Deputy Manager'
    TREASURER = 'Treasurer'
    SECRETARY = 'Secretary'
    
class PersonnelMandate(Enum): 
    VOLUNTEER = 'Volunteer'
    SALARIED = 'Salaried'
    
class PaymentMethod(Enum): 
    CASH = 'Cash'
    DEBIT_CARD = 'Debit Card'
    CREDIT_CARD = 'Credit Card'

class SessionType(Enum):
    GAME = 'Game'
    TRAINING = 'Training'
    
class PlayerPosition(Enum):
    SETTER = 'Setter'
    OUTSIDE_HITTER = 'Outside Hitter'
    OPPOSITE_HITTER = 'Opposite Hitter'
    MIDDLE_BLOCKER = 'Middle Blocker'
    DEFENSIVE_SPECIALIST = 'Defensive Specialist'
    LIBERO = 'Libero'

# =================================================================
# DATACLASS MODELS
# =================================================================

@dataclass
class Person:
    person_id: int
    first_name: str
    last_name: str
    dob: date
    ssn: str | None
    medicare_number: str | None
    phone_number: str | None
    address: str | None
    city: str | None
    province: str | None
    postal_code: str | None
    email_address: str | None
    gender: Gender | None

@dataclass
class ClubMember:
    club_member_id: int
    height: Decimal | None
    weight: Decimal | None
    activity_status: ActivityStatus
    join_date: date
    person_details: Person | None = None

@dataclass
class ClubMemberFamilyLink:
    club_member_id: int
    family_member_id: int
    relationship_type: RelationshipType
    contact_priority: ContactPriority

@dataclass
class Location:
    location_id: int
    location_type: LocationType
    name: str
    address: str | None
    city: str | None
    province: str | None
    postal_code: str | None
    web_address: str | None
    max_capacity: int | None

@dataclass
class LocationPhoneNumber:
    location_id: int
    phone_number: str

@dataclass
class LocationAssignment:
    assignment_id: int
    person_id: int
    location_id: int
    start_date: date
    end_date: date | None
    personnel_role: PersonnelRole | None
    mandate: PersonnelMandate | None

@dataclass
class Hobby:
    hobby_id: int
    hobby_name: str
    description: str | None

@dataclass
class ClubMemberHobby:
    club_member_id: int
    hobby_id: int

@dataclass
class Payment:
    payment_id: int
    club_member_id: int
    payment_date: date
    amount: Decimal
    method: PaymentMethod
    membership_year: int

@dataclass
class Team:
    team_id: int
    home_location_id: int
    name: str
    team_gender: Gender

@dataclass
class Session:
    session_id: int
    type: SessionType
    date_time: datetime
    final_score: str | None
    location_id: int

@dataclass
class SessionTeam:
    session_id: int
    team_id: int

@dataclass
class Formation:
    formation_id: int
    session_id: int
    team_id: int
    player_id: int
    player_position: PlayerPosition

@dataclass
class Email:
    email_id: int
    sender_name: str
    receiver_email: str
    email_subject: str | None
    body: str | None
    send_at: datetime
    session_id: int | None