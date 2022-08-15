-- SELECT ALL
SELECT * FROM CRUD_RTFs.RTFs;

-- SELECT BY NAME
SELECT * 
FROM CRUD_RTFs.RTFs
WHERe NAME like "%F%";

-- SELECT BY Id
SELECT * 
FROM CRUD_RTFs.RTFs
WHERe RTFs.id=3;

UPDATE CRUD_RTFs.RTFs
SET qtd_pages = 3
WHERE id=3;


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


UPDATE CRUD_RTFs.RTFs
SET
name = 'xulio',
descricao = 'coca',
data_update = '2022-08-01',
data_update_formatada = '01/08/2022'
WHERE id = 3;



-- DELETE RTF (essa query apaga todos os registros)
DELETE FROM CRUD_RTFs.RTFs WHERE id != 0;

-- Deleta a table
DROP TABLE CRUD_RTFs.RTFs;