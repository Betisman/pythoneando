--init
DROP TABLE equipos;
DROP TABLE equipostemp;
BEGIN TRANSACTION;
CREATE TABLE equipos (
id integer(10) not null primary key,
nombre varchar(50) not null,
pj integer(2) not null,
g integer(2) not null,
e integer(2) not null,
p integer(2) not null,
gf integer(3) not null,
gc integer(3) not null,
avg integer(3) not null,
ptos integer(3) not null, grupo varchar(1));
INSERT INTO "equipos" VALUES(487829,"Real Betisman Balompié",0,0,0,0,0,0,0,0,"A");
INSERT INTO "equipos" VALUES(1436965,"A.D. Dimitri PITERMAN",0,0,0,0,0,0,0,0,"B");
INSERT INTO "equipos" VALUES(1581841,"Chaconcines",0,0,0,0,0,0,0,0,"B");
INSERT INTO "equipos" VALUES(989753,"CONGRIO F.C.",0,0,0,0,0,0,0,0,"A");
INSERT INTO "equipos" VALUES(492014,"Espino F.C",0,0,0,0,0,0,0,0,"B");
INSERT INTO "equipos" VALUES(1457502,"Inframundo CD Drogadictos anónimos",0,0,0,0,0,0,0,0,"B");
INSERT INTO "equipos" VALUES(48756,"Jumfrys F.K.",0,0,0,0,0,0,0,0,"B");
INSERT INTO "equipos" VALUES(799149,"milan chupao",0,0,0,0,0,0,0,0,"A");
INSERT INTO "equipos" VALUES(491940,"Pitisianos SAD",0,0,0,0,0,0,0,0,"A");
INSERT INTO "equipos" VALUES(1458361,"Real Servelete de Carfesan",0,0,0,0,0,0,0,0,"A");
INSERT INTO "equipos" VALUES(1369155,"ThePiso",0,0,0,0,0,0,0,0,"B");
INSERT INTO "equipos" VALUES(988358,"Raul Gran Capitan",0,0,0,0,0,0,0,0,"A");
INSERT INTO "equipos" VALUES(1462225,"Bukakke Team",0,0,0,0,0,0,0,0,"A");
INSERT INTO "equipos" VALUES(492560,"ollauris F.C.",0,0,0,0,0,0,0,0,"B");
INSERT INTO "equipos" VALUES(779367,"Caranza F.C.",0,0,0,0,0,0,0,0,"B");
INSERT INTO "equipos" VALUES(1369963,"Hapiio FC",0,0,0,0,0,0,0,0,"A");
CREATE TABLE equipostemp AS SELECT * FROM equipos;
COMMIT;