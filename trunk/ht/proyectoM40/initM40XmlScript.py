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

config = Config.Config()
#conectamos con Hattrick y nos logueamos
htconn = HTconnection.HtConnManager()
http, headers = htconn.login(config.get('hattrick.username'), config.get('hattrick.password'))
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
	# if(equipo.getElementsByTagName('liga')[0].getAttribute('id') == ''):
		# equipo.getElementsByTagName('liga')[0].getAttributeNode('id').nodeValue = leagueid
	equipo.getElementsByTagName('liga')[0].getAttributeNode('id').nodeValue = leagueid

afichero(doc.toxml(encoding="utf-8"), fileM40)
	
	