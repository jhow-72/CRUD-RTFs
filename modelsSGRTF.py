import helpers
from datetime import date

class RTFs():
    data = helpers.get_data_formatada()
    def __init__(self, id=None, name=None, descricao=None, qtd_pages=1, squad='online', data_criacao=date.today(), data_update=date.today(), data_criacao_formatada=data, data_update_formatada=data):
        self.id = id
        self.name = name
        self.descricao = descricao
        self.qtd_pages = qtd_pages
        self.squad = squad
        self.data_criacao = data_criacao
        self.data_update = data_update
        self.data_criacao_formatada = data_criacao_formatada
        self.data_update_formatada = data_update_formatada


class Pagina():
    def __init__(self, id_rtf=None, pagina=None, nome=None, id_pagina=None):
        self.id_pagina = id_pagina
        self.id_rtf = id_rtf
        self.pagina = pagina
        self.nome = nome


class Cenarios():
    def __init__(self, id_rtf, id_pagina, linha, cenario, resultado_esperado, status=0, massa_teste='-', log_execucao='-', id_cenario=None, pagina=None):
        self.id_cenario = id_cenario
        self.id_rtf = id_rtf
        self.id_pagina = id_pagina
        self.linha = linha
        self.cenario = cenario
        self.resultado_esperado = resultado_esperado
        self.status = status
        self.massa_teste = massa_teste
        self.log_execucao = log_execucao
        self.pagina = pagina

