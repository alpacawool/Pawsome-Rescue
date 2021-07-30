-- Data Manipulation Queries Needed
-- To denote variables that will be filled in by the back-end/front-end code
-- we will use a colon : character followed by a description of the variable.

-- Animals
-- Add Animals Page
--  INSERT Animals
INSERT INTO Animals(shelter_id, animal_name, birthdate, gender, 
    species_type, breed, personality, image_url, intake_date, 
    adopted_date, adoption_fee)
VALUES (:shelter_id_from_shelter_SELECTion, :animal_name, 
    :birthdate, :gender, :species_type, :breed, :personality,
    :image_url, :intake_date, :adopted_date, :adoption_fee);
--  SELECT Shelters to populate Shelter Name Selection
SELECT id, shelter_name
FROM Shelters;

-- Update Animals Page
--  UPDATE Animals
UPDATE Animals 
SET shelter_id = :shelter_id_from_shelter_SELECTion, 
    animal_name = :animal_name, 
    birthdate = :birthdate, 
    gender = :gender, 
    species_type = :species_type, 
    breed = :breed, 
    personality = :personality,
    image_url = :image_url, 
    intake_date = :intake_date, 
    adopted_date = :adopted_date, 
    adoption_fee = :adoption_fee
WHERE id = :id_of_animal_to_be_updated;
--  SELECT Shelters to populate Shelter Name Selection
SELECT id, shelter_name
FROM Shelters;

-- UPDATE Animal (Image URL only)
UPDATE Animals 
SET image_url = :url_of_image
WHERE id = :id_of_animal;

-- Filter Animals Page
--  SELECT all Animals
SELECT Animals.id, shelter_id, animal_name, birthdate, 
    gender, species_type, breed, personality, image_url, intake_date, 
    adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
LEFT JOIN Shelters ON shelter_id = Shelters.id
ORDER BY Animals.id ASC;
-- SELECT subset of Animals, based on Species, Shelter, and Adoption Filter
-- Note: Available animals are filtered by : adopted_date is NULL
--       Adopted animals are filtered by: adopted_date is NOT NULL
--       Animals with no Shelter assigned are: shelter_name IS NULL
SELECT Animals.id, shelter_id, animal_name,
        birthdate, gender, species_type, breed, personality, 
        image_url, intake_date, adopted_date, adoption_fee, 
        Shelters.id, shelter_name
FROM Animals 
LEFT JOIN Shelters ON shelter_id = Shelters.id
WHERE adopted_date IS NOT NULL
    AND
       species_type = :species_type_from_the_filter_dropdown
    AND
       shelter_name :shelter_name_from_the_filter_dropdown
ORDER BY Animals.id ASC
LIMIT :results_per_page OFFSET :curr_page_offset;
--  SELECT subset of Animals - based on the Species Type Filter
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, 
    species_type, breed, personality, image_url, intake_date, 
    adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
LEFT JOIN Shelters ON shelter_id = Shelters.id
WHERE species_type = :species_type_from_the_filter_dropdown
ORDER BY Animals.id ASC
LIMIT :results_per_page OFFSET :curr_page_offset;
--  SELECT subset of Animals - based on the Shelter Name Filter
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, 
    species_type, breed, personality, image_url, intake_date, 
    adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
LEFT JOIN Shelters ON shelter_id = Shelters.id
WHERE shelter_name = :shelter_name_from_the_filter_dropdown
ORDER BY Animals.id ASC
LIMIT :results_per_page OFFSET :curr_page_offset;
--  SELECT subset of Animals - based on the Available Filter - Available
SELECT Animals.id, shelter_id, animal_name, birthdate, gender,
    species_type, breed, personality, image_url, intake_date, 
    adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
LEFT JOIN Shelters ON shelter_id = Shelters.id
WHERE adopted_date IS NULL
ORDER BY Animals.id ASC
LIMIT :results_per_page OFFSET :curr_page_offset;
--  SELECT subset of Animals - based on the Available Filter - Adopted
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, 
    species_type, breed, personality, image_url, intake_date, 
    adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
LEFT JOIN Shelters ON shelter_id = Shelters.id
WHERE adopted_date IS NOT NULL
ORDER BY Animals.id ASC
LIMIT :results_per_page OFFSET :curr_page_offset;

-- Pet Profile Pages (available from "Learn More About Me" links on Filter Animals Page)
-- SELECT single pet by animal_id
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, 
    species_type, breed, personality, image_url, intake_date, 
    adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
LEFT JOIN Shelters ON shelter_id = Shelters.id
WHERE Animals.id = :id_of_desired_animal;


-- Shelters
-- Edit Shelters Page
--  INSERT Shelters
INSERT INTO Shelters(shelter_name, street, city, state, zip_code)
VALUES (:shelter_name, :street, :city, :state, :zip_code);
--  DELETE Shelters
DELETE FROM Shelters WHERE id = :id_of_shelter_to_be_deleted;

-- View Shelters Page
--  SELECT Shelters
SELECT *
FROM Shelters;


-- Applications
-- Edit Applications Page
--  SELECT Applications and get foreign key names
SELECT app.id, app.user_id, app.animal_id,
       app.application_date, app.approval_status,
       a.animal_name, u.first_name, u.last_name
       FROM Applications AS app
INNER JOIN Animals as a
    ON app.animal_id = a.id
INNER JOIN Users as u
    ON app.user_id = u.id
ORDER BY app.id ASC;

--  SELECT Applications specific to ID with foreign key information
SELECT app.*,
       a.animal_name, u.first_name, u.last_name
       FROM Applications AS app
INNER JOIN Animals as a
    ON app.animal_id = a.id
INNER JOIN Users as u
    ON app.user_id = u.id
WHERE app.id = :id_of_application;

--  UPDATE Applications
UPDATE Applications
SET approval_status = :approval_boolean
WHERE id = :id_of_application;

-- Apply for Animal (available from "Learn More About Me" links on Filter Animals Page)
--  INSERT Application
INSERT INTO Applications (
    user_id, animal_id, application_date, home_ownership,
    has_children, first_pet, pets_in_home, approval_status)
VALUES (
    :id_of_user, :id_of_animal, :date_of_app, :bool_owns_home,
    :bool_children, :bool_first_pet, :number_of_pets, :approval_boolean
);

-- Users
-- Edit Users Page
--  SELECT Users
SELECT * FROM Users;

--  UPDATE Users
UPDATE Users
SET first_name = :input_first_name,
    last_name = :input_last_name,
    email_address = :input_email,
    password = :input_password
WHERE id = :id_of_user;

-- SELECT Roles for Specific User (Users_Roles)
SELECT * FROM Users_Roles 
INNER JOIN Users ON user_id = Users.id 
INNER JOIN Roles ON role_id = Roles.id 
WHERE user_id = :id_of_user;

-- INSERT Users_Roles (M:M)
INSERT INTO Users_Roles (user_id, role_id)
VALUES (:id_of_user, :id_of_role);

-- DELETE Users_Roles
DELETE FROM Users_Roles
WHERE id = :id_of_users_roles;

-- Sign Up Page
--  INSERT Users
INSERT INTO Users (
    first_name, last_name, email_address, password)
VALUES (:input_first_name, :input_last_name, :input_email, :input_pw);

-- Roles
-- Edit Roles Page
--  SELECT Roles
SELECT * FROM Roles;
--  INSERT Roles
INSERT INTO Roles (role_name) VALUES (:input_role_name);
--  UPDATE Roles
UPDATE Roles
SET role_name = :input_role_name
WHERE id = :id_of_role;

-- Users_Roles
-- View Users_Roles Page
--  SELECT Users_Roles and include foreign key information
SELECT ur.*,
       r.role_name, u.first_name, u.last_name
       FROM Users_Roles AS ur
INNER JOIN Roles as r
    ON ur.role_id = r.id
INNER JOIN Users as u
    ON ur.user_id = u.id
ORDER BY r.id ASC;