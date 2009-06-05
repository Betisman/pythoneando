# coding=ISO-8859-1
import HTconnection
import Config
import xml.dom.minidom as minidom
import sys
import traceback
from tools.roman import *


def afichero(content, fichero):
	f = open(fichero, 'w')
	#f = codecs.open(fichero, encoding='utf-8', mode='w')
	f.write(content)
	f.close()
	return 'Generado fichero ' + fichero

def crearFicheroResultados(path, matches):
	cadena = ''
	res = {'g':0, 'e':0, 'p':0}
	for partido in matches:
		liga = "(" + partido['liga'] + ")"
		if len(liga) < 11:
			dif = 11 - len(liga)
			liga = liga + ' '*dif
		cadena = cadena + partido['matchid'] + " "
		cadena = cadena + partido['hora'] + " "
		cadena = cadena + liga + "\t"
		cadena = cadena + partido['matchhomename']
		cadena = cadena + " - "
		cadena = cadena + partido['matchawayname'] + "\n"
	#print asciizacion(cadena)
	print cadena
	#afichero(cadena, path)

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

def ordenarEquiposPorLiga(teams):
	aux = {}
	ret = []
	for team in teams:
		rom, numliga = team['liga'].split('.')
		try:
			aux[fromRoman(rom)].append(team)
		except KeyError:
			nuevo = []
			nuevo.append(team)
			aux[fromRoman(rom)] = nuevo
	#al poner enteros como claves, se autoordena.
	for i in sorted(aux.keys()):
		lig = [{int(t['liga'].split('.')[1]):t} for t in aux[i]]
		for l in sorted(lig):
			ret.append(l[l.keys()[0]])
	return ret
	
config = Config.Config()
#conectamos con Hattrick y nos logueamos
htconn = HTconnection.HtConnManager()
http, headers = htconn.login(config.get('hattrick.username'), config.get('hattrick.password'))
recServer = htconn.recServer
#headers = {'Content-type': 'application/x-www-form-urlencoded'}
username = config.get('hattrick.username')
password = config.get('hattrick.password')
securitycode = config.get('hattrick.securitycode')
#pathMatchids = config.get('file.matches')
results = 'misc/resultados.txt'
fileM40 = config.get('file.m40')

matches = []
teams = []
#hasta aquí, variables globales

#obtenemos los teamids
doc = minidom.parse(fileM40)
equipos = doc.getElementsByTagName('equipo')
for equipo in equipos:
	team = {}
	team['id'] = equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
	team['name'] = equipo.getElementsByTagName('nombre')[0].firstChild.nodeValue
	team['liga'] = equipo.getElementsByTagName('liganombre')[0].firstChild.nodeValue
	teams.append(team)

teams = ordenarEquiposPorLiga(teams)

for team in teams:
	partido = {}
	url = recServer + '/Common/chppxml.axd?file=matches&teamid='+team['id']
	try:
		response, content = http.request(url, 'GET', headers=headers)
		#open('misc\\live'+matchid+'.xml', "w").write(content)
		#afichero(content, "misc\\matches"+teamid+".xml")
		
		doc = minidom.parseString(content)
		#para cada partido, recuperamos el MatchID de aquel que cumpla:
		#	MatchType = 4
		#	y Status = UPCOMING
		partidos = doc.getElementsByTagName('Match')
		ultPartidoLiga = ''
		for match in partidos:
			#partido = {}
			matchtype = match.getElementsByTagName('MatchType')[0].firstChild.nodeValue
			status = match.getElementsByTagName('Status')[0].firstChild.nodeValue
			if status == "UPCOMING":
				#if matchtype == "1": ## LIGA
				if matchtype == "1":
					ultPartidoLiga = match
					break;

		partido['matchid'] = ultPartidoLiga.getElementsByTagName('MatchID')[0].firstChild.nodeValue
		partido['matchhomename'] = asciizacion(ultPartidoLiga.getElementsByTagName('HomeTeamName')[0].firstChild.nodeValue)
		partido['matchawayname'] = asciizacion(ultPartidoLiga.getElementsByTagName('AwayTeamName')[0].firstChild.nodeValue)
		partido['liga'] = team['liga']
		partido['hora'] = (ultPartidoLiga.getElementsByTagName('MatchDate')[0].firstChild.nodeValue).split(' ')[1][:5]
		#carita
		matches.append(partido)
	except Exception, msg:
		print "oh, oh", msg
		traceback.print_exc()
crearFicheroResultados(results, matches)