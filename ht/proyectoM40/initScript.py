# -*- coding: UTF-8 -*-
import codecs

# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
import time, datetime
import tools.BeautifulSoup as BeautifulSoup
from model import Equipo
from handlers import EquipoHandler
from pysqlite2 import dbapi2 as sqlite

#script para inicialización de la bd

# lines = open('misc\\inserts.sql').readlines()
# sqls = []
# for sql in lines:
	# print sql
	# if sql.startswith('--'):
		# print 'no hacemos nada'
		# pass
	# else:
		# sqls.append(unicode(sql, sys.stdout.encoding))
sql = open('misc\\inserts.sql').read()
#sql = unicode(sql, sys.stdout.encoding)
sql = unicode(sql, 'utf-8')
ini = sql.find('DROP')
sql = sql[ini:]
sqls = sql.split(';\n')
print 'length ==', len(sqls)

conn = sqlite.connect('misc\\ht.sqlite')
cur = conn.cursor()
for sql in sqls:
	print sql
	try:
		if (sql == "COMMIT;"):
			conn.commit()
		else:
			cur.execute(sql)
	except sqlite.OperationalError, m:
		print 'Excepcion de pysqlite2 con >', sql, '<'
conn.close()







http = httplib2.Http()

#variables globales
recServer = ''
headers = {'Content-type': 'application/x-www-form-urlencoded'}
username = 'betisman'
password = 'logaritmo'
#hasta aquí, variables globales

def login():
	try:
		cookie = ''
		url = 'http://www.cupmanager.org/files/index.php'
		body = {'szLoginName':username,'szPassword':password,'login.x':'37','login.y':'8','login':'Login'}
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		try:
			cookie = response['set-cookie']
			headers['Cookie'] = cookie
		except KeyError:
			print 'Saltó excepción KeyError'
			return None
		return 'Login OK'
	except Exception:
		print 'Saltó una excepción en login().'
		print 'Info: '
		print sys.exc_info()
		return None

def getHtmlGrupos(cupid):
	try:
		url = 'http://www.cupmanager.org/files/index.php?mainpage=cupdetails&szMenu=main&nCupId='+cupid+'&szAction=groups'
		body = {'szLoginName':username,'szPassword':password,'login.x':'37','login.y':'8','login':'Login'}
		response, content = http.request(url, 'GET', headers=headers)
		return content
	except Exception:
		print 'Saltó una excepción en getHtmlGrupos.'
		print 'Info: ', sys.exc_info()
		return None
	
def afichero(content, fichero):
	f = open(fichero, 'w')
	f.write(content)
	f.close()
	return 'Generado fichero ' + fichero

def prettyfyHtml(html):
	soup = BeautifulSoup.BeautifulSoup(html)
	return soup

def indicesGrupos(tables):
	ret = []
	i = 0
	for t in tables:
	    try:
	            if (str(t.tr.td.font.string)).startswith('Grupo'):
	                    ret.append(i)
	    except AttributeError:
	            pass
	    i = i + 1
	return ret

def grupoHtml(indice, tables):
	return tables[indice]

def getGrupoFromHtml(grupo):
	ret = []
	gr = []
	filas = grupo.findAll('tr')
	for fila in filas:
		f = []
		columnas = fila.findAll('td')
		for c in columnas:
			f.append(c)
		gr.append(f)
	#aqui ya tenemos un grupo, ahora lo "limpiamos"
	#Además, separamos gf-gc en dos campos y aprovechamos y nos cargamos la posicion
	#posicion -> [0]
	#gf-gc -> [6]
	gr.pop(0) #quitamos la 1ª fila (pos, nombre, pj, g, e, p...)
	for fila in gr:
		if len(fila) > 1: #para cuando no se clasifican todos los del grupo y hay una línea de color entre medias de los clasificados y los no clasificados
			k = 0
			fret = []
			#print fila
			for celda in fila:
				if k > 0:
					if k == 1:
						# print celda.a.string
						# celda = celda.a.string
						fret.append(celda.a.string)
					else:
						if k == 6:
							str = celda.string.split() # '2 - 3' ---> ['2', '-', '3']  === 'gf - gc' ---> ['gf', '-', 'gc']
							fret.append(str[0]) #gf
							fret.append(str[2]) #gc
						else:
							# print celda.string
							# celda = celda.string
							fret.append(celda.string)
				k = k+1
			ret.append(fret)
	return ret

def getIdFromXml(nombre):
	"""
	devuelve tanto el teamid como el nombrecorto del equipo
	"""
	doc = minidom.parse('misc\\m40.xml')
	equipos = doc.getElementsByTagName('equipo')
	for equipo in equipos:
		teamname = equipo.getElementsByTagName('nombre')[0].firstChild.nodeValue
		if teamname.startswith(nombre[:15]):
			return equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue, \
			equipo.getElementsByTagName('nombrecorto')[0].firstChild.nodeValue
	
print login()
html = getHtmlGrupos('94992') #idCopa
html = prettyfyHtml(html)
tables = html.findAll('table', border="0", width="410px", align="center", cellpadding="1", cellspacing="1")
indices = indicesGrupos(tables)

grupos = []
for i in indices:
	grupo = getGrupoFromHtml(grupoHtml(i, tables))
	grupos.append(grupo)

conn = sqlite.connect('misc\\ht.sqlite')
cur = conn.cursor()
i = 1
for grupo in grupos:
	for equipo in grupo:
		#equipo [0]:nombre, [1]: pj, [2]: g, [3]: e, [4]: p, [5]: gf, [6]: gc, [7]: ptos
		nombre = equipo[0]
		print nombre
		try:
			id, nombrecorto = getIdFromXml(nombre)
		except TypeError:
			id = "0"
			nombrecorto = "-"
			
		#sql = "SELECT grupo FROM equipos WHERE id = "+id
		#print sql
		#cur.execute(sql)
		# for row in cur:
			# grupo = row[0]
		
		if i == 1:
			gpo = "A"
		elif i == 2:
			gpo = "B"
		eq = Equipo(id, nombre, nombrecorto, equipo[1], equipo[2], equipo[3], equipo[4], equipo[5], equipo[6], int(equipo[5])-int(equipo[6]), equipo[7], str(gpo))
		eqh = EquipoHandler(eq)
		# eqh.actualizarEquipo()
		# eqh.actualizarEquipoTemp()
		eqh.insertarEquipo()
	i +=1

	
#creación de la tabla equipostemp
conn = sqlite.connect('misc\\ht.sqlite')
cur = conn.cursor()
try:
	cur.execute('CREATE TABLE equipostemp AS SELECT * FROM equipos')
except sqlite.OperationalError, m:
	print 'Excepcion de pysqlite2 con >', sql, '<'
conn.close()	



# sql = "select * from equipos"
# cur.execute(sql)
# for i in cur:
	# print i[1]