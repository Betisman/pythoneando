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
		cadena = cadena + partido['carita'] + " "
		cadena = cadena + liga + "\t" + "[" + partido['posLiga'] + ".]" + "\t"
		cadena = cadena + partido['matchhomename'] + " " + partido['homegoals']
		cadena = cadena + " - "
		cadena = cadena + partido['awaygoals'] + " " +partido['matchawayname'] + "\n"
		if partido['carita'].endswith(')'):
			res['g'] = res['g'] + 1
		elif partido['carita'].endswith('('):
			res['p'] = res['p'] + 1
		else:
			res['e'] = res['e'] + 1
	cadena = cadena + '\n%d jugados: %d ganados, %d empatados, %d perdidos\n' % (len(matches), res['g'], res['e'], res['p'])
	print asciizacion(cadena)
	afichero(cadena, path)

def asciizacion(cadena):
	#primero limpiamos las tildes
	tildes = {u'�':'a', u'�':'e', u'�':'i', u'�':'o', u'�':'u'}
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
	
def getPosLiga(equipoid, ligaid, headers):
	url = recServer + '/Common/chppxml.axd?file=leagueDetails&leagueLevelUnitID=%s' % (ligaid)
	response, content = http.request(url, 'GET', headers=headers)
	doc = minidom.parseString(content)
	equipos = doc.getElementsByTagName('Team')
	for eq in equipos:
		eqid = eq.getElementsByTagName('TeamID')[0].firstChild.nodeValue
		if eqid == equipoid:
			pos = eq.getElementsByTagName('Position')[0].firstChild.nodeValue
			return pos
	return '-1'
	
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
#hasta aqu�, variables globales

#obtenemos los teamids
doc = minidom.parse(fileM40)
equipos = doc.getElementsByTagName('equipo')
for equipo in equipos:
	team = {}
	team['id'] = equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
	team['name'] = equipo.getElementsByTagName('nombre')[0].firstChild.nodeValue
	team['liga'] = equipo.getElementsByTagName('liganombre')[0].firstChild.nodeValue
	team['ligaID'] = equipo.getElementsByTagName('ligaid')[0].firstChild.nodeValue
	team['posLiga'] = getPosLiga(team['id'], team['ligaID'], headers)
	teams.append(team)

teams = ordenarEquiposPorLiga(teams)

for team in teams:
	partido = {}
	url = recServer + '/Common/chppxml.axd?file=matches&teamid='+team['id']
	try:
		response, content = http.request(url, 'GET', headers=headers)
		#open('misc\\live'+matchid+'.xml', "w").write(content)
		#afichero(content, "misc\\matches"+team['id']+".xml")
		#-----------------------------------temporal para pruebas nuevo login
		if team == teams[0]:
			f = open('temp.txt', 'a')
			#f = codecs.open(fichero, encoding='utf-8', mode='w')
			f.write(content +'\n' + '*******************' + str(response))
			f.close()
		#------------------------------------------------------------------------
		doc = minidom.parseString(content)
		#para cada partido, recuperamos el MatchID de aquel que cumpla:
		#	MatchType = 4
		#	y Status = UPCOMING
		partidos = doc.getElementsByTagName('Match')
		ultPartidoLiga = ''
		for match in partidos:
			#partido = {}
			matchtype = match.getElementsByTagName('MatchType')[0].firstChild.nodeValue
			#if matchtype == "1": ## LIGA
			if matchtype == "1":
				status = match.getElementsByTagName('Status')[0].firstChild.nodeValue
				if status == "FINISHED":
					ultPartidoLiga = match
				else:
					break;
					
		partido['matchid'] = ultPartidoLiga.getElementsByTagName('MatchID')[0].firstChild.nodeValue
		partido['matchhomename'] = asciizacion(ultPartidoLiga.getElementsByTagName('HomeTeamName')[0].firstChild.nodeValue)
		partido['matchawayname'] = asciizacion(ultPartidoLiga.getElementsByTagName('AwayTeamName')[0].firstChild.nodeValue)
		partido['homegoals'] = asciizacion(ultPartidoLiga.getElementsByTagName('HomeGoals')[0].firstChild.nodeValue)
		partido['awaygoals'] = asciizacion(ultPartidoLiga.getElementsByTagName('AwayGoals')[0].firstChild.nodeValue)
		partido['liga'] = team['liga']
		partido['posLiga'] = team['posLiga']
		#carita
		carita = ''
		if int(partido['homegoals']) == int(partido['awaygoals']):
			carita = ':-|'
		elif team['id'] == ultPartidoLiga.getElementsByTagName('HomeTeamID')[0].firstChild.nodeValue:
			if int(partido['homegoals']) > int(partido['awaygoals']):
				carita = ':-)'
			else:
				carita =':-('
		elif team['id'] == ultPartidoLiga.getElementsByTagName('AwayTeamID')[0].firstChild.nodeValue:
			if int(partido['homegoals']) > int(partido['awaygoals']):
				carita = ':-('
			else:
				carita =':-)'
		partido['carita'] = carita
		matches.append(partido)
	except Exception, msg:
		print "oh, oh", msg
		traceback.print_exc()
crearFicheroResultados(results, matches)