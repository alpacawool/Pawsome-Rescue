from flask import Flask, render_template, request, redirect, flash, url_for
import os

# Testing with User Object Below
from test_object.test_users import User, test_users
from test_object.test_roles import Role, test_roles
from test_object.test_users_roles import User_Role, test_users_roles
from test_object.test_animals import Animal, test_animals

users = test_users
roles = test_roles
users_roles = test_users_roles
roles = test_roles
users_roles = test_users_roles
animals_data = test_animals
# End Testing Content Above

app = Flask("Pawsome")
app.secret_key = "1234" # For flask flash

@app.route("/")
@app.route("/home")
def home():
    return render_template('nw57_home.j2')

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


@app.route("/animals")
def animals():
    return render_template('nw57_animals.j2', animals_data=animals_data)

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

@app.route("/add_animal", methods=['GET', 'POST'])
def add_animal():
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


@app.route("/edit-animals")
def edit_animals():
    # print(animals_data[1].intake_date)
    return render_template('nw57_update_animals.j2', animals_data=animals_data)

@app.route("/update_animal/<int:animal_id>", methods=['GET', 'POST'])
def update_animals(animal_id):
    if request.method == 'POST': 
        # add Update to DB Logic
        return render_template('nw57_update_animals.j2')
    else:
        return redirect(url_for('edit_animals'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)