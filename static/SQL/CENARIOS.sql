-- SELECT ALL
SELECT * FROM CRUD_RTFs.Cenarios;

-- SELECT 1 linha em uma pagina específica
SELECT * 
FROM CRUD_RTFs.Cenarios
WHERe linha=1 and id_pagina=3 and id_rtf=3;

-- SELECT ALL BY PAGINA
SELECT * FROM CRUD_RTFs.Cenarios WHERE id_pagina=2;


-- ADD NEW Cenario
INSERT INTO `CRUD_RTFs`.`Cenarios`(`linha`,`cenario`,`resultado_esperado`,`status`,`massa_teste`,`log_execucao`,`id_rtf`,`id_pagina`)
VALUES (1,'TBD','TBD',0,NULL,NULL,3,2);

INSERT INTO `CRUD_RTFs`.`Cenarios`(`linha`,`cenario`,`resultado_esperado`,`status`,`massa_teste`,`log_execucao`,`id_rtf`,`id_pagina`)
VALUES (2,'TBD','TBD',0,NULL,NULL,3,2);

INSERT INTO `CRUD_RTFs`.`Cenarios`(`linha`,`cenario`,`resultado_esperado`,`status`,`massa_teste`,`log_execucao`,`id_rtf`,`id_pagina`)
VALUES (3,'TBD','TBD',0,NULL,NULL,3,2);

INSERT INTO `CRUD_RTFs`.`Cenarios`(`linha`,`cenario`,`resultado_esperado`,`status`,`massa_teste`,`log_execucao`,`id_rtf`,`id_pagina`)
VALUES (1,'TBD','TBD',0,NULL,NULL,3,3);


-- UPDATES
-- edit_cenario(id_rtf, pagina, linha) 
UPDATE CRUD_RTFs.Cenarios
SET 
WHERE

UPDATE `CRUD_RTFs`.`Cenarios`
SET
`id_cenario` = <{id_cenario: }>,
`linha` = <{linha: }>,
`cenario` = <{cenario: TBD}>,
`resultado_esperado` = <{resultado_esperado: TBD}>,
`status` = <{status: }>,
`massa_teste` = <{massa_teste: }>,
`log_execucao` = <{log_execucao: }>,
`id_rtf` = <{id_rtf: }>,
`id_pagina` = <{id_pagina: }>
WHERE `id_cenario` = <{expr}>;


-- DELETE Cenario (essa query apaga todos os registros)
DELETE FROM CRUD_RTFs.Cenarios WHERE id != 0;

-- DELETE de um cenário especifico
DELETE FROM CRUD_RTFs.Cenarios WHERE linha=1 and id_pagina=3 and id_rtf=3;

-- DELETE de um cenário especifico via id
DELETE FROM CRUD_RTFs.Cenarios WHERE id_cenario=3;


-- Deleta a table
DROP TABLE CRUD_RTFs.Cenarios;

-- FALTAM os updates!!!!!!!!!!!!!!!!