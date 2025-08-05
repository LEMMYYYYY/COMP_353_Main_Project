DELIMITER $$

CREATE TRIGGER trg_chk_ssn_club_member_insert
BEFORE INSERT ON club_member 
FOR EACH ROW
BEGIN
	DECLARE v_ssn VARCHAR(11);
    SELECT ssn INTO v_ssn FROM person WHERE person_id = NEW.club_member_id;
    
    IF v_ssn IS NULL THEN
			SIGNAL SQLSTATE '45000' -- User-defined exception
            SET MESSAGE_TEXT = 'Error: Cannot create a club member. The associated person must have an SSN.';
    END IF;
END$$

CREATE TRIGGER trg_chk_ssn_personnel_assignment_insert
BEFORE INSERT ON location_assignment
FOR EACH ROW
BEGIN
	DECLARE v_ssn VARCHAR(11);
    
    -- Check for SSN is personnel role is actually being assigned
    IF NEW.personnel_role IS NOT NULL THEN
		SELECT ssn INTO v_ssn FROM person WHERE person_id = NEW.person_id;
        
        IF v_ssn IS NULL THEN
			SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: Cannot assign personnel role. The associated person must have an SSN';
        END IF;
    END IF;
END$$

CREATE TRIGGER trg_two_team_limit_on_session
BEFORE INSERT ON session_teams
FOR EACH ROW
BEGIN
    DECLARE v_team_count INT;
    
    SELECT COUNT(*) INTO v_team_count FROM session_teams WHERE session_id = NEW.session_id;
    
    IF v_team_count >= 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Cannot add team to session. A session can only have a maximum of two teams.';
    END IF;
END$$

CREATE TRIGGER trg_4_payment_limit
BEFORE INSERT ON payments
FOR EACH ROW
BEGIN
    DECLARE v_payment_count INT;
    
    SELECT COUNT(*) INTO v_payment_count FROM payments WHERE payment_id = NEW.payment_id;
    
    IF v_payment_count >= 4 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Cannot add payment. User has already reached the maximum of four installements.';
    END IF;
END$$

CREATE TRIGGER trg_check_gender_consistency
BEFORE INSERT ON formations
FOR EACH ROW
BEGIN
    DECLARE v_player_gender ENUM('Male', 'Female');
    DECLARE v_team_gender ENUM('Male', 'Female');

    SELECT p.gender INTO v_player_gender
    FROM person p
    WHERE p.person_id = NEW.player_id;

    SELECT t.team_gender INTO v_team_gender
    FROM teams t
    WHERE t.team_id = NEW.team_id;

    -- Compare the two genders. If they do not match, reject the INSERT.
    IF v_player_gender <> v_team_gender THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Player gender does not match team gender. Cannot assign player to this formation.';
    END IF;
END$$

CREATE TRIGGER trg_check_session_time_conflict
BEFORE INSERT ON formations
FOR EACH ROW
BEGIN
    DECLARE v_new_session_datetime TIMESTAMP;
    DECLARE v_conflict_count INT;

    SELECT s.date_time INTO v_new_session_datetime
    FROM sessions s
    WHERE s.session_id = NEW.session_id;

    SELECT COUNT(*) INTO v_conflict_count
    FROM formations f
    JOIN sessions s ON f.session_id = s.session_id
    WHERE
        f.player_id = NEW.player_id
        AND DATE(s.date_time) = DATE(v_new_session_datetime)
        AND ABS(TIMESTAMPDIFF(MINUTE, s.date_time, v_new_session_datetime)) < 180;

    IF v_conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Time conflict. This player is already assigned to another session within 3 hours of this one.';
    END IF;
END$$
