from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime, date
import sqlManager
import modelsSGRTF as models
import helpers


app = Flask(__name__)
app.secret_key = "jhow"
app.permanent_session_lifetime = timedelta(minutes=5)


##########################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_rtf/", methods=["GET", "POST"])
def add_rtf():
    if request.method == "POST":
        rtf = models.RTFs(name=request.form["name"], descricao=request.form["descricao"], squad=request.form["squad"])
        sqlManager.add_rtf(rtf)

        # db.session.add(rtf)
        # db.session.commit()
        flash('RTF adicionado com sucesso!')
        return redirect(url_for("viewRTF"))
    else:
        return render_template("adicionar.html")

@app.route("/edit_rtf/<int:id>", methods=["GET", "POST"])
def edit_rtf(id):
    rtf = sqlManager.get_one_rtf(id)

    if request.method == "POST":
        rtf.name = request.form["name"]
        rtf.descricao = request.form["descricao"]
        rtf.data_update = helpers.get_data()
        rtf.data_update_formatada = helpers.get_data_formatada()

        sqlManager.edit_rtf(rtf)
        return redirect(url_for('viewRTF'))

    return render_template("editar.html", rtf=rtf)

@app.route("/add_cenario/<int:id_rtf>/<int:pagina>", methods=["GET", "POST"])
def add_cenario(id_rtf, pagina):
    pagina_obj = sqlManager.busca_pagina(id_rtf, pagina)

    if request.method == "POST":
        return new_line(id_rtf, pagina, cenario=request.form["cenario"], resultado_esperado=request.form["resultado_esperado"])
    else:
        return render_template("adicionar_cenario.html", id_rtf=id_rtf, pagina=pagina)


@app.route("/new_line/<int:id_rtf>/<int:pagina>", methods=["GET", "POST"])
def new_line(id_rtf, pagina, cenario="TBD", resultado_esperado="TBD"):
    id_pagina = sqlManager.busca_id_1_pagina(id_rtf, pagina)

    # Precisa fazer uma query para buscar todas as linhas da pagina do rtfs.
    # se o array for > 0, pegar a linha mais alta e somar 1
    # se não, linha = 1 (primeiro RTF)
    linha_nova = 1
    quantidade_linhas = sqlManager.get_qtd_cenarios_pagina(id_rtf, pagina)
    maior_linha = sqlManager.get_maior_linha_pagina(id_rtf, pagina)

    if quantidade_linhas > 0:
        linha_nova = maior_linha+1

    cenario_obj = models.Cenarios(id_rtf=id_rtf, id_pagina=id_pagina, pagina=pagina, linha=linha_nova, cenario=cenario, resultado_esperado=resultado_esperado)
    sqlManager.new_line(cenario_obj)

    sqlManager.update_date_rtf(id_rtf)

    flash("Linha Adicionada...")
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

@app.route("/edit_cenario/<int:id_rtf>/<int:pagina>/<int:linha>/", methods=["GET", "POST"])
def edit_cenario(id_rtf, pagina, linha):
    cenario = sqlManager.busca_cenarios(id_rtf, pagina, linha)

    if request.method == "POST":
        cenario.cenario = request.form["cenario"]
        cenario.resultado_esperado = request.form["resultado_esperado"]
        cenario.status = request.form["status"]
        cenario.massa_teste = request.form["massa_teste"]
        cenario.log_execucao = request.form["log_execucao"]

        sqlManager.update_date_rtf(id_rtf)

        sqlManager.update_cenario(cenario)

        return redirect(url_for('viewCenarios', id_rtf=id_rtf, pagina=pagina))

    return render_template("editar_cenario.html", cenario=cenario)


@app.route("/viewRTF", methods=["POST", "GET"])
def viewRTF():

    if request.method == "POST":
        busca = request.form["busca"]
        rtfs = sqlManager.viewRTF_name(busca)
    else:
        rtfs = sqlManager.viewRTF_all()

    return render_template("viewRTFs.html", values=rtfs)\


@app.route("/viewCenarios/<int:id_rtf>/<int:pagina>")
def viewCenarios(id_rtf, pagina):
    rtf = sqlManager.get_one_rtf(id_rtf)

    try:
        pagina_obj = sqlManager.busca_pagina(id_rtf, pagina)
    except TypeError: # pagina não existe... RTF vazio:
        # se tentar abrir um RTF vazio, vai criar uma pagina nova
        # adicionamente, irá forcar o qtd_pages = 1
        print("entrou no typeError")
        pagina_obj = sqlManager.add_pagina(id_rtf, nome=f"Pagina {1}", pagina=1)
        rtf.qtd_pages = 1
        sqlManager.update_qtd_pages_rtf(id_rtf, qtd_pages=1)
        sqlManager.commit()

    try:
        cenarios = sqlManager.busca_cenarios_pagina(pagina_obj.id_pagina)

        if not cenarios:
            lista_cenarios_RTF_inteiro = sqlManager.busca_cenarios_rtf(id_rtf)

            if not lista_cenarios_RTF_inteiro:
                raise AttributeError("Lista de Cenarios Vazia")

        qtd_pages = rtf.qtd_pages  # tenta pegar a qtd_paginas, se n conseguir, o array está vazio
        print(qtd_pages)
        rtf_nome = rtf.name
        nome_pagina = pagina_obj.nome
        return render_template("viewCenarios.html", values=cenarios, rtf_nome=rtf_nome, id_rtf=id_rtf, pagina=pagina, qtd_pages=qtd_pages, nome_pagina=nome_pagina)
    except AttributeError:
        # se tentar abrir um RTF sem cenarios, vai pedir para criar um cenário na pagina 1

        flash('RTF está sem nenhum cenário! Adicione o primeiro ;D')
        return render_template("adicionar_cenario.html", id_rtf=id_rtf, pagina=1)


@app.route("/delete_rtf/<int:id>")
def delete_rtf(id):
    rtf = sqlManager.get_one_rtf(id)

    lista_de_paginas = sqlManager.busca_paginas_by_id_rtf(rtf.id)

    lista_de_cenarios = []
    for pagina in lista_de_paginas:
        cenarios_pagina_atual = sqlManager.busca_cenarios_pagina(pagina.id_pagina)
        for cenario in cenarios_pagina_atual:
            lista_de_cenarios.append(cenario)

    sqlManager.apaga_lista_cenarios(lista_de_cenarios)
    sqlManager.apaga_lista_paginas(lista_de_paginas)
    sqlManager.delete_rtf(rtf)

    sqlManager.commit()

    flash('RTF removido com sucesso!')
    return redirect(url_for("viewRTF"))

@app.route("/delete_cenario/<int:id_rtf>/<int:pagina>/<int:linha>")
def delete_cenario(id_rtf, pagina, linha):
    print("entrando na funcao de delecao")
    cenario = sqlManager.busca_cenarios(id_rtf, pagina, linha)
    sqlManager.delete_cenario(cenario)
    sucess = ajust_num_linhas(id_rtf, pagina)

    if sucess:
        sqlManager.commit()
        flash('Cenário removido com sucesso!')
    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

def ajust_num_linhas(id_rtf, pagina):
    cenarios = sqlManager.busca_cenarios_pagina_v2(id_rtf, pagina)
    for count, cenario in enumerate(cenarios):
        cenario.linha = count+1
        sqlManager.update_linha_cenario(cenario)
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
    rtf = sqlManager.get_one_rtf(id_rtf)
    pagina_nova = pagina_atual + 1
    pagina_obj = models.Pagina(id_rtf=id_rtf, pagina=pagina_nova, nome=f"Pagina {pagina_nova}")

    sqlManager.add_pagina(id_rtf=id_rtf, pagina=pagina_obj.pagina, nome=pagina_obj.nome)

    if rtf.qtd_pages > 1:
        rtf.qtd_pages += 1
        sqlManager.update_qtd_pages_rtf(id_rtf, rtf.qtd_pages)
        # começa organizando da pagina nova, pois a ideia é deixar a atual no mesmo estado
        organiza_paginas(id_rtf, pagina_nova, "add")
    else:
        rtf.qtd_pages += 1
        sqlManager.update_qtd_pages_rtf(id_rtf, rtf.qtd_pages)

    print("vai entrar no commit")
    sqlManager.commit()
    print("passou pelo commit")

    return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina_nova))

def organiza_paginas(id_rtf, pagina_atual, modo):
    rtf = sqlManager.get_one_rtf(id_rtf)

    if modo.__eq__("add"):
        # condicao de parada das chamadas recursivas
        if pagina_atual >= rtf.qtd_pages:  # preciso olhar todas as paginas
            return

        cenarios = sqlManager.busca_cenarios_pagina_v2(id_rtf, pagina_atual)
        pagina_obj = sqlManager.busca_pagina(id_rtf, pagina_atual)

        proxima_pagina = pagina_atual+1
        organiza_paginas(id_rtf, proxima_pagina, "add")

        # passa os cenarios da pagina atual para a proxima pagina q está confirmadamente vazia
        for cenario in cenarios:
            cenario.pagina = proxima_pagina
            sqlManager.update_pagina_cenario(cenario)

        # quando chegar aqui pela primeira vez o rtf já tem pagina_atual == qtd_paginas
        # porém o add no DB ainda n foi commitado
        # portanto pagina_obj = None quando pagina_atual == rtf.qtd_pages
        # por isso só preciso até o ultimo numero antes
        # olhar funcao "add_pagina"... pagina_nova já é o numero correto
        # se pagina_nova = 2, mesmo q qtd_pages seja 7, não vai afetar aqui... espero que eu entenda isso no futuro...
        # mas agr faz sentido...
        if pagina_atual < rtf.qtd_pages:
            pagina_obj.pagina += 1
            sqlManager.update_numero_pagina_v2(pagina_obj)

    if modo.__eq__("del"):
        # condicao de parada
        if pagina_atual > rtf.qtd_pages:  # preciso olhar todas as paginas a partir da que apaguei até a ultima
            return

        cenarios = sqlManager.busca_cenarios_pagina_v2(id_rtf, pagina_atual)
        pagina_obj = sqlManager.busca_pagina(id_rtf, pagina_atual)

        for cenario in cenarios:
            cenario.pagina -= 1
            sqlManager.update_pagina_cenario(cenario)

        pagina_obj.pagina -= 1
        sqlManager.update_numero_pagina_v2(pagina_obj)

        proxima_pagina = pagina_atual + 1
        organiza_paginas(id_rtf, proxima_pagina, "del")

    return

# deletar os cenarios da pagina
# deletar a pagina
# pegar todas as paginas que vinham depois da pagina deletada
# subtrair o numero da pagina para pagina -= 1
@app.route("/delete_pagina/<int:id_rtf>/<int:pagina>/")
def delete_pagina(id_rtf, pagina):
    rtf = sqlManager.get_one_rtf(id_rtf)
    pagina_obj = sqlManager.busca_pagina(id_rtf, pagina)
    lista_cenarios = sqlManager.busca_cenarios_pagina(pagina_obj.id_pagina)

    print(f"id_rtf: {id_rtf}; pagina: {pagina}")
    print(pagina_obj)

    if rtf.qtd_pages == 1:
        flash('Não é permitido apagar a única página do RTF')
        return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))
    else:
        sqlManager.apaga_lista_cenarios(lista_cenarios)

        organiza_paginas(id_rtf, pagina, "del")

        rtf.qtd_pages -= 1
        sqlManager.update_qtd_pages_rtf(id_rtf, rtf.qtd_pages)

        sqlManager.delete_pagina(pagina_obj)

    sqlManager.commit()

    flash('A pagina foi removida com sucesso')

    ultima_pagina = rtf.qtd_pages+1
    if pagina == ultima_pagina:  # quando a pagina excluida for a ultima pagina do rtf
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
    pagina_obj = sqlManager.busca_pagina(id_rtf, pagina)


    if request.method == "POST":
        pagina_obj.nome = request.form["novo_nome"]

        sqlManager.update_date_rtf(id_rtf)
        sqlManager.update_nome_pagina(pagina_obj)

        flash("Nome alterado com Sucesso!")
        return redirect(url_for("viewCenarios", id_rtf=id_rtf, pagina=pagina))

    return render_template("editar_nome_pagina.html", id_rtf=id_rtf, pagina=pagina, nome=pagina_obj.nome)


if __name__ == '__main__':
    app.run(debug=True)
