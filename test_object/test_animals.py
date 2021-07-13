# Animals filler data
# !! TODO: This can be deleted after successful database implementation
#
# Animals: Records the details of pets with connections to our animal shelter
# animal_id: INT, auto_increment, unique, NOT NULL, PK
# animal_name: VARCHAR(50), NOT NULL
# birthdate: DATE NOT NULL
# gender: CHAR(1)
# species_type: VARCHAR(50)
# breed: VARCHAR(50)
# personality: VARCHAR(255)
# image_url: VARCHAR(255)
# intake_date: DATE NOT NULL
# adopted_date: DATE
# adoption_fee: DECIMAL(5,2)
# Relationships: 
# 1:M relationship between Applications, using animal_id as fk implemented inside Applications
# 1:M relationship between Shelters, using shelter_id as fk implemented inside Animals

class Animal:
    def __init__(self, animal_id, animal_name, shelter_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee):
        self.animal_id = animal_id
        self.animal_name = animal_name
        self.shelter_name = shelter_name
        self.birthdate = birthdate
        self.gender = gender
        self.species_type = species_type
        self.breed = breed
        self.personality = personality
        self.image_url = image_url
        self.intake_date = intake_date
        self.adopted_date = adopted_date
        self.adoption_fee = adoption_fee


test_animals = [
    Animal(0, "Belinda", "Wag'on Town", "2020-03-23", "F", "Cat", "Maine Coon", "Friendly", "cat1.png", "2021-06-23", "2021-06-30", 35.00),
    Animal(1, "Gene", "Wag'on Town", "2017-02-20", "M", "Dog", "Poodle", "Goofy", "dog1.png", "2021-06-24", None, 45.00),
    Animal(2, "Dr. Dog", "The Comfy Couch", "2017-02-20", "M", "Dog", "Shih-tzu", "Sleepy", "dog2.png", "2021-06-24", "2021-07-11", 35.00)
]
