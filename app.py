from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime, date
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "jhow"
app.permanent_session_lifetime = timedelta(minutes=5)

def get_data_formatada():
    data = date.today()
    data = data.strftime('%d/%m/%Y')
    return data

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
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    qtd_pages = db.Column(db.Integer)
    cenarios = db.relationship('Cenarios', backref='rtfs')

    data_criacao = db.Column(db.Date, default=datetime.utcnow().date())
    data_update = db.Column(db.Date, default=datetime.utcnow().date())
    data_criacao_formatada = db.Column(db.String(10))
    data_update_formatada = db.Column(db.String(10))

    def __init__(self, name, descricao):
        self.name = name
        self.descricao = descricao
        self.qtd_pages = 1
        data = get_data_formatada()
        self.data_criacao_formatada = data
        self.data_update_formatada = data

class Cenarios(db.Model):
    id_cenario = db.Column("id_cenario", db.Integer, primary_key=True, autoincrement=True)
    id_rtf = db.Column(db.Integer, db.ForeignKey('rt_fs.id'))  # o db por alguma razão chamou RTFs de rt_fs
    pagina = db.Column(db.Integer)
    linha = db.Column(db.Integer)
    cenario = db.Column(db.String(250))
    resultado_esperado = db.Column(db.String(250))
    status = db.Column(db.Integer)
    massa_teste = db.Column(db.String(250))
    log_execucao = db.Column(db.String(10000))

    def __init__(self, id_rtf, pagina, linha, cenario, resultado_esperado):
        self.id_rtf = id_rtf
        self.pagina = pagina
        self.linha = linha
        self.cenario = cenario
        self.resultado_esperado = resultado_esperado


##########################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_rtf/", methods=["GET", "POST"])
def add_rtf():
    if request.method == "POST":
        rtf = RTFs(request.form["name"], request.form["descricao"])
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

        rtf.data_update = datetime.utcnow().date()
        rtf.data_update_formatada = get_data_formatada()

        db.session.commit()
        return redirect(url_for('viewRTF'))

    return render_template("editar.html", rtf=rtf)

@app.route("/add_cenario/<int:id_rtf>/<int:pagina>", methods=["GET", "POST"])
def add_cenario(id_rtf, pagina):

    # Precisa fazer uma query para buscar todas as linhas da pagina do rtfs.
    # se o array for > 0, pegar a linha mais alta e somar 1
    # se não, linha = 1 (primeiro RTF)
    linha = 1
    quantidade_linhas = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina).count()
    maior_linha = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina).order_by(Cenarios.linha.desc()).first()
    if quantidade_linhas > 0:
        linha = maior_linha.linha+1

    if request.method == "POST":
        cenario = Cenarios(id_rtf, pagina, linha, request.form["cenario"], request.form["resultado_esperado"])
        db.session.add(cenario)
        db.session.commit()

        cenario.rtfs.data_update = datetime.utcnow().date()
        cenario.rtfs.data_update_formatada = get_data_formatada()
        db.session.commit()

        flash('Cenário adicionado com sucesso!')
        return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))
    else:
        return render_template("adicionar_cenario.html", id_rtf=id_rtf, pagina=pagina)

@app.route("/edit_cenario/<int:id_rtf>/<int:pagina>/<int:linha>", methods=["GET", "POST"])
def edit_cenario(id_rtf, pagina, linha):
    cenario = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina, linha=linha).first()

    if request.method == "POST":
        cenario.cenario = request.form["cenario"]
        cenario.resultado_esperado = request.form["resultado_esperado"]
        cenario.status = request.form["status"]
        cenario.massa_teste = request.form["massa_teste"]
        cenario.log_execucao = request.form["log_execucao"]

        cenario.rtfs.data_update = datetime.utcnow().date()
        cenario.rtfs.data_update_formatada = get_data_formatada()

        db.session.commit()

        return redirect(url_for('viewCenarios', id_rtf=id_rtf, pagina=pagina))

    return render_template("editar_cenario.html", cenario=cenario)


@app.route("/login/", methods=['POST', 'GET'])
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

@app.route("/viewCenarios/<int:id_rtf>/<int:pagina>")
def viewCenarios(id_rtf, pagina):
    cenarios = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina)
    cenario1 = Cenarios.query.filter_by(id_rtf=id_rtf).first()

    try:
        qtd_pages = cenario1.rtfs.qtd_pages  # tenta pegar a qtd_paginas, se n conseguir, o array está vazio
        return render_template("viewCenarios.html", values=cenarios, id_rtf=id_rtf, pagina=pagina, qtd_pages=qtd_pages)
    except AttributeError:
        # se tentar abrir um RTF vazio, vai pedir para criar um cenário na pagina 1

        # adicionamente, irá forcar o qtd_pages = 1
        rtf = RTFs.query.get(id_rtf)
        rtf.qtd_pages = 1
        db.session.commit()

        flash('RTF está sem nenhum cenário! Adicione o primeiro ;D')
        return render_template("adicionar_cenario.html", id_rtf=id_rtf, pagina=1)

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

@app.route("/delete_cenario/<int:id_rtf>/<int:pagina>/<int:linha>")
def delete_cenario(id_rtf, pagina, linha):
    cenario = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina, linha=linha).first()
    db.session.delete(cenario)
    sucess = ajust_num_linhas(id_rtf, pagina)
    if sucess:
        db.session.commit()
        flash('Cenário removido com sucesso!')
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

def ajust_num_linhas(id_rtf, pagina):
    cenarios = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina).all()
    for count, cenario in enumerate(cenarios):
        cenario.linha = count+1
    return True

# na criação da pagina acontece algumas coisas importantes
# primeiro  adicionamos +1 na qtd paginas do RTF
# depois a diversão começa
# pagina_nova é criada como pagina_atual+1
# pagina_movida é criada como pagina_nova+1
# ou seja, criamos uma pagina nova que ira entrar no lugar da que já existe
# vamos mudar todos os cenários q estavam na pagina_movida para o seu novo número (já é a própria pagina_movida)
# 1 problema: E se tiver mais de uma pagina dps da pagina nova? vamos perder dados!
# aí vamos poder brincar com recursão, vamos criar uma nova funcao para dar um help nisso
@app.route("/add_pagina/<int:id_rtf>/<int:pagina_atual>/")
def add_pagina(id_rtf, pagina_atual):
    rtf = RTFs.query.get(id_rtf)
    pagina_nova = pagina_atual + 1
    if rtf.qtd_pages > 1:
        rtf.qtd_pages += 1
        # começa organizando da pagina nova, pois a ideia é deixar a atual no mesmo estado
        organiza_paginas(id_rtf, pagina_nova)
    else:
        rtf.qtd_pages += 1
    db.session.commit()
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina_nova))

def organiza_paginas(id_rtf, pagina_atual):
    cenarios = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina_atual).all()

    # condicao de parada
    if not cenarios:  # verifica se a lista de cenários está vazia
        return

    proxima_pagina = pagina_atual+1
    organiza_paginas(id_rtf, proxima_pagina)

    for cenario in cenarios:
        cenario.pagina = proxima_pagina
    return

@app.route("/delete_pagina/<int:id_rtf>/<int:pagina>/")
def delete_pagina(id_rtf, pagina):
    cenario = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina, linha=linha).first()
    db.session.delete(cenario)
    sucess = ajust_num_linhas(id_rtf, pagina)
    if sucess:
        db.session.commit()
        flash('Cenário removido com sucesso!')
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

if __name__ == '__main__':
    db.create_all()  # cria o banco de dados caso ele ainda não exista
    app.run(debug=True)
