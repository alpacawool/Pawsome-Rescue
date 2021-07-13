from flask import Flask, render_template, request, redirect, flash, url_for
import os

# Testing with User Object Below
from test_object.test_users import User, test_users
users = test_users
# Testing with Animal Object Below
from test_object.test_animals import Animal, test_animals
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
    return render_template('nw57_animals.j2', animals_data=animals_data)

@app.route('/animals/<int:animal_id>', methods=['GET', 'POST'])
def pet_profile(animal_id):
    if request.method == 'POST': 
        # Implement a method for this POST
        return 'Submit Application'
    else:
        return render_template('nw57_pet_profile.j2', animal_id=animal_id)

@app.route("/add_animal", methods=['GET', 'POST'])
def add_animal():
    if request.method == 'GET':
        shelterQueryResult = None
        # TODO: add SELECT names from Shelters DB Logic
        return render_template('nw57_add_animal.j2', shelters = shelterQueryResult)

    elif request.method == 'POST': 
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


@app.route("/edit-animals")
def edit_animals():
    # print(animals_data[1].intake_date)
    return render_template('nw57_update_animals.j2', animals_data=animals_data)

@app.route("/update_animal/<int:animal_id>", methods=['GET', 'POST'])
def update_animals():
    if request.method == 'POST': 
        # add Update to DB Logic
        return render_template('nw57_update_animals.j2')
    else:
        return render_template('nw57_update_animals.j2')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)