from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add/")
def add():
    return render_template("adicionar.html")

@app.route("/edit/")
def edit():
    return render_template("editar.html")

@app.route("/login/", methods=['POST','GET'])
def login():
    return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
