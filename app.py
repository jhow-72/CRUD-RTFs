from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "jhow"
app.permanent_session_lifetime = timedelta(minutes=5)

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
    if request.method == "POST":
        session.permanent = True  # habilita o tempo setado no inicio do arquivo
        user = request.form['nm']
        session["user"] = user
        flash(f"{user} logou com sucesso ")
        return redirect(url_for('user'))
    elif "user" in session:
        user = session["user"]
        flash(f"{user} já está logado ")
        return redirect(url_for('user'))
    else:
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user} foi deslogado!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
