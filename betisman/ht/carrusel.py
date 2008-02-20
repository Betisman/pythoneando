# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
#httplib2.debuglevel = 1
http = httplib2.Http()

#variables globales
recServer = ''
headers = {'Content-type': 'application/x-www-form-urlencoded'}
username = 'betisman'
password = 'logaritmo'
#hasta aquí, variables globales

def getRecommendedServer():
	try:
		url = 'http://www.hattrick.org/Common/menu.asp?outputType=XML'
		#body = {'u_name':username,'p_word':password}
		#response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		response, content = http.request(url, 'GET')
		
		dom = minidom.parseString(content)
		itemlist = dom.getElementsByTagName('RecommendedURL')
		recommendedServer = itemlist[0].firstChild.nodeValue
		print 'Servidor recomendado:', recommendedServer
		return recommendedServer
		#recServer = recommendedServer
		#return 1
	except Exception:
		print 'Salto una excepcion'
		return None

def login():
	try:
		userAgent = 'MyApp/v1.0'
		cookie = ''
		url = recServer + '/common/default.asp'
		print url
		body = {'loginname':username,'password':password,'actionType':'login','flashVersion':'0','submit.x':'0','submit.y':'0','submit':'Entrar'}
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
	
def getHtFileString(file, body):
	#body = {'outputType':'XML','actionType':'view'}
	url = recServer + '/common/' + file
	try:
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		return content
	except Exception, message:
		print 'Saltó execpción en getHtFileString(' + file + ') : ' #+ sys.exc_info()[]
		return None

def setRecServer():
	recServer = getRecommendedServer()

def valorElementoSimple(elem, tag):
	return elem.getElementsByTagName(tag)[0].firstChild.nodeValue
	# equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
	
def setValorElementoSimple(elem, tag, valor):
	elem.getElementsByTagName(tag)[0].firstChild.nodeValue = valor
	
def afichero(content, fichero):
	f = open(fichero, 'w')
	f.write(content)
	f.close()
	return 'Generado fichero ' + fichero

def Main():
	recServer = getRecommendedServer()
	#setRecServer()
	login()
	# body = {'outputType':'XML','actionType':'view','TeamID':'487829'}
	# equipostr = getHtFileString('TeamDetails.asp', body = body)

	doc = minidom.parse('m40.xml')
	equipos = doc.getElementsByTagName('equipo')
	for equipo in equipos:
		#cogemos el teamid de cada uno de los equipos
		teamid = equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
		print equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
		#cogemos el xml de cada equipo desde hattrick
		body = body = {'outputType':'XML','actionType':'view','TeamID':teamid}
		equipostr = getHtFileString('TeamDetails.asp', body = body)
		htdoc = minidom.parseString(equipostr)
		
		id = valorElementoSimple(htdoc, 'TeamID')
		nombre = valorElementoSimple(htdoc, 'TeamName')
		nombrecorto = valorElementoSimple(htdoc, 'ShortTeamName')
		arenaid = valorElementoSimple(htdoc, 'ArenaID')
		arenaname = valorElementoSimple(htdoc, 'ArenaName')
		leagueid = valorElementoSimple(htdoc, 'LeagueLevelUnitID')
		leaguename = valorElementoSimple(htdoc, 'LeagueLevelUnitName')
		
		print 'nombre: ' + nombre
		print 'nombrecorto: ' + nombrecorto
		print 'arenaid:' + arenaid
		print 'arenaname: ' + arenaname
		print 'leaguid: ' + leagueid
		print 'leaguename: ' + leaguename
		
		# if hayQueSetearValor(equipo, 'nombre', nombre):
			# setValorElementoSimple(equipo, 'nombre', nombre)
		# if hayQueSetearValor(equipo, 'nombrecorto', nombrecorto):
			# setValorElementoSimple(equipo, 'nombrecorto', nombrecorto)
		
		if (valorElementoSimple(equipo, 'nombre') != nombre):
			setValorElementoSimple(equipo, 'nombre', nombre)
		if (valorElementoSimple(equipo, 'nombrecorto') != nombrecorto):
			setValorElementoSimple(equipo, 'nombrecorto', nombrecorto)
		if (valorElementoSimple(equipo, 'estadioid') != arenaid):
			setValorElementoSimple(equipo, 'estadioid', arenaid)
		if (valorElementoSimple(equipo, 'estadionombre') != arenaname):
			setValorElementoSimple(equipo, 'estadionombre', arenaname)
		if (valorElementoSimple(equipo, 'ligaid') != leagueid):
			setValorElementoSimple(equipo, 'ligaid', leagueid)
		if (valorElementoSimple(equipo, 'liganombre') != leaguename):
			setValorElementoSimple(equipo, 'liganombre', leaguename)
		
		if(equipo.getAttribute('id') == ''):
			equipo.getAttributeNode('id').nodeValue = teamid
			print '-----------------------' + teamid
		if(equipo.getElementsByTagName('estadio')[0].getAttribute('id') == ''):
			equipo.getElementsByTagName('estadio')[0].getAttributeNode('id').nodeValue = arenaid
		if(equipo.getElementsByTagName('liga')[0].getAttribute('id') == ''):
			equipo.getElementsByTagName('liga')[0].getAttributeNode('id').nodeValue = leagueid

	afichero(doc.toxml(encoding="utf-8"), 'm40.xml')
	
	
	

recServer = getRecommendedServer()
login()
# url = recServer + '/Common/chppxml.axd?file=matchDetails&matchid=158480060'
# try:
	# response, content = http.request(url, 'GET', headers=headers)
	# afichero(content, 'md.xml')
# except Exception, message:
	# print 'joer'
url = recServer + '/Common/chppxml.axd?file=live&matchid=158480060'
try:
	response, content = http.request(url, 'GET', headers=headers)
	afichero(content, 'live.xml')
except Exception, message:
	print 'joer'
	