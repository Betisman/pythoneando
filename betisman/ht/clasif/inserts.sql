sqlite> .dump equipos
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
INSERT INTO "equipos" VALUES(1,'Betis',5,5,0,0,12,1,11,15,'A');
INSERT INTO "equipos" VALUES(4,'Madrid',5,3,0,2,4,6,-2,9,'A');
INSERT INTO "equipos" VALUES(5,'Antequera',5,2,1,2,8,10,-2,7,'A');
INSERT INTO "equipos" VALUES(3,'Guadalajara',5,2,1,2,10,6,4,7,'A');
INSERT INTO "equipos" VALUES(2,'Periana',5,2,1,2,12,12,0,7,'A');
INSERT INTO "equipos" VALUES(8,'Belchite',5,2,1,2,7,6,1,7,'A');
INSERT INTO "equipos" VALUES(6,'Galapagar',5,1,0,4,6,14,-8,3,'A');
INSERT INTO "equipos" VALUES(7,'Santafe',5,1,0,4,6,10,-4,3,'A');
CREATE TABLE equipostemp (
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