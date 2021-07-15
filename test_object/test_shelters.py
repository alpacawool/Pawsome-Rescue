# Shelters filler data
# !! TODO: This can be deleted after successful database implementation
#
# Shelters: Records the details of each animal shelter location
# shelter_id: INT, auto_increment, unique, NOT NULL, PK
# shelter_name: VARCHAR(255), NOT NULL
# street: VARCHAR(255)
# city: VARCHAR(50)
# state: VARCHAR(2)
# zip_code: INT(5)
# Relationship: 
# 1:M relationship with Animals, using shelter_id as fk implemented inside Animals

class Shelter:
    def __init__(self, shelter_id, shelter_name, street, city, state, zip_code):
        self.shelter_id = shelter_id
        self.shelter_name = shelter_name
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code


test_shelters = [
    Shelter(0, "Wag'on Town", "2300 N 43rd Ave", "Portland", "OR", 97211),
    Shelter(1, "Shady Pines", "4246 Center Street", "Eugene", "OR", 97401),
    Shelter(2, "The Comfy Couch", "1260 Stockert Hollow Road", "Seattle", "WA", 98119)
]
