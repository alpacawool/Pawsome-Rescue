# Filler data to test rendering of Role tables
# !! TODO: This can be deleted after successful database implementation
#
# #Roles: Roles that determine permissions on site for users enabling what features they are allowed to access on the site. For example, some users that are staff on the site would receive the staff role and be able to view certain things normal users cannot. Certain staff would receive editor roles so they could update information on animals. The idea is that create, update, and delete functionality permissions would be based on various roles the user has.
# role_id: INT, auto_increment, unique, NOT NULL, PK
# role_name: VARCHAR(255), NOT NULL
# Relationship: 
# M:M relationship with Users, using intersection table Users_Roles with two foreign keys

class Role:
    def __init__(self, id, name):
        self.id = id
        self.name = name

test_roles = [
    Role(0, "Staff"),
    Role(1, "Volunteer"),
    Role(2, "Member"),
    Role(3, "Donator"),
    Role(4, "Editor")
]
