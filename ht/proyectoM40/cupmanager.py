# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
import time, datetime
import BeautifulSoup
#httplib2.debuglevel = 1
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


print login()
html = getHtmlGrupos('84703')
html = prettyfyHtml(html)
tables = html.findAll('table', border="0", width="410px", align="center", cellpadding="1", cellspacing="1")
indices = indicesGrupos(tables)

for i in indices:
	grupo = getGrupoFromHtml(grupoHtml(i, tables))
	print grupo
	

