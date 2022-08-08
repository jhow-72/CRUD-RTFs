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


# Funcoes dos RTFs

def viewRTF_all():
    comando = '''SELECT * FROM CRUD_RTFs.RTFs;'''
    cursor.execute(comando)
    rtfs = cursor.fetchall()

    return helpers.cria_lista_rtfs(rtfs)


def viewRTF_name(substring):
    comando = f'''SELECT * FROM CRUD_RTFs.RTFs WHERE NAME like "%{substring}%";'''
    cursor.execute(comando)
    rtfs = cursor.fetchall()

    return helpers.cria_lista_rtfs(rtfs)

def add_rtf(rtf):
    comando = f'''INSERT INTO `CRUD_RTFs`.`RTFs`(`name`, `descricao`, `qtd_pages`, `data_criacao`, `data_update`, `data_criacao_formatada`, `data_update_formatada`, `squad`)
                 VALUES ( '{rtf.name}', '{rtf.descricao}', {rtf.qtd_pages}, '{rtf.data_criacao}', '{rtf.data_update}', '{rtf.data_criacao_formatada}', '{rtf.data_update_formatada}', '{rtf.squad}');'''
    cursor.execute(comando)
    db.commit()

    return

def get_one_rtf(id):
    comando = f'''SELECT * FROM CRUD_RTFs.RTFs WHERE id = {id};'''
    cursor.execute(comando)
    rtf = cursor.fetchone()

    return helpers.constroi_rtf(rtf)

def edit_rtf(rtf):
    comando = f'''UPDATE CRUD_RTFs.RTFs
                    SET name = '{rtf.name}', descricao = '{rtf.descricao}', data_update = '{rtf.data_update}', data_update_formatada = '{rtf.data_update_formatada}'
                  WHERE id = {rtf.id};'''
    cursor.execute(comando)
    db.commit()
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
    return

### Funcoes das paginas

def busca_pagina(id_rtf, pagina):
    comando = f"""SELECT *
                 FROM CRUD_RTFs.Pagina
                 WHERE id_rtf={id_rtf} and pagina={pagina};"""
    cursor.execute(comando)
    pagina_obj = cursor.fetchone()

    return helpers.constroi_pagina(pagina_obj)

def busca_numero_pagina_as_pagina(id_pagina):
    comando = f"""SELECT pagina
                  FROM CRUD_RTFs.Pagina
                  WHERE id_pagina={id_pagina};"""
    cursor.execute(comando)
    resultado = cursor.fetchone()
    pagina = resultado[0]
    return pagina

def add_pagina(id_rtf, nome, pagina):
    comando = f"""INSERT INTO CRUD_RTFs.Pagina (id_rtf, nome, pagina)
                  VALUES ({id_rtf}, '{nome}', {pagina});"""
    cursor.execute(comando)
    db.commit()
    return

### Funcoes dos cenarios
def busca_cenarios_pagina(id_pagina):
    comando = f"""SELECT * FROM CRUD_RTFs.Cenarios WHERE id_pagina={id_pagina};"""
    cursor.execute(comando)
    cenarios = cursor.fetchall()

    pagina = busca_numero_pagina_as_pagina(id_pagina)

    return helpers.cria_lista_cenarios(cenarios, pagina)

def busca_cenarios_rtf(id_rtf):
    comando = f"""SELECT * FROM CRUD_RTFs.Cenarios WHERE id_rtf={id_rtf};"""
    cursor.execute(comando)
    cenarios = cursor.fetchall()

    return helpers.cria_lista_cenarios(cenarios)

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
