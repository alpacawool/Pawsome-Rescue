from flask import Flask

app = Flask("Pawsome")

@app.route("/")
def hello_world():
    return "Hello World"