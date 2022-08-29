import mysql.connector as sql
import modelsSGRTF as models
import helpers

db = sql.connect(
    host='localhost',
    user='root',
    passwd='07022109Ju+',
    database="CRUD_RTFs"
)
print('conexão db estabelecida')

cursor = db.cursor()

def commit():
    db.commit()

# Funcoes dos RTFs

def viewRTF_all():
    comando = '''SELECT * FROM CRUD_RTFs.RTFs;'''
    cursor.execute(comando)
    rtfs = cursor.fetchall()

    cursor.reset()
    return helpers.cria_lista_rtfs(rtfs)


def viewRTF_name(substring):
    comando = f'''SELECT * FROM CRUD_RTFs.RTFs WHERE NAME like "%{substring}%";'''
    cursor.execute(comando)
    rtfs = cursor.fetchall()

    cursor.reset()
    return helpers.cria_lista_rtfs(rtfs)

def add_rtf(rtf):
    comando = f'''INSERT INTO `CRUD_RTFs`.`RTFs`(`name`, `descricao`, `qtd_pages`, `data_criacao`, `data_update`, `data_criacao_formatada`, `data_update_formatada`, `squad`)
                 VALUES ( '{rtf.name}', '{rtf.descricao}', {rtf.qtd_pages}, '{rtf.data_criacao}', '{rtf.data_update}', '{rtf.data_criacao_formatada}', '{rtf.data_update_formatada}', '{rtf.squad}');'''
    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return

def get_one_rtf(id):
    comando = f'''SELECT * FROM CRUD_RTFs.RTFs WHERE id = {id};'''
    cursor.execute(comando)
    rtf = cursor.fetchone()

    cursor.reset()
    return helpers.constroi_rtf(rtf)

def edit_rtf(rtf):
    comando = f'''UPDATE CRUD_RTFs.RTFs
                    SET name = '{rtf.name}', descricao = '{rtf.descricao}', data_update = '{rtf.data_update}', data_update_formatada = '{rtf.data_update_formatada}'
                  WHERE id = {rtf.id};'''
    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return

## TO-DO (após paginas e cenários estarem prontos)
def delete_rtf():
    pass

def update_qtd_pages_rtf(id_rtf, qtd_pages):
    comando = f"""UPDATE CRUD_RTFs.RTFs
                 SET qtd_pages = {qtd_pages}
                 WHERE id={id_rtf};"""
    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return

def update_date_rtf(id_rtf):
    data_update = helpers.get_data()
    data_update_formatada = helpers.get_data_formatada()

    comando = f"""UPDATE CRUD_RTFs.RTFs
                 SET data_update='{data_update}', data_update_formatada='{data_update_formatada}'
                 WHERE id={id_rtf};"""

    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return

### Funcoes das paginas

def busca_pagina(id_rtf, pagina):
    comando = f"""SELECT *
                 FROM CRUD_RTFs.Pagina
                 WHERE id_rtf={id_rtf} and pagina={pagina};"""
    cursor.execute(comando)
    pagina_obj = cursor.fetchone()

    cursor.reset()
    return helpers.constroi_pagina(pagina_obj)

def busca_numero_pagina_as_pagina(id_pagina):
    comando = f"""SELECT pagina
                  FROM CRUD_RTFs.Pagina
                  WHERE id_pagina={id_pagina};"""
    cursor.execute(comando)
    resultado = cursor.fetchone()
    pagina = resultado[0]

    cursor.reset()
    return pagina

# adiciona uma pagina no banco e retorna a mesma
def add_pagina(id_rtf, nome, pagina):
    comando = f"""INSERT INTO CRUD_RTFs.Pagina (id_rtf, nome, pagina)
                  VALUES ({id_rtf}, '{nome}', {pagina});"""
    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return busca_pagina(id_rtf, pagina)

def update_numero_pagina(id_rtf, pagina_atual, pagina_nova):
    comando = f"""UPDATE CRUD_RTFs.Pagina
                  SET pagina={pagina_nova}
                  WHERE id_rtf={id_rtf} and pagina={pagina_atual};"""
    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return

def busca_id_1_pagina(id_rtf, pagina):
    pagina_obj = busca_pagina(id_rtf, pagina)
    return pagina_obj.id_pagina

def update_nome_pagina(pagina_obj):
    comando = f"""UPDATE CRUD_RTFs.Pagina
                  SET nome='{pagina_obj.nome}'
                  WHERE id_pagina={pagina_obj.id_pagina};"""

    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return

### Funcoes dos cenarios
def busca_cenarios_pagina(id_pagina):
    comando = f"""SELECT * FROM CRUD_RTFs.Cenarios WHERE id_pagina={id_pagina};"""
    cursor.execute(comando)
    cenarios = cursor.fetchall()

    pagina = busca_numero_pagina_as_pagina(id_pagina)

    cursor.reset()
    return helpers.cria_lista_cenarios(cenarios, pagina)

def busca_cenarios_pagina_v2(id_rtf, pagina):
    comando = f"""SELECT *
                  FROM CRUD_RTFs.Cenarios as Cn
                      INNER JOIN CRUD_RTFs.Pagina AS Pg ON Pg.id_pagina = Cn.id_pagina
                      INNER JOIN CRUD_RTFs.RTFs AS RTF ON RTF.id = Cn.id_rtf
                  WHERE Pg.pagina={pagina} AND RTF.id={id_rtf};"""
    cursor.execute(comando)
    cenarios = cursor.fetchall()

    cursor.reset()
    return helpers.cria_lista_cenarios(cenarios, pagina)

# busca todos os cenarios de 1 rtf especifico
def busca_cenarios_rtf(id_rtf):
    comando = f"""SELECT * FROM CRUD_RTFs.Cenarios WHERE id_rtf={id_rtf};"""
    cursor.execute(comando)
    cenarios = cursor.fetchall()

    cursor.reset()
    return helpers.cria_lista_cenarios(cenarios)

# busca 1 linha (cenario) em uma pagina específica usando o numero da pagina (as pagina)
def busca_cenarios(id_rtf, pagina, linha):
    comando = f"""SELECT * 
                  FROM CRUD_RTFs.Cenarios as Cn
                      INNER JOIN CRUD_RTFs.Pagina AS Pg ON Pg.id_pagina = Cn.id_pagina
                      INNER JOIN CRUD_RTFs.RTFs AS RTF ON RTF.id = Cn.id_rtf
                  WHERE linha={linha} and Pg.pagina={pagina} and RTF.id={id_rtf};"""

    cursor.execute(comando)
    cenario = cursor.fetchone()

    cursor.reset()
    return helpers.constroi_cenario(cenario)

def get_qtd_cenarios_pagina(id_rtf, pagina):
    cenarios = busca_cenarios_pagina_v2(id_rtf, pagina)
    return len(cenarios)

def get_maior_linha_pagina(id_rtf, pagina):
    cenarios = busca_cenarios_pagina_v2(id_rtf, pagina)
    resposta = 0
    for cenario in cenarios:
        if cenario.linha > resposta:
            resposta = cenario.linha

    return resposta

def update_cenario(cenario):
    id_cenario = cenario.id_cenario

    comando = f"""UPDATE CRUD_RTFs.Cenarios
                      SET cenario='{cenario.cenario}',
                          resultado_esperado='{cenario.resultado_esperado}',
                          status={cenario.status},
                          massa_teste='{cenario.massa_teste}',
                          log_execucao='{cenario.log_execucao}'
                      WHERE id_cenario={id_cenario};"""
    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return


def new_line(cenario):

    comando = f"""INSERT INTO CRUD_RTFs.Cenarios (linha,cenario,resultado_esperado,status,massa_teste,log_execucao,id_rtf,id_pagina)
                  VALUES ('{cenario.linha}','{cenario.cenario}','{cenario.resultado_esperado}',{cenario.status},NULL,NULL,{cenario.id_rtf},{cenario.id_pagina});"""
    cursor.execute(comando)
    db.commit()

    cursor.reset()
    return

def delete_cenario(cenario):
    id_cenario = cenario.id_cenario

    comando = f"""DELETE 
                  FROM CRUD_RTFs.Cenarios 
                  WHERE id_cenario={id_cenario};"""

    cursor.execute(comando)
    cursor.reset()
    return

def update_linha_cenario(cenario):

    comando = f"""UPDATE CRUD_RTFs.Cenarios
                      SET linha='{cenario.linha}'
                      WHERE id_cenario={cenario.id_cenario};"""
    cursor.execute(comando)
    cursor.reset()
    return

# cursor.execute('''SELECT *
# FROM CRUD_RTFs.Cenarios
# WHERe linha=1 and id_pagina=3 and id_rtf=3;''')
#
# cenario = cursor.fetchone()
# print(cenario)
#
# # for x in cursor:
# #     print(x)
#
