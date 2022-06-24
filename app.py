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
    paginas = db.relationship('Pagina', backref='rtfsP')

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


class Pagina(db.Model):
    id_pagina = db.Column("id_pagina", db.Integer, primary_key=True, autoincrement=True)
    id_rtf = db.Column(db.Integer, db.ForeignKey('rt_fs.id'))  # o db por alguma razão chamou RTFs de rt_fs
    numero = db.Column(db.Integer)
    nome = db.Column(db.String(30))
    cenarios = db.relationship('Cenarios', backref='pagina_class')

    def __init__(self, id_rtf, numero, nome):
        self.id_rtf = id_rtf
        self.numero = numero
        self.nome = nome


class Cenarios(db.Model):
    id_cenario = db.Column("id_cenario", db.Integer, primary_key=True, autoincrement=True)
    id_rtf = db.Column(db.Integer, db.ForeignKey('rt_fs.id'))  # o db por alguma razão chamou RTFs de rt_fs
    id_pagina = db.Column(db.Integer, db.ForeignKey('pagina.id_pagina'))
    pagina = db.Column(db.Integer)
    linha = db.Column(db.Integer)
    cenario = db.Column(db.String(250))
    resultado_esperado = db.Column(db.String(250))
    status = db.Column(db.Integer)
    massa_teste = db.Column(db.String(250))
    log_execucao = db.Column(db.String(10000))

    def __init__(self, id_rtf, id_pagina, pagina, linha, cenario, resultado_esperado):
        self.id_rtf = id_rtf
        self.id_pagina = id_pagina
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
    id_pagina = Pagina.query.filter_by(id_rtf=id_rtf, numero=pagina).first()
    id_pagina = id_pagina.id_pagina

    # Precisa fazer uma query para buscar todas as linhas da pagina do rtfs.
    # se o array for > 0, pegar a linha mais alta e somar 1
    # se não, linha = 1 (primeiro RTF)
    linha = 1
    quantidade_linhas = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina).count()
    maior_linha = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina).order_by(Cenarios.linha.desc()).first()
    if quantidade_linhas > 0:
        linha = maior_linha.linha+1

    if request.method == "POST":
        cenario = Cenarios(id_rtf, id_pagina, pagina, linha, request.form["cenario"], request.form["resultado_esperado"])
        db.session.add(cenario)
        db.session.commit()

        cenario.rtfs.data_update = datetime.utcnow().date()
        cenario.rtfs.data_update_formatada = get_data_formatada()
        db.session.commit()

        flash('Cenário adicionado com sucesso!')
        return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))
    else:
        return render_template("adicionar_cenario.html", id_rtf=id_rtf, pagina=pagina)


@app.route("/new_line/<int:id_rtf>/<int:pagina>", methods=["GET", "POST"])
def new_line(id_rtf, pagina):
    id_pagina = Pagina.query.filter_by(id_rtf=id_rtf, numero=pagina).first()
    id_pagina = id_pagina.id_pagina

    # Precisa fazer uma query para buscar todas as linhas da pagina do rtfs.
    # se o array for > 0, pegar a linha mais alta e somar 1
    # se não, linha = 1 (primeiro RTF)
    linha = 1
    quantidade_linhas = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina).count()
    maior_linha = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina).order_by(Cenarios.linha.desc()).first()
    if quantidade_linhas > 0:
        linha = maior_linha.linha+1

    cenario = Cenarios(id_rtf, id_pagina, pagina, linha, "TBD", "TBD")
    db.session.add(cenario)
    db.session.commit()

    cenario.rtfs.data_update = datetime.utcnow().date()
    cenario.rtfs.data_update_formatada = get_data_formatada()
    db.session.commit()

    flash("Linha Adicionada...")
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

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


@app.route("/viewRTF", methods=["POST", "GET"])
def viewRTF():

    if request.method == "POST":
        busca = request.form["busca"]
        rtfs = RTFs.query.filter(RTFs.name.contains(busca))
    else:
        rtfs = RTFs.query.all()

    return render_template("viewRTFs.html", values=rtfs)\


@app.route("/viewCenarios/<int:id_rtf>/<int:pagina>")
def viewCenarios(id_rtf, pagina):
    cenarios = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina)
    rtf = RTFs.query.get(id_rtf)
    pagina_obj = Pagina.query.filter_by(id_rtf=id_rtf, numero=pagina).first()

    try:
        qtd_pages = rtf.qtd_pages  # tenta pegar a qtd_paginas, se n conseguir, o array está vazio
        rtf_nome = rtf.name
        nome_pagina = pagina_obj.nome
        return render_template("viewCenarios.html", values=cenarios, rtf_nome=rtf_nome,id_rtf=id_rtf, pagina=pagina, qtd_pages=qtd_pages, nome_pagina=nome_pagina)
    except AttributeError:
        # se tentar abrir um RTF vazio, vai pedir para criar um cenário na pagina 1

        # adicionamente, irá forcar o qtd_pages = 1
        rtf.qtd_pages = 1

        # e criará a pagina 1 se ela não existir (buscar pagina 1 do rtf e verificar se ela tem nome ou n)
        if pagina_obj is None or pagina_obj.nome is None:
            pagina_obj = Pagina(id_rtf, 1, f"Pagina {1}")
            db.session.add(pagina_obj)

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
    pagina = Pagina(id_rtf, pagina_nova, f"Pagina {pagina_nova}")
    db.session.add(pagina)
    if rtf.qtd_pages > 1:
        rtf.qtd_pages += 1
        # começa organizando da pagina nova, pois a ideia é deixar a atual no mesmo estado
        organiza_paginas(id_rtf, pagina_nova, "add")
    else:
        rtf.qtd_pages += 1
    db.session.commit()
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina_nova))

def organiza_paginas(id_rtf, pagina_atual, modo):
    cenarios = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina_atual).all()
    pagina_obj = Pagina.query.filter_by(id_rtf=id_rtf, numero=pagina_atual).first()
    rtf = RTFs.query.get(id_rtf)

    if modo.__eq__("add"):
        # condicao de parada
        if pagina_atual > rtf.qtd_pages:  # preciso olhar todas as paginas
            return

        proxima_pagina = pagina_atual+1
        organiza_paginas(id_rtf, proxima_pagina, "add")

        # passa os cenarios da pagina atual para a proxima pagina q está confirmadamente vazia
        for cenario in cenarios:
            cenario.pagina = proxima_pagina

        # quando chegar aqui pela primeira vez o rtf já tem pagina_atual == qtd_paginas
        # porém o add no DB ainda n foi commitado
        # portanto pagina_obj = None quando pagina_atual == rtf.qtd_pages
        # por isso só preciso até o ultimo numero antes
        # olhar funcao "add_pagina"... pagina_nova já é o numero correto
        # se pagina_nova = 2, mesmo q qtd_pages seja 7, não vai afetar aqui... espero que eu entenda isso no futuro...
        # mas agr faz sentido...
        if pagina_atual < rtf.qtd_pages:
            pagina_obj.numero += 1

    if modo.__eq__("del"):
        # condicao de parada
        if pagina_atual > rtf.qtd_pages:  # preciso olhar todas as paginas a partir da que apaguei até a ultima
            return

        for cenario in cenarios:
            cenario.pagina -= 1

        pagina_obj.numero -= 1
        proxima_pagina = pagina_atual + 1
        organiza_paginas(id_rtf, proxima_pagina, "del")

    return

# deletar os cenarios da pagina
# deletar a pagina
# pegar todas as paginas que vinham depois da pagina deletada
# subtrair o numero da pagina para pagina -= 1
@app.route("/delete_pagina/<int:id_rtf>/<int:pagina>/")
def delete_pagina(id_rtf, pagina):
    rtf = RTFs.query.get(id_rtf)
    print(f"id_rtf: {id_rtf}; pagina: {pagina}")
    pagina_obj = Pagina.query.filter_by(id_rtf=id_rtf, numero=pagina).first()
    print(pagina_obj)

    if rtf.qtd_pages == 1:
        flash('Eae maluko, ta tirano? ta querendo arrumar problema pro c?')
        return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))
    else:
        delete_lista_cenarios(id_rtf, pagina)
        organiza_paginas(id_rtf, pagina, "del")
        rtf.qtd_pages -= 1
        db.session.delete(pagina_obj)

    db.session.commit()

    flash('A pagina foi removida com sucesso')
    ultima_pagina = rtf.qtd_pages+1  # pagina excluida era a ultima pagina do rtf
    if pagina == ultima_pagina:
        return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina-1))

    # se não for a ultima pagina, ele permanece na mesma url só q com os dados da pagina q estava na frente
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

def delete_lista_cenarios(id_rtf, pagina):
    cenarios = Cenarios.query.filter_by(id_rtf=id_rtf, pagina=pagina).all()
    for cenario in cenarios:
        db.session.delete(cenario)
    db.session.commit()
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

@app.route("/editar_nome_pagina/<int:id_rtf>/<int:pagina>/", methods=["POST","GET"])
def editar_nome_pagina(id_rtf, pagina):
    pagina_obj = Pagina.query.filter_by(id_rtf=id_rtf, numero=pagina).first()

    if request.method == "POST":
        novo_nome = request.form["novo_nome"]
        pagina_obj.nome = novo_nome
        db.session.commit()
        flash("Nome alterado com Sucesso!")
        return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

    return render_template("editar_nome_pagina.html", id_rtf=id_rtf, pagina=pagina, nome=pagina_obj.nome)

if __name__ == '__main__':
    db.create_all()  # cria o banco de dados caso ele ainda não exista
    app.run(debug=True)
