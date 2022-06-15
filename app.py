from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "jhow"
app.permanent_session_lifetime = timedelta(minutes=5)

# section sobre o database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class RTFs(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    qtd_pages = db.Column(db.Integer)
    cenarios = db.relationship('Cenarios', backref='rtfs')

    def __init__(self, name, descricao, qtd_pages):
        self.name = name
        self.descricao = descricao
        self.qtd_pages = qtd_pages

class Cenarios(db.Model):
    id_rtf = db.Column(db.Integer, db.ForeignKey('rtfs.id'))
    pagina = db.Column(db.Integer, primary_key=True)
    linha = db.Column(db.Integer, primary_key=True)
    cenario = db.Column(db.String(250))
    resultado_esperado = db.Column(db.String(250))
    status = db.Column(db.Integer)
    massa_teste = db.Column(db.String(250))
    log_execucao = db.Column(db.String(10000))

    def __init__(self, id_rtf, pagina, linha, cenario, resultado_esperado):
        id_rtf = self.id_rtf
        pagina = self.pagina
        linha = self.linha
        cenario = self.cenario
        resultado_esperado = self.resultado_esperado


##########################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_rtf/", methods=["GET", "POST"])
def add_rtf():
    if request.method == "POST":
        rtf = RTFs(request.form["name"], request.form["descricao"], request.form["qtd_pages"])
        db.session.add(rtf)
        db.session.commit()
        flash('RTF adicionado com sucesso!')
        return redirect(url_for("viewRTF"))
    else:
        return render_template("adicionar.html")

@app.route("/edit_rtf/<int:id>", methods=["GET", "POST"])
def edit_rtf(id):
    rtf = RTFs.query.get(id)

    if request.method == "POST":
        rtf.name = request.form["name"]
        rtf.descricao = request.form["descricao"]
        db.session.commit()

        return redirect(url_for('viewRTF'))

    return render_template("editar.html", rtf=rtf)

@app.route("/login/", methods=['POST','GET'])
def login():
    if request.method == "POST":
        session.permanent = True  # habilita o tempo setado no inicio do arquivo
        user = request.form['nm']
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash(f"{user} logou com sucesso ")
        return redirect(url_for('user'))
    elif "user" in session:
        user = session["user"]
        flash(f"{user} já está logado ")
        return redirect(url_for('user'))
    else:
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email Cadastrado com Sucesso!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user} foi deslogado!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route("/viewUsers")
def viewUsers():
    return render_template("viewUsers.html", values=users.query.all())

@app.route("/viewRTF")
def viewRTF():
    rtfs = RTFs.query.all()
    return render_template("viewRTFs.html", values=rtfs)

@app.route("/delete_user/<int:id>")
def delete_user(id):
    found_user = users.query.get(id)
    db.session.delete(found_user)
    db.session.commit()
    flash('Usuário removido com sucesso!')
    return redirect(url_for("viewUsers"))

@app.route("/delete_rtf/<int:id>")
def delete_rtf(id):
    found_rtf = RTFs.query.get(id)
    db.session.delete(found_rtf)
    db.session.commit()
    flash('RTF removido com sucesso!')
    return redirect(url_for("viewRTF"))

if __name__ == '__main__':
    db.create_all()  # cria o banco de dados caso ele ainda não exista
    app.run(debug=True)
