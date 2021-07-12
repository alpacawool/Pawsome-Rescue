from flask import Flask, render_template
import os

app = Flask("Pawsome")

@app.route("/")
@app.route("/home")
def hello_world():
    return render_template('nw57_home.j2')

@app.route("/index")
def index_page():
    return render_template('nw57_index.j2')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)