import mysql.connector as sql
import modelsSGRTF as models
import helpers

db = sql.connect(
    host='localhost',
    user='root',
    passwd='07022109Ju+',
    database="CRUD_RTFs"
)
print('conexão estabelecida')

cursor = db.cursor()

# constroi um objeto RTF
def constroi_rtf(rtf):
    # seta propriedades
    id, name, descricao, qtd_pages = rtf[0], rtf[1], rtf[2], rtf[3]
    data_criacao, data_update, data_criacao_formatada, data_update_formatada = rtf[4], rtf[5], rtf[6], rtf[7]
    rtf_temp = models.RTFs(id, name, descricao, qtd_pages, data_criacao, data_update, data_criacao_formatada, data_update_formatada)

    return rtf_temp

# cria uma lista de objetos RTF
def cria_lista_rtfs(rtfs):
    lista_obj_rtfs = []
    for rtf in rtfs:
        rtf_temp = constroi_rtf(rtf)
        lista_obj_rtfs.append(rtf_temp)

    return lista_obj_rtfs

def viewRTF_all():
    comando = '''SELECT * FROM CRUD_RTFs.RTFs;'''
    cursor.execute(comando)
    rtfs = cursor.fetchall()

    return cria_lista_rtfs(rtfs)


def viewRTF_name(substring):
    comando = f'''SELECT * FROM CRUD_RTFs.RTFs WHERE NAME like "%{substring}%";'''
    cursor.execute(comando)
    rtfs = cursor.fetchall()

    return cria_lista_rtfs(rtfs)

def add_rtf(rtf):
    comando = f'''INSERT INTO `CRUD_RTFs`.`RTFs`(`name`, `descricao`, `qtd_pages`, `data_criacao`, `data_update`, `data_criacao_formatada`, `data_update_formatada`)
                 VALUES ( '{rtf.name}', '{rtf.descricao}', {rtf.qtd_pages}, '{rtf.data_criacao}', '{rtf.data_update}', '{rtf.data_criacao_formatada}', '{rtf.data_update_formatada}');'''
    cursor.execute(comando)
    db.commit()

    return

def get_one_rtf(id):
    comando = f'''SELECT * FROM CRUD_RTFs.RTFs WHERE id = {id};'''
    cursor.execute(comando)
    rtf = cursor.fetchone()

    return constroi_rtf(rtf)

def edit_rtf(rtf):
    comando = f'''UPDATE CRUD_RTFs.RTFs
                    SET name = '{rtf.name}', descricao = '{rtf.descricao}', data_update = '{rtf.data_update}', data_update_formatada = '{rtf.data_update_formatada}'
                  WHERE id = {rtf.id};'''
    cursor.execute(comando)
    db.commit()
    return

## TO-DO
def delete_rtf():
    pass


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
