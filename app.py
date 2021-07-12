from flask import Flask, render_template
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

@app.route("/animals/<int:animal_id>")
def pet_profile(animal_id):
    return (render_template('nw57_pet_profile.j2'), animal_id)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)