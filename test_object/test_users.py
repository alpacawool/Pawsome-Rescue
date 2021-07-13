# Filler data to test rendering of User tables
# !! TODO: This can be deleted after successful database implementation
#
# https://www.fakenamegenerator.com/gen-random-us-us.php
# Users: Users that use the animal shelter website (both adopters and staff)
# user_id: INT, auto_increment, unique, NOT NULL, PK
# first_name: VARCHAR(50), NOT NULL
# last_name: VARCHAR(50)
# email_address: VARCHAR(255), UNIQUE, NOT NULL
# password: VARCHAR(255), NOT NULL
# Relationships: 
# M:M relationship with Roles, using intersection table Users_Roles with two foreign keys

class User:
    def __init__(self, id, first, last, email, pw):
        self.id = id
        self.first = first
        self.last = last
        self.email = email
        self.pw = pw


test_users = [
    User(0, "Mark", "Salazar", "MarkMSalazar@dayrep.com", "oe2ieF4Oin"),
    User(1, "Stephen", "Cruz", "StephenBCruz@jourrapide.com", "gae9veZ2log"),
    User(2, "Mary", "Hunt", "MaryDHunt@teleworm.us", "ooh2Mah5oh"),
    User(3, "Tanya", "Kelly", "TanyaEKelly@dayrep.com", "Ohmae8ooque")
]
