from flask import Flask, render_template, request, redirect, flash, url_for
import database.db_connector as db
import os

# Database connection
db_connection = db.connect_to_db()

# Testing with User Object Below
from test_object.test_users import User, test_users
from test_object.test_roles import Role, test_roles
from test_object.test_users_roles import User_Role, test_users_roles
from test_object.test_animals import Animal, test_animals
from test_object.test_shelters import Shelter, test_shelters
from test_object.test_apps import Apply, test_apps

users = test_users
roles = test_roles
users_roles = test_users_roles
roles = test_roles
users_roles = test_users_roles
animals_data = test_animals
shelters_data = test_shelters
animal_apps = test_apps # preventing confusion with app
# End Testing Content Above

app = Flask("Pawsome")
app.secret_key = "1234" # For flask flash

@app.route("/")
@app.route("/home")
def home():
    animal = animals_data[0]
    return render_template('nw57_home.j2', animal=animal)

@app.route("/index")
def index_page():
    return render_template('nw57_index.j2')


@app.route("/settings")
def settings():
    return render_template('nw57_settings.j2')

@app.route("/edit-users")
def edit_users():
    return render_template('nw57_edit_users.j2', users=users)

@app.route("/signup")
def signup():
    return render_template("nw57_signup.j2")

@app.route("/create-user", methods=['POST'])
def create_user():
    req = request.form
    new_user = User(
        len(users),
        req['first_name'],
        req['last_name'],
        req['email'],
        req['pw']
    )
    users.append(new_user)
    return redirect("/")

@app.route("/update-user/<int:user_id>", methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'POST':
        req = request.form
        for user in users:
            if user.id == user_id:
                user.first = req["user_first"]
                user.last = req["user_last"]
                user.email = req["user_email"]
                flash("Updated user successfully!")
    return redirect("/edit-users")


@app.route("/edit-roles")
def edit_roles():
    return render_template('nw57_edit_roles.j2', roles=roles)

@app.route("/insert-role", methods=['POST'])
def insert_role():
    name = request.form['name']
    id = len(roles)
    roles.append(Role(id, name))
    return redirect("/edit-roles")


@app.route("/update-role/<int:role_id>", methods=['GET', 'POST'])
def update_role(role_id):
    if request.method == 'POST':
        req = request.form
        for role in roles:
            if role.id == role_id:
                role.name = req["role_name"]
                flash("Updated role successfully!")
    return redirect("/edit-roles")

@app.route("/edit-users/roles/<int:user_id>")
def edit_users_roles(user_id):
    # Replace with SQL-query filtering
    # Users_Roles by user and returning the role id and role names.
    for user in users:
        if user.id == user_id:
            current_roles = []
            for user_role in users_roles:
                if user_role.uid == user_id:
                    for role in roles:
                        if role.id == user_role.rid:
                            current_roles.append(Role(role.id, role.name))
            return render_template(
                "nw57_user_role_list.j2", user=user, current_roles=current_roles, roles=roles)
    return render_template('/edit-roles')

# Assign new Roles and Users relationship.
@app.route("/create-users-roles/<int:user_id>", methods=['POST'])
def create_users_roles(user_id):
    new_id = len(users_roles)
    role_id = request.form.get('roles')
    # Note: integer type is important. Otherwise python will interpret as wrong type
    users_roles.append(User_Role(new_id, int(user_id), int(role_id)))
    users_roles_redirect_url = "/edit-users/roles/" + str(user_id)
    return redirect(users_roles_redirect_url)

@app.route("/delete-users-roles/<int:user_id>/<int:role_id>", methods=['POST'])
def delete_users_roles(user_id, role_id):
    for user_role in users_roles:
        if user_role.uid == user_id and user_role.rid == role_id:
            users_roles.remove(user_role)
            break
    users_roles_redirect_url = "/edit-users/roles/" + str(user_id)
    return redirect(users_roles_redirect_url)

@app.route("/view-users-roles")
def view_users_roles():
    return render_template("nw57_view_users_roles.j2", users_roles = users_roles)

@app.route("/animals")
def animals():
    # find distinct attributes for filters
    all_shelters = []
    all_species_types = []
    for animal in animals_data:
        all_shelters.append(animal.shelter_name)
        all_species_types.append(animal.species_type)
    distinct_shelters = set(all_shelters)
    distinct_species_type = set(all_species_types)

    shelter_filter = request.args.get('shelter', type = str)
    available_filter = request.args.get('available', type = str)
    species_type_filter = request.args.get('species_type', type = str)
    
    if shelter_filter:
        print(f"Query DB with shelter filter ({shelter_filter}) & render that data")
        return render_template('nw57_animals.j2', animals_data=animals_data, distinct_shelters=distinct_shelters, distinct_species_type=distinct_species_type)
    elif available_filter:
        print(f"Query DB with available filter ({available_filter}) & render that data")
        return render_template('nw57_animals.j2', animals_data=animals_data, distinct_shelters=distinct_shelters, distinct_species_type=distinct_species_type)
    elif species_type_filter:
        print(f"Query DB with species_type filter ({species_type_filter}) & render that data")
        return render_template('nw57_animals.j2', animals_data=animals_data, distinct_shelters=distinct_shelters, distinct_species_type=distinct_species_type)
    else:
        print("No filters")
        return render_template('nw57_animals.j2', animals_data=animals_data, distinct_shelters=distinct_shelters, distinct_species_type=distinct_species_type)

@app.route('/animals/<int:animal_id>', methods=['GET', 'POST'])
def pet_profile(animal_id):
    if request.method == 'POST': 
        # Implement a method for this POST
        animalID = animal_id
        homeOwnership = request.form["homeOwnership"]
        children = request.form["children"]
        firstPet = request.form["firstPet"]
        petsInHome = request.form["petsInHome"]

        print('Submitted New Application for animalID:', animalID)
        return redirect(url_for('pet_profile', animal_id=animal_id))
    else:
        for animal in animals_data:
            if animal_id == animal.animal_id:
                return render_template('nw57_pet_profile.j2', animal_id=animal_id, animal=animal)
        return 'Pet not found'

@app.route("/insert-animal", methods=['GET', 'POST'])
def insert_animal():
    if request.method == 'POST': 
        animalName = request.form['animalName']
        shelterName = request.form['shelterName']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        speciesType = request.form['speciesType']
        breed = request.form['breed']
        personality = request.form['personality']
        imageURL = request.form['imageURL']
        intakeDate = request.form['intakeDate']
        if request.form['adoptedDate']:
            adoptedDate = request.form['adoptedDate']
        else:
            adoptedDate = None
        adoptionFee = request.form['adoptionFee']

        # TODO: add POST to DB Logic

        print("Adding New Animal:", animalName, adoptedDate)
        return redirect(url_for('edit_animals'))
    else:
        shelterQueryResult = None
        # TODO: add SELECT names from Shelters DB Logic
        return render_template('nw57_add_animal.j2', shelters = shelterQueryResult)

# View general information of the animal
@app.route("/edit-animals")
def edit_animals():
    # Will need to also SELECT shelter information if we also want shelter name
    # print(animals_data[1].intake_date)
    return render_template('nw57_update_animals.j2', animals_data=animals_data)

# View more detail of animal and update information if necessary
@app.route("/edit-animals/<int:animal_id>",methods =['GET', 'POST'])
def edit_animal_detail(animal_id):
    current_animal = None
    for animal in animals_data:
        print(animal.animal_name)
        if animal.animal_id == animal_id:
            current_animal = animal
            break
    return render_template('nw57_update_animal_detail.j2', animal = current_animal)

@app.route("/update_animal/<int:animal_id>", methods=['GET', 'POST'])
def update_animals(animal_id):
    if request.method == 'POST': 
        # add Update to DB Logic
        return render_template('nw57_update_animals.j2')
    else:
        return redirect(url_for('edit_animals'))

@app.route("/edit-apps")
def edit_apps():
    # Query foreign keys from applications where approval status is NULL
    curr_users=[]
    curr_animals=[]
    for application in animal_apps:
        for user in users:
            if user.id == application.uid:
                curr_users.append(user)
    for application in animal_apps:
        for animal in animals_data:
            if animal.animal_id == application.aid:
                curr_animals.append(animal)
    return render_template(
        'nw57_edit_apps.j2', users = curr_users, animals = curr_animals, animal_apps=animal_apps)

@app.route("/edit-apps/<int:app_id>")
def edit_app_detail(app_id):
    current_app = animal_apps[app_id]
    current_user = None
    current_animal = None
    for user in users:
        if user.id == current_app.uid:
            current_user = user
    for animal in animals_data:
        if animal.animal_id == current_app.aid:
            current_animal = animal
    return render_template(
        'nw57_edit_app_detail.j2', 
            current_app = current_app, user = current_user, animal = current_animal)


@app.route("/shelters")
def shelters():
    return render_template('nw57_shelters.j2', shelters_data=shelters_data)

@app.route("/edit-shelters")
def edit_shelters():
    return render_template('nw57_edit_shelters.j2', shelters_data=shelters_data)

@app.route("/delete-shelter/<int:shelter_id>", methods=['POST'])
def delete_shelter(shelter_id):
    shelterID = shelter_id
    print("Deleting Shelter ID: ", shelterID)
    return redirect(url_for('edit_shelters'))

@app.route("/insert-shelter", methods=['POST'])
def insert_shelter():
    if request.method == "POST":
        shelterName = request.form['shelter_name']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zip_code']
        print("Adding New Shelter:", shelterName)
    return redirect(url_for('edit_shelters'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)