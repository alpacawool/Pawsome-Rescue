from flask import Flask, render_template, request, url_for, redirect
import os

app = Flask("Pawsome")

@app.route("/")
@app.route("/home")
def home():
    return render_template('nw57_home.j2')

@app.route("/index")
def index_page():
    return render_template('nw57_index.j2')

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

        print("Adding New Animal:", animalName)
        return redirect(url_for('update_animals'))


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