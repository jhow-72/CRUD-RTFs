ALTER TABLE CRUD_RTFs.RTFs
ADD COLUMN squad varchar(8);

UPDATE CRUD_RTFs.RTFs
SET squad = 'online'
WHERE RTFs.id > 0;

ALTER TABLE CRUD_RTFs.Pagina
RENAME COLUMN numero TO pagina;