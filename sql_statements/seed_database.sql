-- =================================================================
-- FINAL COMPREHENSIVE SEED SCRIPT FOR MONTREAL VOLLEYBALL CLUB (MVC)
-- =================================================================

USE mvc_db;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE emails;
TRUNCATE TABLE formations;
TRUNCATE TABLE session_teams;
TRUNCATE TABLE sessions;
TRUNCATE TABLE payments;
TRUNCATE TABLE club_member_hobbies;
TRUNCATE TABLE hobbies;
TRUNCATE TABLE location_assignment;
TRUNCATE TABLE location_phone_numbers;
TRUNCATE TABLE locations;
TRUNCATE TABLE club_member_family_link;
TRUNCATE TABLE club_member;
TRUNCATE TABLE teams;
TRUNCATE TABLE person;
SET FOREIGN_KEY_CHECKS = 1;


INSERT INTO locations (location_id, location_type, name, address, city, province, postal_code, web_address, max_capacity) VALUES
(1, 'Head', 'MVC Headquarters', '455 de Maisonneuve Blvd W', 'Montreal', 'Quebec', 'H3G 1M8', 'https://mvc-hq.ca', 150),
(2, 'Branch', 'MVC Laval Centropolis', '1235 Promenade du Centropolis', 'Laval', 'Quebec', 'H7T 0B6', 'https://mvc-laval.ca', 100),
(3, 'Branch', 'MVC South Shore Brossard', '8215 Boulevard Taschereau', 'Brossard', 'Quebec', 'J4X 1C2', 'https://mvc-southshore.ca', 120),
(4, 'Branch', 'MVC West Island', '300 Boulevard Brunswick', 'Pointe-Claire', 'Quebec', 'H9R 4Y2', 'https://mvc-westisland.ca', 80),
(5, 'Branch', 'MVC Vaudreuil-Soulanges', '500 Avenue Saint-Charles', 'Vaudreuil-Dorion', 'Quebec', 'J7V 2N3', 'https://mvc-vaudreuil.ca', 90),
(6, 'Branch', 'MVC Longueuil Hub', '100 Place Charles-Le Moyne', 'Longueuil', 'Quebec', 'J4K 2T4', 'https://mvc-longueuil.ca', 75);

INSERT INTO location_phone_numbers (location_id, phone_number) VALUES
(1, '514-848-2424'), (1, '514-848-2425'),
(2, '450-681-4812'),
(3, '450-466-9988'), (3, '450-466-9989'),
(4, '514-697-3333'),
(5, '450-218-3333'), (5, '450-218-3334');

INSERT INTO hobbies (hobby_id, hobby_name, description) VALUES
(1, 'Swimming', 'Enjoying the water and competitive swimming.'),
(2, 'Soccer', 'Playing soccer in local leagues.'),
(3, 'Tennis', 'Playing tennis and participating in tournaments.'),
(4, 'Hockey', 'Ice hockey during the winter season.'),
(5, 'Reading', 'Reading fiction and non-fiction books.'),
(6, 'Gaming', 'Playing video games on PC and console.');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, medicare_number, phone_number, address, city, province, postal_code, email_address, gender) VALUES
(1, 'Alice', 'Tremblay', '1998-03-15', '111222333', 'TRAM11223301', '514-111-1111', '123 Rue Sherbrooke', 'Montreal', 'Quebec', 'H2X 1X1', 'alice.t@email.com', 'Female'),
(2, 'Bob', 'Gagnon', '2001-07-22', '222333444', 'GAGB22334402', '514-222-2222', '456 Avenue McGill', 'Montreal', 'Quebec', 'H3A 1A1', 'bob.g@email.com', 'Male'),
(3, 'Charlie', 'Roy', '1995-11-30', '333444555', 'ROYC33445503', '450-333-3333', '789 Boulevard Rome', 'Brossard', 'Quebec', 'J4Y 1Y1', 'charlie.r@email.com', 'Male'),
(4, 'Diana', 'Bouchard', '2004-01-10', '444555666', 'BOUD44556604', '450-444-4444', '101 Boulevard de la Concorde', 'Laval', 'Quebec', 'H7N 1N1', 'diana.b@email.com', 'Female'),
(5, 'Edward', 'Leblanc', '2002-09-05', '555666777', 'LEBE55667705', '514-555-5555', '212 Boulevard Saint-Jean', 'Pointe-Claire', 'Quebec', 'H9R 3J1', 'edward.l@email.com', 'Male'),
(6, 'Fiona', 'Lavoie', '2010-06-20', '666777888', 'LAVF66778806', '514-666-6666', '313 Rue de la Montagne', 'Montreal', 'Quebec', 'H3G 1G1', 'fiona.l@email.com', 'Female'),
(7, 'George', 'Cote', '2012-04-25', '777888999', 'COTG77889907', '450-777-7777', '414 Rue de la Rive', 'Laval', 'Quebec', 'H7V 1V1', 'george.c@email.com', 'Male'),
(8, 'Hannah', 'Simard', '2011-08-12', '888999000', 'SIMH88990008', '450-888-8888', '515 Chemin de la Plaza', 'Brossard', 'Quebec', 'J4Z 1Z1', 'hannah.s@email.com', 'Female'),
(9, 'Ian', 'Gauthier', '1988-12-01', '999000111', 'GAUI99001109', '514-999-9999', '616 Avenue des Pins', 'Montreal', 'Quebec', 'H2W 1W1', 'ian.g@email.com', 'Male'),
(10, 'Julia', 'Morin', '1992-02-18', '123123123', 'MORJ12312310', '450-123-1234', '717 Rue de la Concorde', 'Laval', 'Quebec', 'H7N 2N2', 'julia.m@email.com', 'Female'),
(11, 'Kyle', 'Bergeron', '1990-10-03', '234234234', 'BERK23423411', '514-234-2345', '818 Avenue Atwater', 'Montreal', 'Quebec', 'H4C 1C1', 'kyle.b@email.com', 'Male'),
(12, 'Liam', 'Pelletier', '1985-05-14', '345345345', 'PELL34534512', '450-345-3456', '919 Boulevard Grande-Allee', 'Brossard', 'Quebec', 'J4Z 2Z2', 'liam.p@email.com', 'Male'),
(13, 'Megan', 'Lavoie', '1980-01-15', NULL, NULL, '514-131-3131', '313 Rue de la Montagne', 'Montreal', 'Quebec', 'H3G 1G1', 'megan.l@email.com', 'Female'),
(14, 'Noah', 'Cote', '1982-03-20', NULL, NULL, '450-141-4141', '414 Rue de la Rive', 'Laval', 'Quebec', 'H7V 1V1', 'noah.c@email.com', 'Male'),
(15, 'Olivia', 'Simard', '1981-07-07', NULL, NULL, '450-151-5151', '515 Chemin de la Plaza', 'Brossard', 'Quebec', 'J4Z 1Z1', 'olivia.s@email.com', 'Female'),
(16, 'Ethan', 'Landry', '2003-04-12', '161616161', 'LANE16161616', '514-161-6161', '16 Boulevard des Prairies', 'Laval', 'Quebec', 'H7N 3N3', 'ethan.l@email.com', 'Male'),
(17, 'Sophia', 'Paquette', '2005-02-28', '171717171', 'PAQS17171717', '514-171-7171', '17 Avenue Greene', 'Westmount', 'Quebec', 'H3Z 1Z3', 'sophia.p@email.com', 'Female'),
(18, 'Mason', 'Girard', '2000-10-10', '181818181', 'GIRM18181818', '514-181-8181', '18 Rue Sainte-Catherine', 'Montreal', 'Quebec', 'H2X 2X2', 'mason.g@email.com', 'Male'),
(19, 'Isabella', 'Martel', '2006-03-03', '191919191', 'MARI19191919', '450-191-9191', '19 Chemin de la Cote', 'Brossard', 'Quebec', 'J4Y 2Y2', 'isabella.m@email.com', 'Female'),
(20, 'Lucas', 'Fortin', '1999-01-20', '202020202', 'FORL20202020', '514-202-0202', '20 Boulevard Rene-Levesque', 'Montreal', 'Quebec', 'H2Z 1A1', 'lucas.f@email.com', 'Male'),
(21, 'Samuel', 'Chen', '1985-04-10', '212121212', NULL, '450-212-1212', '21 Rue de la Gare', 'Vaudreuil-Dorion', 'Quebec', 'J7V 0J1', 'samuel.chen@mvc.com', 'Male'),
(22, 'Chloe', 'Kim', '2004-11-20', '222222222', NULL, '450-222-2222', '22 Boulevard de la Cite', 'Vaudreuil-Dorion', 'Quebec', 'J7V 8P2', 'chloe.k@email.com', 'Female'),
(23, 'David', 'Singh', '2012-09-01', '232323232', NULL, '450-232-3232', '23 Rue Valois', 'Vaudreuil-Dorion', 'Quebec', 'J7V 1S3', 'david.s@email.com', 'Male'),
(24, 'Mia', 'Nguyen', '2011-05-30', '242424242', NULL, '450-242-4242', '24 Rue de la Fabrique', 'Longueuil', 'Quebec', 'J4H 1H1', 'mia.n@email.com', 'Female'),
(25, 'Leo', 'Da Silva', '2013-01-15', '252525252', NULL, '450-252-5252', '25 Rue Saint-Charles', 'Longueuil', 'Quebec', 'J4H 1A9', 'leo.ds@email.com', 'Male');

INSERT INTO club_member (club_member_id, height, weight, activity_status, join_date) VALUES
(1, 175.50, 68.5, 'Active', '2023-01-15'), (2, 182.00, 80.2, 'Active', '2023-02-20'),
(3, 190.10, 85.0, 'Active', '2023-03-10'), (4, 170.00, 62.0, 'Inactive', '2022-05-11'),
(5, 185.50, 78.8, 'Active', '2023-04-01'), (6, 155.00, 48.5, 'Active', '2024-01-20'),
(7, 160.20, 52.1, 'Active', '2024-02-05'), (8, 158.00, 49.0, 'Active', '2024-03-01'),
(9, 188.00, 82.0, 'Active', '2020-09-01'), (10, 172.00, 65.0, 'Active', '2021-08-15'),
(11, 180.00, 75.0, 'Active', '2022-01-10'), (12, 191.00, 88.0, 'Active', '2019-11-05'),
(16, 183.00, 77.0, 'Active', '2023-05-15'), (17, 173.00, 63.0, 'Active', '2023-06-01'),
(18, 181.00, 76.5, 'Active', '2023-07-20'), (19, 169.00, 61.0, 'Active', '2023-08-10'),
(20, 184.00, 79.0, 'Active', '2023-09-01'),
(22, 171.00, 62.5, 'Active', '2024-02-15'),
(23, 162.00, 53.0, 'Active', '2024-03-01'),
(24, 159.5, 50.5, 'Active', '2024-04-10'),
(25, 165.0, 55.0, 'Active', '2024-04-12');

INSERT INTO club_member_family_link (club_member_id, family_member_id, relationship_type, contact_priority) VALUES
(6, 13, 'Mother', 'Primary'),
(7, 14, 'Father', 'Primary'),
(8, 15, 'Mother', 'Primary');

INSERT INTO club_member_hobbies (club_member_id, hobby_id) VALUES
(1, 1), (1, 5), (2, 2), (3, 4), (4, 3), (5, 6), (6, 1), (7, 2), (8, 5);

INSERT INTO location_assignment (person_id, location_id, start_date, personnel_role, mandate) VALUES
(1, 1, '2023-01-15', NULL, NULL), (2, 1, '2023-02-20', NULL, NULL),
(3, 3, '2023-03-10', NULL, NULL), (4, 2, '2022-05-11', NULL, NULL),
(5, 4, '2023-04-01', NULL, NULL), (6, 1, '2024-01-20', NULL, NULL),
(7, 2, '2024-02-05', NULL, NULL), (8, 3, '2024-03-01', NULL, NULL),
(16, 2, '2023-05-15', NULL, NULL), (17, 1, '2023-06-01', NULL, NULL),
(18, 1, '2023-07-20', NULL, NULL), (19, 3, '2023-08-10', NULL, NULL),
(20, 1, '2023-09-01', NULL, NULL), (22, 5, '2024-02-15', NULL, NULL),
(23, 5, '2024-03-01', NULL, NULL), (24, 6, '2024-04-10', NULL, NULL),
(25, 6, '2024-04-12', NULL, NULL),
(9, 1, '2022-01-01', 'General Manager', 'Salaried'),
(10, 2, '2022-06-01', 'Manager', 'Salaried'),
(11, 1, '2023-01-01', 'Coach', 'Salaried'),
(12, 3, '2021-01-01', 'Coach', 'Volunteer'),
(21, 5, '2023-01-01', 'General Manager', 'Salaried');

INSERT INTO teams (team_id, home_location_id, name, team_gender) VALUES
(1, 1, 'Montreal Titans', 'Male'),
(2, 1, 'Montreal Valkyries', 'Female'),
(3, 2, 'Laval Raiders', 'Male'),
(4, 2, 'Laval Comets', 'Female'),
(5, 3, 'South Shore Sharks', 'Male'),
(6, 3, 'South Shore Sirens', 'Female'),
(7, 5, 'Vaudreuil Vipers', 'Male'),
(8, 6, 'Longueuil Lynx', 'Female');

INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year) VALUES
(1, '2024-01-10', 200.00, 'Credit Card', 2024),
(2, '2024-02-15', 100.00, 'Debit Card', 2024), (2, '2024-03-15', 100.00, 'Debit Card', 2024),
(3, '2024-03-05', 250.00, 'Cash', 2024), 
(22, '2024-02-20', 200.00, 'Debit Card', 2024),
(4, '2023-01-15', 150.00, 'Credit Card', 2023),
(6, '2024-01-18', 100.00, 'Credit Card', 2024),
(7, '2024-02-01', 50.00, 'Cash', 2024), (7, '2024-03-01', 50.00, 'Cash', 2024),
(8, '2024-02-28', 100.00, 'Debit Card', 2024),
(23, '2024-03-05', 100.00, 'Cash', 2024),
(24, '2024-04-15', 100.00, 'Credit Card', 2024),
(25, '2024-04-15', 100.00, 'Debit Card', 2024);

CALL sp_recalculate_member_status(2024);
CALL sp_recalculate_member_status(2023);

INSERT INTO sessions (session_id, type, date_time, final_score, location_id) VALUES
(1, 'Game', '2024-07-20 18:00:00', '3-1', 1);
INSERT INTO session_teams (session_id, team_id) VALUES (1, 1), (1, 5);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
(1, 1, 2, 'Setter'), (1, 1, 18, 'Outside Hitter'), (1, 1, 20, 'Libero'),
(1, 5, 3, 'Setter'), (1, 5, 12, 'Middle Blocker');

INSERT INTO sessions (session_id, type, date_time, location_id) VALUES
(2, 'Training', CONCAT(CURDATE() + INTERVAL 2 DAY, ' 19:00:00'), 2);
INSERT INTO session_teams (session_id, team_id) VALUES (2, 3), (2, 1);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
(2, 3, 7, 'Setter'), (2, 3, 16, 'Outside Hitter'),
(2, 1, 2, 'Libero'), (2, 1, 5, 'Setter');

INSERT INTO sessions (session_id, type, date_time, location_id) VALUES
(3, 'Game', CONCAT(CURDATE() + INTERVAL 4 DAY, ' 20:00:00'), 3);
INSERT INTO session_teams (session_id, team_id) VALUES (3, 2), (3, 6);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
(3, 2, 1, 'Setter'), (3, 2, 17, 'Outside Hitter'),
(3, 6, 8, 'Libero'), (3, 6, 19, 'Middle Blocker');

INSERT INTO sessions (session_id, type, date_time, location_id) VALUES
(4, 'Training', CONCAT(CURDATE() + INTERVAL 10 DAY, ' 17:30:00'), 4);
INSERT INTO session_teams (session_id, team_id) VALUES (4, 1), (4, 3);

INSERT INTO sessions (session_id, type, date_time, location_id) VALUES
(5, 'Training', CONCAT(CURDATE() + INTERVAL 5 DAY, ' 18:30:00'), 1);
INSERT INTO session_teams (session_id, team_id) VALUES (5, 1);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
(5, 1, 2, 'Setter'), (5, 1, 5, 'Outside Hitter'),
(5, 1, 18, 'Middle Blocker'), (5, 1, 20, 'Libero');

INSERT INTO sessions (session_id, type, date_time, location_id) VALUES
(6, 'Training', CONCAT(CURDATE() + INTERVAL 6 DAY, ' 20:00:00'), 1);
INSERT INTO session_teams (session_id, team_id) VALUES (6, 2);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
(6, 2, 1, 'Setter'), (6, 2, 6, 'Libero'),
(6, 2, 17, 'Opposite Hitter');

-- Q11
UPDATE location_assignment
SET end_date = '2023-08-31'
WHERE person_id = 4 AND location_id = 2;
INSERT INTO location_assignment (person_id, location_id, start_date, end_date)
VALUES (4, 1, '2023-09-01', '2024-01-15');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender) VALUES
(26, 'William', 'Brown', '2000-01-01', '262626262', 'Male');
INSERT INTO club_member (club_member_id, join_date, activity_status) VALUES
(26, '2021-05-20', 'Inactive');
INSERT INTO location_assignment (person_id, location_id, start_date, end_date) VALUES
(26, 2, '2021-05-20', '2022-04-30'),
(26, 3, '2022-05-01', '2023-01-10');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender) VALUES
(27, 'Ava', 'Garcia', '1999-03-15', '272727272', 'Female');
INSERT INTO club_member (club_member_id, join_date, activity_status) VALUES
(27, '2020-09-01', 'Inactive');
INSERT INTO location_assignment (person_id, location_id, start_date, end_date) VALUES
(27, 1, '2020-09-01', '2021-12-31'),
(27, 4, '2022-01-01', '2022-11-15');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender) VALUES
(28, 'James', 'Miller', '2002-07-22', '282828282', 'Male');
INSERT INTO club_member (club_member_id, join_date, activity_status) VALUES
(28, '2022-02-10', 'Inactive');
INSERT INTO location_assignment (person_id, location_id, start_date, end_date) VALUES
(28, 3, '2022-02-10', '2022-08-01'),
(28, 1, '2022-08-02', '2023-05-20');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender) VALUES
(29, 'Charlotte', 'Davis', '2001-11-30', '292929292', 'Female');
INSERT INTO club_member (club_member_id, join_date, activity_status) VALUES
(29, '2021-10-01', 'Inactive');
INSERT INTO location_assignment (person_id, location_id, start_date, end_date) VALUES
(29, 4, '2021-10-01', '2022-03-01'),
(29, 2, '2022-03-02', '2022-09-01'),
(29, 1, '2022-09-02', '2023-06-30');

-- Q12
INSERT INTO sessions (type, date_time, final_score, location_id) VALUES
('Game', '2024-06-15 19:00:00', '3-0', 1),
('Game', '2024-05-22 20:00:00', '2-3', 1),
('Game', '2024-04-18 18:00:00', '3-2', 1);

INSERT INTO session_teams (session_id, team_id) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2024-06-15 19:00:00'), 1),
((SELECT session_id FROM sessions WHERE date_time = '2024-06-15 19:00:00'), 3),
((SELECT session_id FROM sessions WHERE date_time = '2024-05-22 20:00:00'), 2),
((SELECT session_id FROM sessions WHERE date_time = '2024-05-22 20:00:00'), 4),
((SELECT session_id FROM sessions WHERE date_time = '2024-04-18 18:00:00'), 1),
((SELECT session_id FROM sessions WHERE date_time = '2024-04-18 18:00:00'), 5);

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2024-06-15 19:00:00'), 1, 2, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2024-06-15 19:00:00'), 1, 18, 'Libero'),
((SELECT session_id FROM sessions WHERE date_time = '2024-05-22 20:00:00'), 2, 1, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2024-05-22 20:00:00'), 2, 17, 'Outside Hitter');

INSERT INTO sessions (type, date_time, final_score, location_id) VALUES
('Game', '2024-07-01 18:00:00', '3-1', 3),
('Game', '2024-07-08 18:00:00', '1-3', 3),
('Game', '2024-07-15 18:00:00', '3-2', 3),
('Game', '2024-07-22 18:00:00', '0-3', 3);

INSERT INTO session_teams (session_id, team_id) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2024-07-01 18:00:00'), 5),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-01 18:00:00'), 1),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-08 18:00:00'), 6),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-08 18:00:00'), 2),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-15 18:00:00'), 5),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-15 18:00:00'), 3),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-22 18:00:00'), 6),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-22 18:00:00'), 4);

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2024-07-01 18:00:00'), 5, 3, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-01 18:00:00'), 5, 12, 'Libero'),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-08 18:00:00'), 6, 8, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-08 18:00:00'), 6, 19, 'Outside Hitter');

-- Q13
INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(30, 'Nora', 'Wilson', '2003-08-25', '303030303', 'Female', 'nora.w@email.com', '514-303-0303');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(30, '2024-05-01', 174.0, 64.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(30, 4, '2024-05-01');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(31, 'Benjamin', 'Lee', '1999-11-10', '313131313', 'Male', 'ben.lee@email.com', '514-313-1313');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(31, '2024-05-02', 180.0, 75.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(31, 1, '2024-05-02');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(32, 'Evelyn', 'Scott', '2005-01-20', '323232323', 'Female', 'evelyn.s@email.com', '450-323-2323');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(32, '2024-05-05', 168.5, 60.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(32, 2, '2024-05-05');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(33, 'Henry', 'Green', '2001-04-15', '333333333', 'Male', 'henry.g@email.com', '450-333-3333');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(33, '2024-05-10', 185.0, 82.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(33, 3, '2024-05-10');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(34, 'Sofia', 'King', '2006-02-25', '343434343', 'Female', 'sofia.k@email.com', '450-343-4343');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(34, '2024-05-12', 170.0, 61.5, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(34, 3, '2024-05-12');

-- Q14
INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(35, 'Daniel', 'Wilson', '2005-07-15', '353535353', 'Male', 'daniel.w@email.com', '514-353-5353');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(35, '2022-10-01', 181.0, 76.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(35, 1, '2022-10-01');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(36, 'Grace', 'Thompson', '2006-08-01', '363636363', 'Female', 'grace.t@email.com', '450-363-6363');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(36, '2022-11-15', 170.0, 61.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(36, 2, '2022-11-15');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(37, 'Jack', 'Robinson', '2004-02-20', '373737373', 'Male', 'jack.r@email.com', '514-373-7373');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(37, '2021-06-01', 188.0, 84.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(37, 4, '2021-06-01');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(38, 'Lily', 'Wright', '2005-03-10', '383838383', 'Female', 'lily.w@email.com', '450-383-8383');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(38, '2022-07-20', 169.5, 60.5, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(38, 3, '2022-07-20');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(39, 'Olivia', 'Walker', '2006-05-20', '393939393', 'Female', 'olivia.w@email.com', '450-393-9393');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(39, '2023-09-01', 172.0, 63.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(39, 5, '2023-09-01');

-- Q15
INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(40, 'William', 'Carter', '2002-12-01', '404040404', 'Male', 'will.c@email.com', '514-404-0404');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(40, '2023-10-10', 186.0, 81.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(40, 1, '2023-10-10');
INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year) VALUES
(40, '2024-01-15', 200.00, 'Credit Card', 2024);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
(4, 1, 40, 'Setter');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(41, 'Madison', 'Clark', '2004-06-18', '414141414', 'Female', 'maddy.c@email.com', '450-414-1414');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(41, '2023-11-01', 173.0, 64.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(41, 3, '2023-11-01');
INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year) VALUES
(41, '2024-02-01', 200.00, 'Debit Card', 2024);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
(3, 6, 41, 'Setter');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(42, 'Noah', 'Evans', '2003-02-14', '424242424', 'Male', 'noah.e@email.com', '514-424-2424');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(42, '2023-10-15', 188.0, 83.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(42, 2, '2023-10-15');
INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year) VALUES
(42, '2024-01-16', 200.00, 'Debit Card', 2024);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
(2, 3, 42, 'Setter');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(43, 'Emma', 'Collins', '2001-09-22', '434343434', 'Female', 'emma.c@email.com', '450-434-3434');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(43, '2022-11-20', 175.0, 66.0, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(43, 4, '2022-11-20');
INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year) VALUES
(43, '2024-02-11', 200.00, 'Credit Card', 2024);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2024-05-22 20:00:00'), 4, 43, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2024-07-22 18:00:00'), 4, 43, 'Setter');

INSERT INTO person (person_id, first_name, last_name, dob, ssn, gender, email_address, phone_number) VALUES
(44, 'Liam', 'Stewart', '1998-07-30', '444444444', 'Male', 'liam.s@email.com', '514-444-4444');
INSERT INTO club_member (club_member_id, join_date, height, weight, activity_status) VALUES
(44, '2021-08-15', 190.0, 85.5, 'Active');
INSERT INTO location_assignment (person_id, location_id, start_date) VALUES
(44, 1, '2021-08-15');
INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year) VALUES
(44, '2024-01-22', 200.00, 'Cash', 2024);
INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2024-06-15 19:00:00'), 1, 44, 'Setter');

-- Q16
INSERT INTO sessions (type, date_time, final_score, location_id) VALUES
('Game', '2025-03-01 10:00:00', '3-0', 1), -- Game Slot A (Male)
('Game', '2025-03-01 14:00:00', '1-3', 2), -- Game Slot B (Female)
('Game', '2025-03-08 10:00:00', '3-2', 3), -- Game Slot C (Male)
('Game', '2025-03-08 14:00:00', '2-3', 4), -- Game Slot D (Female)
('Game', '2025-03-15 10:00:00', '3-1', 1), -- Game Slot E (Male)
('Game', '2025-03-15 14:00:00', '0-3', 2), -- Game Slot F (Female)
('Game', '2025-03-22 10:00:00', '3-0', 3), -- Game Slot G (Male)
('Game', '2025-03-22 14:00:00', '3-2', 4); -- Game Slot H (Female)

-- Attach teams to these new games
INSERT INTO session_teams (session_id, team_id) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 10:00:00'), 1),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 10:00:00'), 3),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 14:00:00'), 2), 
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 14:00:00'), 4),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 10:00:00'), 5),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 10:00:00'), 7), 
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 14:00:00'), 6),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 14:00:00'), 8),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 10:00:00'), 1), 
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 10:00:00'), 5),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 14:00:00'), 2), 
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 14:00:00'), 6), 
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 10:00:00'), 3), 
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 10:00:00'), 7),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 14:00:00'), 4),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 14:00:00'), 8);

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 14:00:00'), 2, 1, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 14:00:00'), 4, 1, 'Libero'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 14:00:00'), 6, 1, 'Outside Hitter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 14:00:00'), 8, 1, 'Opposite Hitter');

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 10:00:00'), 1, 2, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 10:00:00'), 3, 2, 'Libero'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 10:00:00'), 5, 2, 'Outside Hitter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 10:00:00'), 7, 2, 'Opposite Hitter');

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 10:00:00'), 3, 3, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 10:00:00'), 5, 3, 'Libero'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 10:00:00'), 7, 3, 'Outside Hitter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 10:00:00'), 1, 3, 'Opposite Hitter');

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 14:00:00'), 4, 4, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 14:00:00'), 6, 4, 'Libero'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 14:00:00'), 8, 4, 'Outside Hitter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 14:00:00'), 2, 4, 'Opposite Hitter');

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-03-01 10:00:00'), 5, 5, 'Setter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-08 10:00:00'), 7, 5, 'Libero'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-15 10:00:00'), 3, 5, 'Outside Hitter'),
((SELECT session_id FROM sessions WHERE date_time = '2025-03-22 10:00:00'), 1, 5, 'Opposite Hitter');

INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year) VALUES
(4, '2024-03-01', 200.00, 'Credit Card', 2024);
INSERT INTO payments (club_member_id, payment_date, amount, method, membership_year) VALUES
(5, '2024-03-02', 200.00, 'Debit Card', 2024);
CALL sp_recalculate_member_status(2024);

-- Q17
UPDATE person
SET ssn = '141414141'
WHERE person_id = 14;

INSERT INTO location_assignment (person_id, location_id, start_date, personnel_role, mandate)
VALUES (14, 2, '2024-01-01', 'Coach', 'Volunteer');

-- Q18
INSERT INTO sessions (type, date_time, final_score, location_id) VALUES
('Game', '2025-04-01 19:00:00', '3-0', 2);

INSERT INTO session_teams (session_id, team_id) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-04-01 19:00:00'), 4), -- Laval Comets (WINNER)
((SELECT session_id FROM sessions WHERE date_time = '2025-04-01 19:00:00'), 6); -- South Shore Sirens (LOSER)

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-04-01 19:00:00'), 4, 22, 'Libero');

INSERT INTO formations (session_id, team_id, player_id, player_position) VALUES
((SELECT session_id FROM sessions WHERE date_time = '2025-04-01 19:00:00'), 4, 17, 'Outside Hitter');

-- Q19
INSERT INTO club_member_family_link (club_member_id, family_member_id, relationship_type, contact_priority)
VALUES (8, 12, 'Tutor', 'Secondary');