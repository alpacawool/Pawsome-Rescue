from flask import Flask, render_template, request, redirect, flash, url_for
import database.db_connector as db
import os

# Database connection
db_connection = db.connect_to_db()

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

# Users Routes

"""
/edit-users
Entity: Users
Functions: SELECT all Users
"""
@app.route("/edit-users")
def edit_users():
    db_users = execute_query("SELECT * FROM Users;")
    return render_template('Users/nw57_edit_users.j2', users = db_users)

"""
/create-user
Entity: Users
Functions: INSERT new User
"""
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

"""
/update-user/<int:user_id>
Entity: Users
Functions: UPDATE individual Users
"""
@app.route("/update-user/<int:user_id>", methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'POST':
        req = request.form
        update_user_query = 'UPDATE Users ' \
            'SET first_name = "' + req["user_first"] + '", ' \
            'last_name = "' + req["user_last"] + '", ' \
            'email_address = "' + req["user_email"] + '", ' \
            'password = "' + req["user_pass"] + '" ' \
            'WHERE id = ' + str(user_id) + ';'
        execute_query(update_user_query)
        update_user_success = 'Updated ' + req["user_first"] \
            + ' ' + req["user_last"] + ' successfully!'
        flash(update_user_success)
    return redirect("/edit-users")

# Roles Routes

"""
/edit-roles
Entity: Roles
Functions: SELECT all Roles
"""
@app.route("/edit-roles")
def edit_roles():
    db_roles = execute_query('SELECT * FROM Roles;')
    return render_template('Roles/nw57_edit_roles.j2', roles=db_roles)

"""
/insert-roles
Entity: Roles
Functions: INSERT new Role
"""
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

"""
/update-role/<int:role_id>
Entity: Roles
Functions: UPDATE individual Role
"""
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

# Users_Roles Routes

"""
/edit-users/roles/<int:user_id>
Entity: Users_Roles
Functions: SELECT Users_Roles (Roles that belong to individual Users)
Relationships: Users and Roles (M:M)
"""
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
        "Users_Roles/nw57_user_role_list.j2", 
        users_roles = db_users_roles,
        user = db_user,
        roles = db_roles
    )

"""
/create-users-roles/<int:user_id>
Entity: Users_Roles
Functions: INSERT new Users_Roles
Relationships: Users and Roles (M:M)
"""
@app.route("/create-users-roles/<int:user_id>", methods=['POST'])
def create_users_roles(user_id):
    role_id = request.form.get('roles')
    insert_user_role_query = 'INSERT INTO Users_Roles (user_id, role_id) ' \
        'VALUES (' + str(user_id) + ', ' + role_id + ');'
    execute_query(insert_user_role_query)
    users_roles_redirect_url = "/edit-users/roles/" + str(user_id)
    flash('Added role successfully!' , 'insert')
    return redirect(users_roles_redirect_url)

"""
/delete-users-roles/<int:users_roles_id>
Entity: Users_Roles
Functions: DELETE individual Users_Roles
Relationships: Users and Roles (M:M)
"""
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

"""
/view-users-roles
Entity: Users_Roles, Users, Roles
Functions: SELECT all Users_Roles,
           SELECT Users first_name, last_name
           SELECT Roles role_name
Relationships: Users and Roles (M:M)
"""
@app.route("/view-users-roles")
def view_users_roles():
    select_users_roles_query = """
        SELECT ur.*,
            r.role_name, u.first_name, u.last_name
            FROM Users_Roles AS ur
        INNER JOIN Roles as r
            ON ur.role_id = r.id
        INNER JOIN Users as u
            ON ur.user_id = u.id
        ORDER BY r.id ASC;
        """
    db_users_roles = execute_query(select_users_roles_query)
    return render_template("Users_Roles/nw57_view_users_roles.j2", 
        users_roles = db_users_roles)

# Animals Routes

"""
Entity: Animals, Shelters
Functions: SELECT all Animals and
           SELECT all Shelters
           Filter Animals by shelter, availability, or species
Relationships: M:1 relationship between Animals and Shelters
"""
@app.route("/animals")
def animals():
    db_animals = execute_query("""
            SELECT Animals.id, shelter_id, animal_name, birthdate, 
                   gender, species_type, breed, personality, image_url, 
                   intake_date, adopted_date, adoption_fee, Shelters.id, 
                   shelter_name
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

    # All Three Filters
    if shelter_filter and available_filter and species_type_filter:
        if shelter_filter == 'None' and available_filter == 'Adopted':
            db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality, 
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE adopted_date IS NOT NULL
                    AND
                      species_type = '{species_type_filter}'
                    AND
                      shelter_name IS NULL
                ORDER BY Animals.id ASC;""")
        elif shelter_filter == 'None' and available_filter == 'Available':
            db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality, 
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE adopted_date IS NULL
                    AND
                      species_type = '{species_type_filter}'
                    AND
                      shelter_name IS NULL
                ORDER BY Animals.id ASC;""")
        elif available_filter == 'Available': 
             db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality, 
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE adopted_date IS NULL
                    AND
                      species_type = '{species_type_filter}'
                    AND
                      shelter_name = '{shelter_filter}'
                ORDER BY Animals.id ASC;""") 
        else:
             db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality, 
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE adopted_date IS NOT NULL
                    AND
                      species_type = '{species_type_filter}'
                    AND
                      shelter_name = '{shelter_filter}'
                ORDER BY Animals.id ASC;""") 
        return render_template('Animals/nw57_animals.j2', 
            animals_data=db_animals_filtered, 
            distinct_shelters=distinct_shelters, 
            distinct_species_type=distinct_species_type,
            current_species = species_type_filter,
            current_available = available_filter,
            current_shelter = shelter_filter)
  

    # Combined Filter: Availability and Species Type
    if species_type_filter and available_filter:
        if available_filter == 'Available':
            db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality, 
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE adopted_date IS NULL
                    AND
                      species_type = '{species_type_filter}'
                ORDER BY Animals.id ASC;""")
        else:
            db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality, 
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE adopted_date IS NOT NULL
                    AND
                      species_type = '{species_type_filter}'
                ORDER BY Animals.id ASC;""")
        return render_template('Animals/nw57_animals.j2', 
            animals_data=db_animals_filtered, 
            distinct_shelters=distinct_shelters, 
            distinct_species_type=distinct_species_type,
            current_species = species_type_filter,
            current_available = available_filter)

    
    # Combined Filter: Shelter and Availability
    if shelter_filter and available_filter:
        if shelter_filter == 'None' and available_filter == 'Available':
            db_animals_filtered = execute_query(f"""
             SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality,
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name IS NULL
					AND
					  adopted_date IS NULL
                ORDER BY Animals.id ASC;
            """)
        elif shelter_filter == 'None' and available_filter == 'Adopted':
            db_animals_filtered = execute_query(f"""
             SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality,
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name IS NULL
					AND
					  adopted_date IS NOT NULL
                ORDER BY Animals.id ASC;
            """)
        elif available_filter == 'Available':
            db_animals_filtered = execute_query(f"""
             SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality,
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name = '{shelter_filter}'
					AND
					  adopted_date IS NULL
                ORDER BY Animals.id ASC;
            """)
        else:
            db_animals_filtered = execute_query(f"""
             SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality,
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name = '{shelter_filter}'
					AND
					  adopted_date IS NOT NULL
                ORDER BY Animals.id ASC;
            """)
        return render_template('Animals/nw57_animals.j2', 
                animals_data=db_animals_filtered, 
                distinct_shelters=distinct_shelters, 
                distinct_species_type=distinct_species_type,
                current_shelter = shelter_filter,
                current_available = available_filter)
    
    # Combined Filter: Shelter and Species
    if shelter_filter and species_type_filter:
        if shelter_filter == 'None':
            db_animals_filtered = execute_query(f"""
             SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality,
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name IS NULL
					AND
					  species_type = '{species_type_filter}'
                ORDER BY Animals.id ASC;
            """)
        else:
            db_animals_filtered = execute_query(f"""
             SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality,
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name = '{shelter_filter}'
					AND
					  species_type = '{species_type_filter}'
                ORDER BY Animals.id ASC;
            """)
        return render_template('Animals/nw57_animals.j2', 
            animals_data=db_animals_filtered, 
            distinct_shelters=distinct_shelters, 
            distinct_species_type=distinct_species_type,
            current_shelter = shelter_filter,
            current_species = species_type_filter)
            

    if shelter_filter:
        # Filter Animal Shelters that are NULL
        if shelter_filter == 'None':
            db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name,
                    birthdate, gender, species_type, breed, personality,
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name IS NULL
                ORDER BY Animals.id ASC;""")
        else:
            db_animals_filtered = execute_query(f"""
                SELECT Animals.id, shelter_id, animal_name, 
                    birthdate, gender, species_type, breed, personality, 
                    image_url, intake_date, adopted_date, adoption_fee, 
                    Shelters.id, shelter_name
                FROM Animals 
                LEFT JOIN Shelters ON shelter_id = Shelters.id
                WHERE shelter_name = '{shelter_filter}'
                ORDER BY Animals.id ASC;""")
        return render_template('Animals/nw57_animals.j2', 
            animals_data=db_animals_filtered, 
            distinct_shelters=distinct_shelters, 
            distinct_species_type=distinct_species_type,
            current_shelter = shelter_filter
        )
    elif available_filter:
        if available_filter == 'Available':
            db_animals_filtered = execute_query("""
            SELECT Animals.id, shelter_id, animal_name,
                birthdate, gender, species_type, breed, personality, 
                image_url, intake_date, adopted_date, adoption_fee, 
                Shelters.id, shelter_name
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            WHERE adopted_date IS NULL
            ORDER BY Animals.id ASC;""")
        else:   # if available_filter == 'adopted'
            db_animals_filtered = execute_query("""
            SELECT Animals.id, shelter_id, animal_name, 
                birthdate, gender, species_type, breed, personality, 
                image_url, intake_date, adopted_date, adoption_fee,
                Shelters.id, shelter_name
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            WHERE adopted_date IS NOT NULL
            ORDER BY Animals.id ASC;""")
        return render_template('Animals/nw57_animals.j2', 
            animals_data=db_animals_filtered, 
            distinct_shelters=distinct_shelters, 
            distinct_species_type=distinct_species_type,
            current_available = available_filter
        )
    elif species_type_filter:
        db_animals_filtered = execute_query(f"""
            SELECT Animals.id, shelter_id, animal_name, birthdate, 
                gender, species_type, breed, personality, image_url, 
                intake_date, adopted_date, adoption_fee, 
                Shelters.id, shelter_name
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            WHERE species_type = '{species_type_filter}'
            ORDER BY Animals.id ASC;""")
        return render_template('Animals/nw57_animals.j2', 
            animals_data=db_animals_filtered, 
            distinct_shelters=distinct_shelters, 
            distinct_species_type=distinct_species_type,
            current_species = species_type_filter
        )
    else:   # no filters
        return render_template('Animals/nw57_animals.j2', 
            animals_data=db_animals, 
            distinct_shelters=distinct_shelters, 
            distinct_species_type=distinct_species_type
        )

"""
/animals/<int:animal_id>
Entity: Animals, Shelters, Users
Function: SELECT individual Animals to view their pet profile
          SELECT individual Shelters
          SELECT all Users (for /insert-app/ route in Applications)
Relationships: M:1 relationship between Animals and Shelters
"""
@app.route('/animals/<int:animal_id>', methods=['GET', 'POST'])
def pet_profile(animal_id):
    db_animals = execute_query(f"""
        SELECT Animals.id, shelter_id, animal_name, birthdate,
            gender, species_type, breed, personality, image_url, 
            intake_date, adopted_date, adoption_fee,
            Shelters.id, shelter_name
        FROM Animals 
        LEFT JOIN Shelters ON shelter_id = Shelters.id
        WHERE Animals.id = {animal_id};""")
    db_users = execute_query(f"""
        SELECT id, first_name, last_name FROM Users;
        """)
    try: 
        animal = db_animals[0]
        return render_template('Animals/nw57_pet_profile.j2', 
            animal_id=animal_id, 
            animal=animal, 
            users=db_users
        )
    except IndexError as error:
        return render_template('Animals/nw57_pet_profile.j2', 
            error_message="Animal Not Found"
        )

"""
/insert-animal
Entity: Animals, Shelters
Functions: INSERT individual Animals
           SELECT Shelter by id, shelter_name
Relationships: M:1 Relationship between Animals and Shelters
"""
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

        # utiized this answer to help with inserting dates or NULLs into db: 
        # https://stackoverflow.com/a/66739228
        query = f"""
            INSERT INTO Animals(shelter_id, animal_name, birthdate, \
            gender, species_type, breed, personality, image_url, \
            intake_date, adopted_date, adoption_fee)
            VALUES ({f"'{shelterId}'" if shelterId else 'NULL'}, \
            '{animalName}', '{birthdate}', \
            '{gender}', '{speciesType}', '{breed}', '{personality}', \
            '{imageURL}', '{intakeDate}', \
            {f"'{adoptedDate}'" if adoptedDate else 'NULL'}, {adoptionFee});
            """
        execute_query(query)
        flash("Added animal successfully!")
        return redirect(url_for('edit_animals'))
    else:
        shelterQueryResult = execute_query("""
            SELECT id, shelter_name
            FROM Shelters;""")
        return render_template('Animals/nw57_add_animal.j2', shelters = shelterQueryResult)

"""
/edit-animals
Entity: Animals, Shelters
Functions: SELECT all Animals
           SELECT Shelters by id
Relationships: M:1 relationship between Animals and Shelters
"""
@app.route("/edit-animals")
def edit_animals():
    db_animals = execute_query("""
            SELECT *
            FROM Animals 
            LEFT JOIN Shelters ON shelter_id = Shelters.id
            ORDER BY Animals.id ASC;""")
    return render_template('Animals/nw57_update_animals.j2', animals_data=db_animals)

"""
/edit-animals/<int:animal_id>
Entity: Animals, Shelters
Functions: SELECT individual Animals
           SELECT all Shelters
Relationships: M:1 Relationship between Animals and Shelters
"""
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
        return render_template('Animals/nw57_update_animal_detail.j2', 
            animal_id = animal_id, 
            animal = animal, 
            shelters = db_shelters
        )
    except IndexError as error:
        return('Animal not found')

"""
/update_animal/<int:animal_id>
Entity: Animals
Functions: UPDATE individual Animals
"""
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
            SET shelter_id = \
            {f"{shelterId}" if shelterId else 'NULL'}, \
                animal_name = '{animalName}', \
                birthdate = '{birthdate}', gender = '{gender}', \
                species_type = '{speciesType}', breed = '{breed}', \
                personality = '{personality}', image_url = '{imageURL}', \
                intake_date = '{intakeDate}', \
                adopted_date = {f"'{adoptedDate}'" if adoptedDate else 'NULL'}, \
                adoption_fee = {adoptionFee}
            WHERE id = {animal_id};"""
        print(update_query)
        execute_query(update_query)
        flash("Updated animal successfully!")
        return redirect(url_for('edit_animals'))
    else:
        return redirect(url_for('edit_animals'))

# Applications Routes

"""
/edit-apps
Entity: Applications, Animals, Users
Functions: SELECT all Applications,
           SELECT Users by Users.id,
           SELECT Animals by Animal.id
Relationships: M:1 Relationship between Applications and Animals
               M:1 Relationship between Applications and Users
"""
@app.route("/edit-apps")
def edit_apps():
    select_app_query = 'SELECT app.id, app.user_id, app.animal_id, ' \
        'app.application_date, app.approval_status, ' \
        'a.animal_name, u.first_name, u.last_name ' \
        'FROM Applications AS app ' \
        'INNER JOIN Animals as a ON app.animal_id = a.id ' \
        'INNER JOIN Users as u ON app.user_id = u.id ' \
        'ORDER BY app.id ASC;'
    db_animal_apps = execute_query(select_app_query)
    return render_template(
        'Applications/nw57_edit_apps.j2', animal_apps=db_animal_apps)

"""
/edit-apps/<int:app_id>
Entity: Applications, Animals, Users
Functions: SELECT individual Applications,
           SELECT individual Users by Users.id,
           SELECT individual Animals by Animal.id
Relationships: M:1 Relationship between Applications and Animals
               M:1 Relationship between Applications and Users
"""
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
        'Applications/nw57_edit_app_detail.j2', 
            current_app = db_current_app[0])

"""
/update-app/<int:app_id>/<int:app_status>
Entity: Applications
Functions: UPDATE Application approval boolean
"""
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

"""
/insert-app/<int:animal_id>
Entity: Applications
Functions: INSERT individual Applications
"""
@app.route("/insert-app/<int:animal_id>", methods=['GET', 'POST'])
def insert_app(animal_id):
    req = request.form
    insert_app_query = f"""
        INSERT INTO Applications(
            user_id, animal_id, application_date, home_ownership,
            has_children, first_pet, pets_in_home, approval_status)
        VALUES (
            {req['user-select']}, {str(animal_id)}, 
            {f"'{req['appDate']}'" if req['appDate'] else 'NULL'},
            {req['homeOwnership']}, {req['children']}, {req['firstPet']},
            {req['petsInHome']}, NULL
        );
        """
    execute_query(insert_app_query)
    flash("Application submitted successfully!")
    profile_redirect_url = '/animals/' + str(animal_id)
    return redirect(profile_redirect_url)

# Shelters Routes

"""
/shelters
Entity: Shelters
Functions: SELECT all Shelters
"""
@app.route("/shelters")
def shelters():
    query = """
            SELECT *
            FROM Shelters;
            """
    db_shelters = execute_query(query)
    return render_template('Shelters/nw57_shelters.j2', shelters_data=db_shelters)

"""
/edit-shelters
Entity: Shelters
Functions: SELECT all Shelters
"""
@app.route("/edit-shelters")
def edit_shelters():
    query = """
            SELECT *
            FROM Shelters;
            """
    db_shelters = execute_query(query)
    return render_template('Shelters/nw57_edit_shelters.j2', shelters_data=db_shelters)

"""
/delete-shelter/<int:shelter_id>
Entity: Shelters
Functions: DELETE individual Shelters
"""
@app.route("/delete-shelter/<int:shelter_id>", methods=['POST'])
def delete_shelter(shelter_id):
    delete_query = f"""
            DELETE FROM Shelters WHERE id = {shelter_id};
            """
    # print(delete_query)
    execute_query(delete_query)
    flash('Deleted Shelter successfully!' , 'delete')
    return redirect(url_for('edit_shelters'))

"""
/insert-shelter
Entity: Shelters
Functions: INSERT individual Shelters
"""
@app.route("/insert-shelter", methods=['POST'])
def insert_shelter():
    insert_query = f"""
            INSERT INTO Shelters (shelter_name, street, city, state, zip_code)
            VALUES ("{request.form['shelter_name']}", 
            "{request.form['street']}", "{request.form['city']}",
             "{request.form['state']}", "{request.form['zip_code']}");
            """
    # print(insert_query)
    execute_query(insert_query)
    flash('Added shelter successfully!' , 'insert')
    return redirect(url_for('edit_shelters'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)