-- Data Manipulation Queries Needed
-- To denote variables that will be filled in by the back-end/front-end code
-- we will use a colon : character followed by a description of the variable.

-- Animals
-- Add Animals Page
--  INSERT Animals
INSERT INTO Animals(shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee)
VALUES (:shelter_id_from_shelter_SELECTion, :animal_name, :birthdate, :gender, :species_type, :breed, :personality, :image_url, :intake_date, :adopted_date, :adoption_fee)
--  SELECT Shelters to populate Shelter Name Selection
SELECT id, shelter_name
FROM Shelters

-- Update Animals Page
--  UPDATE Animals
UPDATE Animals 
SET shelter_id = :shelter_id_from_shelter_SELECTion, animal_name = :animal_name, birthdate = :birthdate, gender = :gender, species_type = :species_type, breed = :breed, personality = :personality, image_url = :image_url, intake_date = :intake_date, adopted_date = :adopted_date, adoption_fee = :adoption_fee
WHERE id = :id_of_animal_to_be_updated
--  SELECT Shelters to populate Shelter Name Selection
SELECT id, shelter_name
FROM Shelters

-- Filter Animals Page
--  SELECT all Animals
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
INNER JOIN Shelters ON shelter_id = Shelters.id
ORDER BY intake_date ASC
--  SELECT subset of Animals - based on the Species Type Filter
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
INNER JOIN Shelters ON shelter_id = Shelters.id
WHERE species_type = :species_type_from_the_filter_dropdown
ORDER BY intake_date ASC
--  SELECT subset of Animals - based on the Shelter Name Filter
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
INNER JOIN Shelters ON shelter_id = Shelters.id
WHERE shelter_name = :shelter_name_from_the_filter_dropdown
ORDER BY intake_date ASC
--  SELECT subset of Animals - based on the Available Filter - Available
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
INNER JOIN Shelters ON shelter_id = Shelters.id
WHERE adopted_date IS NULL
ORDER BY intake_date ASC
--  SELECT subset of Animals - based on the Available Filter - Adopted
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
INNER JOIN Shelters ON shelter_id = Shelters.id
WHERE adopted_date IS NOT NULL
ORDER BY intake_date ASC

-- Pet Profile Pages (available from "Learn More About Me" links on Filter Animals Page)
-- SELECT single pet by animal_id
SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
FROM Animals 
INNER JOIN Shelters ON shelter_id = Shelters.id
WHERE Animals.id = :id_of_desired_animal
-- INSERT Application


-- Shelters
-- Edit Shelters Page
--  INSERT Shelters
INSERT INTO Shelters(shelter_name, street, city, state, zip_code)
VALUES (:shelter_name, :street, :city, :state, :zip_code)
--  DELETE Shelters
DELETE FROM Shelters WHERE id = :id_of_shelter_to_be_deleted

-- View Shelters Page
--  SELECT Shelters
SELECT id, shelter_name, street, city, state, zip_code
FROM Shelters


-- Applications
-- Edit Applications Page
--  SELECT Applications
--  SELECT Applications specific to ID
--  UPDATE Applications

-- Apply for Animal (available from "Learn More About Me" links on Filter Animals Page)
--  SELECT single pet by animal_id
--  INSERT Application


-- Users
-- Edit Users Page
--  SELECT Users
--  UPDATE Users
--  INSERT and DELETE Users_Roles (M:M)

-- Sign Up Page
--  INSERT Users


-- Roles
-- Edit Roles Page
--  SELECT Roles
--  INSERT Roles
--  UPDATE Roles


-- Users_Roles
-- View Users_Roles Page
--  SELECT Users_Roles

-- Edit Users_Roles Page (Click on plus symbol next to user in Role column)
--  INSERT and DELETE Users_Roles (M:M)
