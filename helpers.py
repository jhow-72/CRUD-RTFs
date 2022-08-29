from datetime import timedelta, datetime, date
import modelsSGRTF as models

def get_data_formatada():
    data = date.today()
    data = data.strftime('%d/%m/%Y')
    return data

def get_data():
    return date.today()

# constroi um objeto RTF
def constroi_rtf(rtf):
    # seta propriedades
    id, name, descricao, qtd_pages, squad = rtf[0], rtf[1], rtf[2], rtf[3], rtf[8]
    data_criacao, data_update, data_criacao_formatada, data_update_formatada = rtf[4], rtf[5], rtf[6], rtf[7]
    rtf_temp = models.RTFs(id=id, name=name, descricao=descricao, qtd_pages=qtd_pages, data_criacao=data_criacao, data_update=data_update, data_criacao_formatada=data_criacao_formatada, data_update_formatada=data_update_formatada, squad=squad)

    return rtf_temp

# cria uma lista de objetos RTF
def cria_lista_rtfs(rtfs):
    lista_obj_rtfs = []
    for rtf in rtfs:
        rtf_temp = constroi_rtf(rtf)
        lista_obj_rtfs.append(rtf_temp)

    return lista_obj_rtfs

def cria_lista_paginas(paginas):
    lista_obj_paginas = []
    for pagina in paginas:
        pagina_temp = constroi_pagina(pagina)
        lista_obj_paginas.append(pagina_temp)

    return lista_obj_paginas

def constroi_cenario(cenario_obj, pagina=None):

    id_cenario, linha, cenario, resultado_esperado = cenario_obj[0], cenario_obj[1], cenario_obj[2], cenario_obj[3]
    status = cenario_obj[4]
    massa_teste = cenario_obj[5]
    log_execucao = cenario_obj[6]
    id_rtf, id_pagina = cenario_obj[7], cenario_obj[8]

    cenario_temp = models.Cenarios(id_cenario=id_cenario, linha=linha, cenario=cenario, resultado_esperado=resultado_esperado, status=status, massa_teste=massa_teste, log_execucao=log_execucao, id_rtf=id_rtf, id_pagina=id_pagina, pagina=pagina)

    return cenario_temp

def cria_lista_cenarios(cenarios, pagina=None):
    lista_obj_cenarios = []
    for cenario in cenarios:
        cenario_temp = constroi_cenario(cenario, pagina)
        lista_obj_cenarios.append(cenario_temp)

    return lista_obj_cenarios

# constroi um objeto Pagina
def constroi_pagina(pagina_obj):
    # seta propriedades
    id_pagina, pagina, nome, id_rtf, = pagina_obj[0], pagina_obj[1], pagina_obj[2], pagina_obj[3]
    pagina_obj_temp = models.Pagina(id_pagina=id_pagina, pagina=pagina, nome=nome, id_rtf=id_rtf)

    return pagina_obj_temp