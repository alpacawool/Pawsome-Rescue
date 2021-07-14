from flask import Flask, render_template, request, redirect, flash
import os

# Testing with User Object Below
from test_object.test_users import User, test_users
from test_object.test_roles import Role, test_roles
from test_object.test_users_roles import User_Role, test_users_roles

users = test_users
roles = test_roles
users_roles = test_users_roles
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
    return render_template('nw57_animals.j2')

@app.route('/animals/<int:animal_id>', methods=['GET', 'POST'])
def pet_profile(animal_id):
    if request.method == 'POST': 
        # Implement a method for this POST
        return 'Submit Application'
    else:
        return render_template('nw57_pet_profile.j2', animal_id=animal_id)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)