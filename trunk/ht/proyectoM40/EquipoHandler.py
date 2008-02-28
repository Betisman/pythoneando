#!/usr/bin/env python
# coding=ISO-8859-1
from pysqlite2 import dbapi2 as sqlite


class EquipoHandler(Equipo):
	def __init__(self, equipo):
		self.equipo = equipo
		self.con = sqlite.connect("ht.sqlite")
		self.cur = con.cursor()

#SELECT = "select * from equipos where grupo = 'A' order by ptos desc, avg desc, gf desc"

# 1. Iterate over the rows available from the cursor, unpacking the
# resulting sequences to yield their elements (name_last, age):
# cur.execute(SELECT)
# for (name_last, age) in cur:
    # print '%s is %d years old.' % (name_last, age)

# 2. Equivalently:
# cur.execute(SELECT)
# for row in cur:
    # print row

def printAll():
	con = sqlite.connect("ht.sqlite")
	cur.execute(SELECT)
	for row in cur:
	    print row


def actualizarEquipo(equipo):
	actualizarEquipo(equipo.nombre, equipo.pj, equipo.g, equipo.e, equipo.p, equipo.gf, equipo.gc, equipo.avg, equipo.ptos)
	
def actualizarEquipo(nombre, pj, g, e, p, gf, gc, avg, ptos):
	con = sqlite.connect("ht.sqlite")
	sql = "update equipos set pj = "+str(pj)+", g = "+str(g)+", e = "+str(e)+", p = "+str(p)+", gf = "+str(gf)+", gc = "+str(gc)+", avg = "+str(avg)+", ptos = "+str(ptos)+" where nombre = '"+nombre+"'"
	#print sql
	cur = con.cursor()
	cur.execute(sql)
	con.commit()

def actualizarEquipoTemp(equipo):
	actualizarEquipoTemp(equipo.nombre, equipo.pj, equipo.g, equipo.e, equipo.p, equipo.gf, equipo.gc, equipo.avg, equipo.ptos)
	
def actualizarEquipoTemp(nombre, pj, g, e, p, gf, gc, avg, ptos):
	con = sqlite.connect("ht.sqlite")
	sql = "update equipostemp set pj = "+str(pj)+", g = "+str(g)+", e = "+str(e)+", p = "+str(p)+", gf = "+str(gf)+", gc = "+str(gc)+", avg = "+str(avg)+", ptos = "+str(ptos)+" where nombre = '"+nombre+"'"
	#print sql
	cur = con.cursor()
	cur.execute(sql)
	con.commit()

def getEquipoTemp(nombre):
	con = sqlite.connect("ht.sqlite")
	sql = "SELECT * FROM equipostemp WHERE nombre = '"+nombre+"'"
	#print sql
	cur = con.cursor()
	cur.execute(sql)
	con.commit()


#Betis 2-1 Madrid
actualizarEquipo('Betis', 5, 5, 0, 0, 12, 1, 11, 15)
actualizarEquipo('Madrid', 5, 3, 0, 2, 4, 6, -2, 9)
#Belchite 5-0 Periana
#(2, u'Periana', 4, 2, 1, 1, 12, 7, 5, 7, u'A')
#(8, u'Belchite', 4, 1, 1, 2, 2, 6, -4, 4, u'A')
actualizarEquipo('Periana', 5, 2, 1, 2, 12, 12, 0, 7)
actualizarEquipo('Belchite', 5, 2, 1, 2, 7, 6, 1, 7)
#Guadalajara 3-3 Antequera
# (3, u'Guadalajara', 4, 2, 0, 2, 7, 3, 4, 6, u'A')
# (5, u'Antequera', 4, 2, 0, 2, 5, 7, -2, 6, u'A')
actualizarEquipo('Guadalajara', 5, 2, 1, 2, 10, 6, 4, 7)
actualizarEquipo('Antequera', 5, 2, 1, 2, 8, 10, -2, 7)
#galapagar 3 - 5 Santafe
# (6, u'Galapagar', 4, 1, 0, 3, 3, 9, -6, 3, u'A')
# (7, u'Santafe', 4, 0, 0, 4, 1, 7, -6, 0, u'A')
actualizarEquipo('Galapagar', 5, 1, 0, 4, 6, 14, -8, 3)
actualizarEquipo('Santafe', 5, 1, 0, 4, 6, 10, -4, 3)
printAll()