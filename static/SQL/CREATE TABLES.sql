CREATE TABLE RTFs (
    id int auto_increment,
    name varchar(100) NOT NULL,
    descricao varchar(500) NOT NULL,
    qtd_pages int,
    data_criacao date NOT NULL,
    data_update date NOT NULL,
    data_criacao_formatada varchar(10),
    data_update_formatada varchar(10),
    PRIMARY KEY(id)
);


CREATE TABLE Pagina (
	id_pagina int auto_increment,
    numero int NOT NULL,
    nome varchar(30) NOT NULL,
    PRIMARY KEY(id_pagina)
);


CREATE TABLE Cenarios(
	id_cenario int auto_increment,
    linha int NOT NULL,
    cenario varchar(250) NOT NULL DEFAULT 'TBD',
    resultado_esperado varchar(250) NOT NULL DEFAULT 'TBD',
    status int NOT NULL,
    massa_teste  varchar(1000),
    log_execucao  varchar(10000),
    PRIMARY KEY(id_cenario)
);