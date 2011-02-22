# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
import Config
import HTconnection
#httplib2.debuglevel = 1
http = httplib2.Http()
	
def getHtFileString(file, body):
	#body = {'outputType':'XML','actionType':'view'}
	url = recServer + '/common/' + file
	try:
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		return content
	except Exception, message:
		print 'Saltó execpción en getHtFileString(' + file + ') : ' #+ sys.exc_info()[]
		return None

def getTeamHtml(idteam):
	#body = {'outputType':'XML','actionType':'view'}
	url = recServer + '/Common/chppxml.axd?file=teamdetails&teamid='+idteam
	try:
		response, content = http.request(url, 'GET', headers=headers)
		return content
	except Exception, message:
		print 'Saltó execpción en getHtFileString(' + file + ') : ' #+ sys.exc_info()[]
		return None
		
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
	
def asciizacion(cadena):
	#primero limpiamos las tildes
	tildes = {u'á':'a', u'é':'e', u'í':'i', u'ó':'o', u'ú':'u'}
	keys = tildes.keys()
	try:
		for i in tildes:
			abuscar = keys.pop()
			while cadena.find(abuscar) > -1:
				cadena = cadena.replace(abuscar, tildes[abuscar])
	except IndexError:
		pass
	# ahora limpiamos el resto de caracteres no ISO-8859-1
	charsmalos = []
	try:
		cadena.decode('iso-8859-1')
	except UnicodeEncodeError, message:
		for i in cadena:
			try:
				i.decode('iso-8859-1')
			except UnicodeEncodeError, message:
				charsmalos.append(i)
		if len(charsmalos) > 0:
			for c in charsmalos:
				cadena = cadena.replace(c, '?')
	
	# return cadena
	return cadena.encode('utf-8')

config = Config.Config()
#conectamos con Hattrick y nos logueamos
htconn = HTconnection.HtConnManager()
http, headers = htconn.login(config.get('hattrick.username'), config.get('hattrick.password'), config.get('hattrick.securitycode'))
recServer = htconn.recServer
#headers = {'Content-type': 'application/x-www-form-urlencoded'}
username = config.get('hattrick.username')
password = config.get('hattrick.password')
securitycode = config.get('hattrick.securitycode')
pathMatchids = config.get('file.matches')
fileM40 = config.get('file.m40')

doc = minidom.parse(fileM40)
equipos = doc.getElementsByTagName('equipo')
for equipo in equipos:
	#cogemos el teamid de cada uno de los equipos
	teamid = equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
	print equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
	#cogemos el xml de cada equipo desde hattrick
	body = body = {'outputType':'XML','actionType':'view','TeamID':teamid}
	equipostr = getTeamHtml(teamid)
	htdoc = minidom.parseString(equipostr)
	
	id = valorElementoSimple(htdoc, 'TeamID')
	nombre = asciizacion(valorElementoSimple(htdoc, 'TeamName'))
	nombrecorto = asciizacion(valorElementoSimple(htdoc, 'ShortTeamName'))
	arenaid = valorElementoSimple(htdoc, 'ArenaID')
	arenaname = asciizacion(valorElementoSimple(htdoc, 'ArenaName'))
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
	
	if(equipo.getAttribute('id') != teamid):
		equipo.getAttributeNode('id').nodeValue = teamid
		print '-----------------------' + teamid
	if(equipo.getElementsByTagName('estadio')[0].getAttribute('id') != arenaid):
		equipo.getElementsByTagName('estadio')[0].getAttributeNode('id').nodeValue = arenaid
	# if(equipo.getElementsByTagName('liga')[0].getAttribute('id') == ''):
		# equipo.getElementsByTagName('liga')[0].getAttributeNode('id').nodeValue = leagueid
	equipo.getElementsByTagName('liga')[0].getAttributeNode('id').nodeValue = leagueid

afichero(doc.toxml(encoding="utf-8"), fileM40)
	
	