# Applications: Records the details of adopter seeking adoption of a pet
# application_id: INT, auto_increment, unique, NOT NULL, PK
# fk_user_id: foreign key
# fk_animal_id: foreign key
# application_date: DATE NOT NULL
# home_ownership: BOOL
# has_children: BOOL
# first_pet: BOOL
# pets_in_home: INT(2)
# approval_status: BOOL
# Relationships: 
# 1:M relationship between Users, using user_id as fk implemented inside Applications
# 1:M relationship between Animals, using animal_id as fk implemented inside Applications


class Apply:
    def __init__(self, id, uid, aid, app_date, own_home, has_child, first_pet, 
        pets_in_home, approval):
            self.id = id
            self.uid = uid
            self.aid = aid
            self.app_date = app_date
            self.own_home = own_home
            self.has_child = has_child
            self.first_pet = first_pet
            self.pets_in_home = pets_in_home
            self.approval = approval
    

test_apps = [
    Apply(0, 0, 1,"2021-6-24",True,True,False,1,None),
    Apply(1, 2, 1,"2021-6-25",False,True,True,0,None),
    Apply(2, 3, 1,"2021-6-26",False,False,False,2,None),
    Apply(3, 0, 0, "2021-6-30",True,True,False,0,True)
]