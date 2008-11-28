--init
DROP TABLE equipos;
DROP TABLE equipostemp;
BEGIN TRANSACTION;
CREATE TABLE equipos (
id integer(10) not null primary key,
pj integer(2) not null,
g integer(2) not null,
e integer(2) not null,
p integer(2) not null,
gf integer(3) not null,
gc integer(3) not null,
avg integer(3) not null,
ptos integer(3) not null, grupo varchar(1));
--INSERT INTO "equipos" VALUES(487829,0,0,0,0,0,0,0,0,"A");
--INSERT INTO "equipos" VALUES(1436965,0,0,0,0,0,0,0,0,"B");
--INSERT INTO "equipos" VALUES(992758,0,0,0,0,0,0,0,0,"B");
--INSERT INTO "equipos" VALUES(989753,0,0,0,0,0,0,0,0,"B");
--INSERT INTO "equipos" VALUES(492014,0,0,0,0,0,0,0,0,"A");
--INSERT INTO "equipos" VALUES(1457502,0,0,0,0,0,0,0,0,"A");
--INSERT INTO "equipos" VALUES(48756,0,0,0,0,0,0,0,0,"B");
--INSERT INTO "equipos" VALUES(799149,0,0,0,0,0,0,0,0,"B");
--INSERT INTO "equipos" VALUES(491940,0,0,0,0,0,0,0,0,"A");
--INSERT INTO "equipos" VALUES(1458361,0,0,0,0,0,0,0,0,"A");
--INSERT INTO "equipos" VALUES(1369155,0,0,0,0,0,0,0,0,"A");
--INSERT INTO "equipos" VALUES(988358,0,0,0,0,0,0,0,0,"A");
--INSERT INTO "equipos" VALUES(1462225,0,0,0,0,0,0,0,0,"A");
--INSERT INTO "equipos" VALUES(492560,0,0,0,0,0,0,0,0,"B");
--INSERT INTO "equipos" VALUES(779367,0,0,0,0,0,0,0,0,"B");
--INSERT INTO "equipos" VALUES(1369963,0,0,0,0,0,0,0,0,"B");
--CREATE TABLE equipostemp AS SELECT * FROM equipos;
COMMIT;