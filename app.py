from flask import Flask, render_template, request, redirect, flash
import os

# Testing with User Object Below
from test_object.test_users import User, test_users
users = test_users
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