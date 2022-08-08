-- SELECT ALL
SELECT * FROM CRUD_RTFs.Pagina;

-- SELECT ALL PAGES FROM A RTF
SELECT * 
FROM CRUD_RTFs.Pagina
WHERE id_rtf = 3;

-- SELECT 1 pagina especifica de 1 rtf especifico
SELECT *
FROM CRUD_RTFs.Pagina
WHERE id_rtf=3 and id_pagina=2;


SELECT pagina
FROM CRUD_RTFs.Pagina
WHERE id_pagina=3;

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


-- DELETE Paginas (essa query apaga todos os registros)
DELETE FROM CRUD_RTFs.Pagina WHERE id_pagina!=0;

-- DELETE Paginas From a specific RTF
DELETE FROM CRUD_RTFs.Pagina WHERE id_pagina=3;

-- DELETE de uma PAGINA especifica de 1 RTF
DELETE FROM CRUD_RTFs.Pagina WHERE id_rtf=3 and id_pagina=2

-- Deleta a Table
DROP TABLE CRUD_RTFs.Pagina;