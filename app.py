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

if __name__ == '__main__':
    app.run(debug=True)