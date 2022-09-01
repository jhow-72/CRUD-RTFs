-- SELECT ALL
SELECT * FROM CRUD_RTFs.Pagina;

-- SELECT ALL PAGES FROM A RTF
SELECT * 
FROM CRUD_RTFs.Pagina
WHERE id_rtf = 3;

SELECT *
FROM CRUD_RTFs.Pagina
where nome like "Pagina%";

DELETE
FROM CRUD_RTFs.Pagina
where nome like "Pagina%";

-- SELECT 1 pagina especifica de 1 rtf especifico
SELECT *
FROM CRUD_RTFs.Pagina
WHERE id_rtf=3 and id_pagina=1;

SELECT *
FROM CRUD_RTFs.Pagina
WHERE id_rtf=3 and pagina=1;

SELECT *
FROM CRUD_RTFs.Pagina
WHERE id_pagina=2;

-- ADD NEW Pagina
INSERT INTO `CRUD_RTFs`.`Pagina` (`numero`, `nome`, `id_rtf`)
VALUES (1, 'paçoca', 3);

INSERT INTO `CRUD_RTFs`.`Pagina` (`numero`, `nome`, `id_rtf`)
VALUES (2, 'sashimi', 3);

INSERT INTO `CRUD_RTFs`.`Pagina` (`numero`, `nome`, `id_rtf`)
VALUES (3, 'bife angus', 3);

INSERT INTO `CRUD_RTFs`.`Pagina` (`numero`, `nome`, `id_rtf`)
VALUES (1, 'pizza', 4);

INSERT INTO `CRUD_RTFs`.`Pagina` (`numero`, `nome`, `id_rtf`)
VALUES (2, 'salmão grelhado', 4);


UPDATE CRUD_RTFs.Pagina
SET
pagina = 3
WHERE id_rtf=3 and pagina=2;

-- DELETE Paginas (essa query apaga todos os registros)
DELETE FROM CRUD_RTFs.Pagina WHERE id_pagina!=0;

-- DELETE Paginas From a specific RTF
DELETE FROM CRUD_RTFs.Pagina WHERE id_rtf=3;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM CRUD_RTFs.Pagina WHERE nome='Pagina 1';

-- DELETE de uma PAGINA especifica de 1 RTF
DELETE FROM CRUD_RTFs.Pagina WHERE id_rtf=3 and id_pagina=2;


DELETE FROM CRUD_RTFs.Pagina;

-- Deleta a Table
DROP TABLE CRUD_RTFs.Pagina;