-- Create Tables
CREATE OR REPLACE TABLE Animals (
    id INT NOT NULL AUTO_INCREMENT,
    shelter_id INT,
    animal_name VARCHAR(50) NOT NULL,
    birthdate DATE NOT NULL,
    gender CHAR(1),
    species_type VARCHAR(50),
    breed VARCHAR(50),
    personality VARCHAR(255),
    image_url VARCHAR(255),
    intake_date DATE NOT NULL,
    adopted_date DATE,
    adoption_fee DECIMAL(5,2),
    PRIMARY KEY(id)
); 

CREATE OR REPLACE TABLE Applications (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    animal_id INT,
    application_date DATE NOT NULL,
    home_ownership BOOLEAN,
    has_children BOOLEAN,
    first_pet BOOLEAN,
    pets_in_home INT(2),
    approval_status BOOLEAN,
    PRIMARY KEY(id)
); 

CREATE OR REPLACE TABLE Shelters (
    id INT NOT NULL AUTO_INCREMENT,
    shelter_name VARCHAR(255) NOT NULL,
    street VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code INT(5),
    PRIMARY KEY(id)
); 

CREATE OR REPLACE TABLE Users (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    email_address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT UNIQUE(email_address)
);

CREATE OR REPLACE TABLE Roles (
    id INT NOT NULL AUTO_INCREMENT,
    role_name VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE OR REPLACE TABLE Users_Roles (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    role_id INT,
    PRIMARY KEY(id)
);

-- Add Foreign Keys
-- Add shelter_id fk in Animals
ALTER TABLE Animals 
ADD CONSTRAINT fk_animals_shelters
FOREIGN KEY(shelter_id) REFERENCES Shelters(id)
ON DELETE SET NULL
ON UPDATE CASCADE;

-- Add user_id fk in Applications
ALTER TABLE Applications 
ADD CONSTRAINT fk_applications_users
FOREIGN KEY(user_id) REFERENCES Users(id)
ON DELETE SET NULL
ON UPDATE CASCADE;

-- Add animal_id fk in Applications
ALTER TABLE Applications 
ADD CONSTRAINT fk_applications_animals
FOREIGN KEY(animal_id) REFERENCES Animals(id)
ON DELETE SET NULL
ON UPDATE CASCADE;

-- M:M Users_Roles table
ALTER TABLE Users_Roles 
ADD CONSTRAINT fk_user_id
FOREIGN KEY(user_id) REFERENCES Users(id)
ON DELETE SET NULL
ON UPDATE CASCADE;

ALTER TABLE Users_Roles 
ADD CONSTRAINT fk_role_id
FOREIGN KEY(role_id) REFERENCES Roles(id)
ON DELETE SET NULL
ON UPDATE CASCADE;

-- Add Test Data
-- Insert Shelter Data
INSERT INTO Shelters(shelter_name, street, city, state, zip_code) VALUES ('Sunny Hills', '123 E 45th St', 'Portland', 'OR', '97211');
INSERT INTO Shelters(shelter_name, street, city, state, zip_code) VALUES ('Happy Tails', '333 N Broadway St', 'Tacoma', 'WA', '97232');
INSERT INTO Shelters(shelter_name, street, city, state, zip_code) VALUES ('The Comfy Couch', '1 N Broadway St', 'Seattle', 'WA', '97233');

-- Insert Animals Data
INSERT INTO Animals(shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee) VALUES (1, 'Greg', '2021-01-01', 'M', 'Dog', 'Beagle', 'Grouchy', 'dog1.png', '2021-03-01', NULL, 35.00);
INSERT INTO Animals(shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee) VALUES (2, 'Genevive', '2021-01-02', 'F', 'Cat', 'Calico', 'Happy', 'cat1.png', '2021-03-02', '2021-04-01', 35.00);
INSERT INTO Animals(shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee) VALUES (1, 'Peanut', '2021-01-03', 'F', 'Dog', 'Basset Hound', 'Cuddly', 'dog1.png', '2021-03-03', '2021-04-03', 25.00);

-- Insert Users Data
INSERT INTO Users(first_name, last_name, email_address, password) VALUES ("Mark", "Salazar", "MarkMSalazar@dayrep.com", "oe2ieF4Oin");
INSERT INTO Users(first_name, last_name, email_address, password) VALUES ("Stephen", "Cruz", "StephenBCruz@jourrapide.com", "gae9veZ2log");
INSERT INTO Users(first_name, last_name, email_address, password) VALUES ("Mary", "Hunt", "MaryDHunt@teleworm.us", "ooh2Mah5oh");
INSERT INTO Users(first_name, last_name, email_address, password) VALUES ("Tanya", "Kelly", "TanyaEKelly@dayrep.com", "Ohmae8ooque");

-- Insert Applications Data
INSERT INTO Applications(user_id, animal_id, application_date, home_ownership, has_children, first_pet, pets_in_home, approval_status) VALUES (1, 2, "2021-6-24", True, True, False, 1, NULL);
INSERT INTO Applications(user_id, animal_id, application_date, home_ownership, has_children, first_pet, pets_in_home, approval_status) VALUES (3, 1, "2021-6-26", False, False, False, 2, NULL);
INSERT INTO Applications(user_id, animal_id, application_date, home_ownership, has_children, first_pet, pets_in_home, approval_status) VALUES (1, 1, "2021-6-30", True, True, False, 0, True);

-- Insert Roles Data
INSERT INTO Roles(role_name) VALUES ("Staff");
INSERT INTO Roles(role_name) VALUES ("Volunteer");
INSERT INTO Roles(role_name) VALUES ("Member");
INSERT INTO Roles(role_name) VALUES ("Donator");
INSERT INTO Roles(role_name) VALUES ("Editor");

-- Insert Users_Roles Data
INSERT INTO Users_Roles(user_id, role_id) VALUES (1, 1);
INSERT INTO Users_Roles(user_id, role_id) VALUES (2, 1);
INSERT INTO Users_Roles(user_id, role_id) VALUES (3, 2);
INSERT INTO Users_Roles(user_id, role_id) VALUES (4, 3);
