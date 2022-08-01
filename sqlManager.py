import mysql.connector as sql
import modelsSGRTF as models

db = sql.connect(
    host='localhost',
    user='root',
    passwd='07022109Ju+',
    database="CRUD_RTFs"
)
print('conexão estabelecida')

cursor = db.cursor()

def viewRTF_all():
    comando = '''SELECT * FROM CRUD_RTFs.RTFs;'''
    cursor.execute(comando)
    rtfs = cursor.fetchall()
    print(rtfs)
    lista_obj_rtfs = []
    for rtf in rtfs:
        id = rtf[0]
        name = rtf[1]
        descricao = rtf[2]
        qtd_pages = rtf[3]
        data_criacao = rtf[4]
        data_update = rtf[5]
        data_criacao_formatada = rtf[6]
        data_update_formatada = rtf[7]
        rtf_temp = models.RTFs(id, name,descricao,qtd_pages,data_criacao, data_update, data_criacao_formatada, data_update_formatada)
        lista_obj_rtfs.append(rtf_temp)

    return lista_obj_rtfs

def add_rtf(rtf):
    comando = f'''INSERT INTO `CRUD_RTFs`.`RTFs`(`name`, `descricao`, `qtd_pages`, `data_criacao`, `data_update`, `data_criacao_formatada`, `data_update_formatada`)
                 VALUES ( '{rtf.name}', '{rtf.descricao}', {rtf.qtd_pages}, '{rtf.data_criacao}', '{rtf.data_update}', '{rtf.data_criacao_formatada}', '{rtf.data_update_formatada}');'''
    cursor.execute(comando)
    db.commit()
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
