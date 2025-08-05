-- =================================================================
-- SQL CREATE SCRIPT FOR MONTREAL VOLLEYBALL CLUB (MVC)
-- =================================================================

CREATE DATABASE IF NOT EXISTS mvc_db;
USE mvc_db;

CREATE TABLE person (
    person_id 			INT AUTO_INCREMENT PRIMARY KEY,
    first_name 			VARCHAR(255) 	NOT NULL,
    last_name 			VARCHAR(255) 	NOT NULL,
    dob 				DATE 			NOT NULL,
    ssn 				VARCHAR(11) 	UNIQUE, -- Nullable to allow for emergency contacts. Enforced by triggers
    medicare_number 	VARCHAR(20) 	UNIQUE, -- Nullable
    phone_number 		VARCHAR(20),
    address 			VARCHAR(255),
    city 				VARCHAR(100),
    province 			VARCHAR(100),
    postal_code 		VARCHAR(10),
    email_address 		VARCHAR(255) 	UNIQUE,
    gender				ENUM('Male', 'Female')
);

CREATE TABLE club_member (
    club_member_id 		INT PRIMARY KEY, -- This is a 1-to-1 relationship with person
    height 				DECIMAL(5, 2), -- e.g., 180.50 cm
    weight 				DECIMAL(5, 2), -- e.g., 75.25 kg
    activity_status 	ENUM('Active', 'Inactive') 	NOT NULL DEFAULT 'Active',
    join_date 			DATE 						NOT NULL,
    CONSTRAINT 			fk_club_member_person
	FOREIGN KEY 		(club_member_id) 			REFERENCES person(person_id) ON DELETE CASCADE
);
-- Trigger is required on INSERT to club_member to ensure the person has an SSN

CREATE TABLE club_member_family_link (
    club_member_id 		INT,
    family_member_id 	INT,
    relationship_type 	ENUM('Father', 'Mother', 'Grandfather', 'Grandmother', 'Tutor', 'Partner', 'Friend', 'Other') 	NOT NULL,
    contact_priority 	ENUM('Primary', 'Secondary') 	NOT NULL,
    PRIMARY KEY 		(club_member_id, family_member_id),
    UNIQUE 				(club_member_id, contact_priority),     -- A minor member can only have one primary and one secondary contact
    CONSTRAINT 			fk_link_club_member 	FOREIGN KEY (club_member_id) 	REFERENCES club_member(club_member_id) 	ON DELETE CASCADE,
    CONSTRAINT 			fk_link_family_member 	FOREIGN KEY (family_member_id) 	REFERENCES person(person_id)	 		ON DELETE CASCADE
);

CREATE TABLE locations (
    location_id 	INT AUTO_INCREMENT PRIMARY KEY,
    location_type 	ENUM('Head', 'Branch') 		NOT NULL,
    name 			VARCHAR(255) 				NOT NULL UNIQUE,
    address 		VARCHAR(255),
    city 			VARCHAR(100),
    province 		VARCHAR(100),
    postal_code 	VARCHAR(10),
    web_address 	VARCHAR(255),
    max_capacity 	INT
);

CREATE TABLE location_phone_numbers (
    location_id 	INT,
    phone_number 	VARCHAR(20),
    PRIMARY KEY 	(location_id, phone_number),
    CONSTRAINT 		fk_phone_location 	FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE TABLE location_assignment (
    assignment_id 	INT AUTO_INCREMENT PRIMARY KEY,
    person_id 		INT NOT NULL,
    location_id 	INT NOT NULL,
    start_date	 	DATE NOT NULL,
    end_date 		DATE, -- NULL if the assignment is current
    personnel_role 	ENUM('Administrator', 'Captain', 'Coach', 'Assistant Coach', 'Manager', 'General Manager', 'Deputy Manager', 'Treasurer', 'Secretary'),
    mandate 		ENUM('Volunteer', 'Salaried'),
    UNIQUE 			(person_id, start_date),     -- Business Rule: A person can't start two different assignments on the same day.
    CONSTRAINT 		fk_assignment_person FOREIGN KEY (person_id) REFERENCES person(person_id) ON DELETE CASCADE,
    CONSTRAINT 		fk_assignment_location FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE RESTRICT
);
-- Trigger is required on INSERT to ensure a person with a personnel_role has an SSN.

CREATE TABLE hobbies (
    hobby_id 		INT AUTO_INCREMENT PRIMARY KEY,
    hobby_name 		VARCHAR(100) NOT NULL UNIQUE,
    description 	TEXT
);

CREATE TABLE club_member_hobbies (
    club_member_id 	INT,
    hobby_id 		INT,
    PRIMARY KEY 	(club_member_id, hobby_id),
    CONSTRAINT 		fk_hobby_member FOREIGN KEY (club_member_id) REFERENCES club_member(club_member_id) ON DELETE CASCADE,
    CONSTRAINT 		fk_hobby_id FOREIGN KEY (hobby_id) REFERENCES hobbies(hobby_id) ON DELETE CASCADE
);

CREATE TABLE payments (
    payment_id 			INT AUTO_INCREMENT PRIMARY KEY,
    club_member_id 		INT NOT NULL,
    payment_date 		DATE NOT NULL,
    amount 				DECIMAL(10, 2) NOT NULL,
    method 				ENUM('Cash', 'Debit Card', 'Credit Card') NOT NULL,
    membership_year 	INT NOT NULL,
    CONSTRAINT 			fk_payment_member FOREIGN KEY (club_member_id) REFERENCES club_member(club_member_id) ON DELETE RESTRICT
);
-- Trigger on this table should update club_member.activity_status

CREATE TABLE teams (
    team_id 			INT AUTO_INCREMENT PRIMARY KEY,
    home_location_id 	INT NOT NULL,
    name 				VARCHAR(255) NOT NULL,
    team_gender	 		ENUM('Male', 'Female') NOT NULL,
    UNIQUE				(name, home_location_id),
    CONSTRAINT 			fk_team_location FOREIGN KEY (home_location_id) REFERENCES locations(location_id) ON DELETE RESTRICT
);

CREATE TABLE sessions (
    session_id 			INT AUTO_INCREMENT PRIMARY KEY,
    type 				ENUM('Game', 'Training') NOT NULL,
    date_time 			TIMESTAMP NOT NULL,
    final_score 		VARCHAR(50), -- e.g., "3-1", "25-23, 25-19, 22-25, 26-24"
    location_id 		INT NOT NULL,
    CONSTRAINT 			fk_session_location FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE RESTRICT
);

CREATE TABLE session_teams (
    session_id 		INT,
    team_id 		INT,
    PRIMARY KEY 	(session_id, team_id),
    CONSTRAINT 		fk_session_teams_session FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    CONSTRAINT 		fk_session_teams_team FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
);
-- Trigger is required to enforce that a session can have a maximum of two teams

CREATE TABLE formations (
    formation_id 		INT AUTO_INCREMENT PRIMARY KEY,
    session_id 			INT NOT NULL,
    team_id 			INT NOT NULL,
    player_id 			INT NOT NULL, -- This is a club_member_id
    player_position 	ENUM('Setter', 'Outside Hitter', 'Opposite Hitter', 'Middle Blocker', 'Defensive Specialist', 'Libero') NOT NULL,
    UNIQUE (session_id, player_id),  -- Business Rule: A player can only have one position in a single session.
    CONSTRAINT 			fk_formation_session FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    CONSTRAINT 			fk_formation_team FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    CONSTRAINT 			fk_formation_player FOREIGN KEY (player_id) REFERENCES club_member(club_member_id) ON DELETE CASCADE
);
-- Trigger is required to ensure that the player is of the team's gender. 
-- Trigger is required to verify player doesn't have two sessions within 3 hours.

CREATE TABLE emails (
    email_id 		INT AUTO_INCREMENT PRIMARY KEY,
    session_id 		INT, -- Can be NULL if the email is not related to a session
    sender_name 	VARCHAR(255), -- As per description, the name of the location
    receiver_email 	VARCHAR(255) NOT NULL,
    email_subject 	VARCHAR(255),
    body 			TEXT,
    send_at 		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT 		fk_email_session FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE SET NULL
);