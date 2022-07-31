-- SELECT ALL
SELECT * FROM CRUD_RTFs.RTFs;

-- SELECT BY NAME
SELECT * 
FROM CRUD_RTFs.RTFs
WHERe NAME like "%F%";

-- ADD NEW RTF
INSERT INTO `CRUD_RTFs`.`RTFs`
(`name`,
`descricao`,
`qtd_pages`,
`data_criacao`,
`data_update`,
`data_criacao_formatada`,
`data_update_formatada`)
VALUES
( 'FRB - Ajuste 2way', 'ajuste no retorno do 2way', 1, current_date(), current_date(), '30/07/2022', '30/07/2022');


-- DELETE RTF (essa query apaga todos os registros)
DELETE FROM CRUD_RTFs.RTFs WHERE id != 0;

-- Deleta a table
DROP TABLE CRUD_RTFs.RTFs;