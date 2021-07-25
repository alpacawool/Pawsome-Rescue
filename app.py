from flask import Flask, render_template, request, redirect, flash, url_for
import database.db_connector as db
import os
import json

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

# Database execute query and return results
def execute_query(query):
    query = query
    cursor = db.run_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return results

app = Flask("Pawsome")
app.secret_key = "1234" # For flask flash

@app.route("/")
@app.route("/home")
def home():
    db_animal = execute_query("SELECT * FROM Animals LIMIT 1;")
    return render_template('nw57_home.j2', animals=db_animal)

@app.route("/index")
def index_page():
    return render_template('nw57_index.j2')


@app.route("/settings")
def settings():
    return render_template('nw57_settings.j2')

@app.route("/edit-users")
def edit_users():
    db_users = execute_query("SELECT * FROM Users;")
    return render_template('nw57_edit_users.j2', users = db_users)

@app.route("/signup")
def signup():
    return render_template("nw57_signup.j2")

@app.route("/create-user", methods=['POST'])
def create_user():
    req = request.form
    insert_user_query = 'INSERT INTO Users ' \
        '(first_name, last_name, email_address, password) ' \
        'VALUES ("' + req['first_name'] + '", "' + req['last_name'] \
        + '", "' + req['email'] + '", "' + req['pw'] + '");'
    execute_query(insert_user_query)
    if request.referrer.endswith('/edit-users'):
        insert_success_message = req['first_name'] + ' ' \
            + req['last_name'] + ' added successfully!'
        flash(insert_success_message)
        return redirect('/edit-users')
    return redirect("/")

@app.route("/update-user/<int:user_id>", methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'POST':
        req = request.form
        update_user_query = 'UPDATE Users ' \
            'SET first_name = "' + req["user_first"] + '", ' \
            'last_name = "' + req["user_last"] + '", ' \
            'email_address = "' + req["user_email"] + '" ' \
            'WHERE id = ' + str(user_id) + ';'
        execute_query(update_user_query)
        update_user_success = 'Updated ' + req["user_first"] \
            + ' ' + req["user_last"] + ' successfully!'
        flash(update_user_success)
    return redirect("/edit-users")


@app.route("/edit-roles")
def edit_roles():
    db_roles = execute_query('SELECT * FROM Roles;')
    return render_template('nw57_edit_roles.j2', roles=db_roles)

@app.route("/insert-role", methods=['POST'])
def insert_role():
    if request.method == 'POST':
        insert_role_query = 'INSERT INTO Roles (role_name) ' \
            'VALUES ("' + request.form['name'] + '");'
        print(insert_role_query)
        execute_query(insert_role_query)
        success_message = 'Created role ' + request.form['name'] \
            + ' successfully!'
        flash(success_message)
    return redirect("/edit-roles")


@app.route("/update-role/<int:role_id>", methods=['GET', 'POST'])
def update_role(role_id):
    if request.method == 'POST':
        req = request.form
        update_role_query = 'UPDATE Roles ' \
            'SET role_name = "' + req["role_name"] + \
            '" WHERE id = ' + str(role_id) + ';'
        execute_query(update_role_query)
        flash("Updated role successfully!")

    return redirect("/edit-roles")

@app.route("/edit-users/roles/<int:user_id>")
def edit_users_roles(user_id):
    db_user_query = 'SELECT * FROM Users ' \
        'WHERE id = ' + str(user_id) + ';'
    db_user_role_query = 'SELECT * FROM Users_Roles ' \
        'INNER JOIN Users ON user_id = Users.id ' \
        'INNER JOIN Roles ON role_id = Roles.id ' \
        'WHERE user_id = ' + str(user_id) + ';'
    db_user = execute_query(db_user_query)
    db_users_roles = execute_query(db_user_role_query)
    db_roles = execute_query('SELECT * FROM Roles;')
    return render_template(
        "nw57_user_role_list.j2", 
        users_roles = db_users_roles,
        user = db_user,
        roles = db_roles
    )

# Assign new Roles and Users relationship
@app.route("/create-users-roles/<int:user_id>", methods=['POST'])
def create_users_roles(user_id):
    role_id = request.form.get('roles')
    insert_user_role_query = 'INSERT INTO Users_Roles (user_id, role_id) ' \
        'VALUES (' + str(user_id) + ', ' + role_id + ');'
    execute_query(insert_user_role_query)
    users_roles_redirect_url = "/edit-users/roles/" + str(user_id)
    flash('Added role successfully!' , 'insert')
    return redirect(users_roles_redirect_url)

# Delete Roles and Users relationship
@app.route("/delete-users-roles/<int:users_roles_id>", methods=['POST'])
def delete_users_roles(users_roles_id):
    current_user_id_query = 'SELECT user_id FROM Users_Roles ' \
        'WHERE id = ' + str(users_roles_id) + ';'
    delete_users_roles_query = 'DELETE FROM Users_Roles ' \
        'WHERE id = ' + str(users_roles_id) + ';'

    current_user_id = execute_query(current_user_id_query)[0]['user_id']
    execute_query(delete_users_roles_query)
    flash('Deleted role successfully!', 'delete')

    users_roles_redirect_url = "/edit-users/roles/" + str(current_user_id)
    return redirect(users_roles_redirect_url)

@app.route("/view-users-roles")
def view_users_roles():
    return render_template("nw57_view_users_roles.j2", users_roles = users_roles)

@app.route("/animals")
def animals():
    db_animals = execute_query("""
            SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            ORDER BY Animals.id ASC;""")
            
    # find distinct attributes for populating filters
    all_shelters = []
    all_species_types = []
    for animal in db_animals:
        all_shelters.append(animal['shelter_name'])
        all_species_types.append(animal['species_type'])
    distinct_shelters = set(all_shelters)
    distinct_species_type = set(all_species_types)

    # get any filters from the request
    shelter_filter = request.args.get('shelter', type = str)
    available_filter = request.args.get('available', type = str)
    species_type_filter = request.args.get('species_type', type = str)
    print(shelter_filter)
    if shelter_filter:
        # Filter Animal Shelters that are NULL
        if shelter_filter == 'None':
            db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality,
                    image_url, intake_date, adopted_date, adoption_fee, Shelters.id, 
                    shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name IS NULL
                ORDER BY Animals.id ASC;""")
        else:
            db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name = '{shelter_filter}'
                ORDER BY Animals.id ASC;""")
        return render_template('nw57_animals.j2', animals_data=db_animals_filtered, distinct_shelters=distinct_shelters, distinct_species_type=distinct_species_type)
    elif available_filter:
        if available_filter == 'available':
            db_animals_filtered = execute_query("""
            SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            WHERE adopted_date IS NULL
            ORDER BY Animals.id ASC;""")
        else:   # if available_filter == 'adopted'
            db_animals_filtered = execute_query("""
            SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            WHERE adopted_date IS NOT NULL
            ORDER BY Animals.id ASC;""")
        return render_template('nw57_animals.j2', animals_data=db_animals_filtered, distinct_shelters=distinct_shelters, distinct_species_type=distinct_species_type)
    elif species_type_filter:
        db_animals_filtered = execute_query(f"""
            SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            WHERE species_type = '{species_type_filter}'
            ORDER BY Animals.id ASC;""")
        return render_template('nw57_animals.j2', animals_data=db_animals_filtered, distinct_shelters=distinct_shelters, distinct_species_type=distinct_species_type)
    else:   # no filters
        return render_template('nw57_animals.j2', animals_data=db_animals, distinct_shelters=distinct_shelters, distinct_species_type=distinct_species_type)

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
        db_animals = execute_query(f"""
            SELECT Animals.id, shelter_id, animal_name, birthdate, gender, species_type, breed, personality, image_url, intake_date, adopted_date, adoption_fee, Shelters.id, shelter_name
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            WHERE Animals.id = {animal_id};""")
        try: 
            animal = db_animals[0]
            return render_template('nw57_pet_profile.j2', animal_id=animal_id, animal=animal)
        except IndexError as error:
            return('Animal not found')


@app.route("/insert-animal", methods=['GET', 'POST'])
def insert_animal():
    if request.method == 'POST': 
        animalName = request.form['animalName']
        shelterId = request.form['shelterId']
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

        # utiized this answer to help with inserting dates or NULLs into db: https://stackoverflow.com/a/66739228
        query = f"""
            INSERT INTO Animals(shelter_id, animal_name, birthdate, \
            gender, species_type, breed, personality, image_url, \
            intake_date, adopted_date, adoption_fee)
            VALUES ({f"'{shelterId}'" if shelterId else 'NULL'}, '{animalName}', '{birthdate}', \
            '{gender}', '{speciesType}', '{breed}', '{personality}', \
            '{imageURL}', '{intakeDate}', \
            {f"'{adoptedDate}'" if adoptedDate else 'NULL'}, {adoptionFee});
            """
        execute_query(query)
        return redirect(url_for('edit_animals'))
    else:
        shelterQueryResult = execute_query("""
            SELECT id, shelter_name
            FROM Shelters;""")
        return render_template('nw57_add_animal.j2', shelters = shelterQueryResult)

# View general information of all the animals
@app.route("/edit-animals")
def edit_animals():
    db_animals = execute_query("""
            SELECT *
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            ORDER BY Animals.id ASC;""")
    return render_template('nw57_update_animals.j2', animals_data=db_animals)

# View more detail of a single animal and update information if necessary
@app.route("/edit-animals/<int:animal_id>",methods =['GET', 'POST'])
def edit_animal_detail(animal_id):
    db_animals = execute_query(f"""
            SELECT *
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            WHERE Animals.id = {animal_id};""")
    db_shelters = execute_query("""
            SELECT id, shelter_name
            FROM Shelters;""")
    try: 
        animal = db_animals[0]
        return render_template('nw57_update_animal_detail.j2', animal_id = animal_id, animal = animal, shelters = db_shelters)
    except IndexError as error:
        return('Animal not found')

@app.route("/update_animal/<int:animal_id>", methods=['GET', 'POST'])
def update_animals(animal_id):
    if request.method == 'POST': 
        animalName = request.form['animalName']
        shelterId = request.form['shelterId']
        if shelterId == 'None':
            shelterId = None
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

        update_query = f"""
            UPDATE Animals 
            SET shelter_id = {f"{shelterId}" if shelterId else 'NULL'}, animal_name = '{animalName}', \
                birthdate = '{birthdate}', gender = '{gender}', \
                species_type = '{speciesType}', breed = '{breed}', \
                personality = '{personality}', image_url = '{imageURL}', \
                intake_date = '{intakeDate}', \
                adopted_date = {f"'{adoptedDate}'" if adoptedDate else 'NULL'}, \
                adoption_fee = {adoptionFee}
            WHERE id = {animal_id};"""
        print(update_query)
        execute_query(update_query)
        return redirect(url_for('edit_animals'))
    else:
        return redirect(url_for('edit_animals'))

@app.route("/edit-apps")
def edit_apps():
    select_app_query = 'SELECT app.id, app.user_id, app.animal_id, ' \
        'app.application_date, app.approval_status, ' \
        'a.animal_name, u.first_name, u.last_name ' \
        'FROM Applications AS app ' \
        'INNER JOIN Animals as a ON app.animal_id = a.id ' \
        'INNER JOIN Users as u ON app.user_id = u.id;'
    db_animal_apps = execute_query(select_app_query)
    return render_template(
        'nw57_edit_apps.j2', animal_apps=db_animal_apps)

@app.route("/edit-apps/<int:app_id>")
def edit_app_detail(app_id):
    select_app_detail_query = 'SELECT app.*, ' \
        'a.animal_name, u.first_name, u.last_name ' \
        'FROM Applications AS app ' \
        'INNER JOIN Animals as a ON app.animal_id = a.id ' \
        'INNER JOIN Users as u ON app.user_id = u.id ' \
        'WHERE app.id = ' + str(app_id) + ';'
    db_current_app = execute_query(select_app_detail_query)
    return render_template(
        'nw57_edit_app_detail.j2', 
            current_app = db_current_app[0])

@app.route("/update-app/<int:app_id>/<int:app_status>")
def update_app_approval(app_id, app_status):
    approval_string = None
    if app_status == 3:
        approval_string = 'NULL'
    else:
        approval_string = str(app_status)
    update_app_query = 'UPDATE Applications ' \
        'SET approval_status = ' + approval_string \
        + ' WHERE id = ' + str(app_id) + ';'
    execute_query(update_app_query)
    flash('Updated approval status successfully!')
    users_roles_redirect_url = "/edit-apps/" + str(app_id)
    return redirect(users_roles_redirect_url)


@app.route("/shelters")
def shelters():
    query = """
            SELECT *
            FROM Shelters;
            """
    db_shelters = execute_query(query)
    return render_template('nw57_shelters.j2', shelters_data=db_shelters)

@app.route("/edit-shelters")
def edit_shelters():
    query = """
            SELECT *
            FROM Shelters;
            """
    db_shelters = execute_query(query)
    return render_template('nw57_edit_shelters.j2', shelters_data=db_shelters)

@app.route("/delete-shelter/<int:shelter_id>", methods=['POST'])
def delete_shelter(shelter_id):
    delete_query = f"""
            DELETE FROM Shelters WHERE id = {shelter_id};
            """
    # print(delete_query)
    execute_query(delete_query)
    return redirect(url_for('edit_shelters'))

@app.route("/insert-shelter", methods=['POST'])
def insert_shelter():
    insert_query = f"""
            INSERT INTO Shelters(shelter_name, street, city, state, zip_code)
            VALUES ("{request.form['shelter_name']}", "{request.form['street']}", "{request.form['city']}", "{request.form['state']}", "{request.form['zip_code']}");
            """
    # print(insert_query)
    execute_query(insert_query)
    return redirect(url_for('edit_shelters'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)