# Filler data to test rendering of Role tables
# !! TODO: This can be deleted after successful database implementation
#
# #Roles: Roles that determine permissions on site for users enabling what features they are allowed to access on the site. For example, some users that are staff on the site would receive the staff role and be able to view certain things normal users cannot. Certain staff would receive editor roles so they could update information on animals. The idea is that create, update, and delete functionality permissions would be based on various roles the user has.
# role_id: INT, auto_increment, unique, NOT NULL, PK
# role_name: VARCHAR(255), NOT NULL
# Relationship: 
# M:M relationship with Users, using intersection table Users_Roles with two foreign keys

class User_Role:
    def __init__(self, id, uid, rid):
        self.id = id
        self.uid = uid # User ID
        self.rid = rid # Role ID

test_users_roles = [
    User_Role(0, 1, 2),
    User_Role(1, 1, 1),
    User_Role(2, 0, 0),
    User_Role(3, 0, 3),
    User_Role(4, 0, 1),
    User_Role(5, 2, 3),
    User_Role(6, 2, 1),
    User_Role(6, 3, 2),
    User_Role(7, 3, 0),
]
