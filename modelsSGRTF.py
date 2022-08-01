import helpers
from datetime import date

class RTFs():
    data = helpers.get_data_formatada()
    def __init__(self, id=None, name=None, descricao=None, qtd_pages=1, data_criacao=date.today(), data_update=date.today(), data_criacao_formatada=data, data_update_formatada=data):
        self.id = id
        self.name = name
        self.descricao = descricao
        self.qtd_pages = qtd_pages
        self.data_criacao = data_criacao
        self.data_update = data_update
        self.data_criacao_formatada = data_criacao_formatada
        self.data_update_formatada = data_update_formatada


class Pagina():
    def __init__(self, id_rtf, numero, nome, id_pagina=None):
        self.id_pagina = id_pagina
        self.id_rtf = id_rtf
        self.numero = numero
        self.nome = nome


class Cenarios():
    def __init__(self, id_rtf, id_pagina, pagina, linha, cenario, resultado_esperado, id_cenario=None):
        self.id_cenario = id_cenario
        self.id_rtf = id_rtf
        self.id_pagina = id_pagina
        self.linha = linha
        self.cenario = cenario
        self.resultado_esperado = resultado_esperado
        self.status = 0
        self.massa_teste= '-'
        self.log_execucao = '-'