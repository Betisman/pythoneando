# coding=ISO-8859-1
import HTconnection
import Config
import xml.dom.minidom as minidom
import sys
import traceback


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
		cadena = cadena + liga + "\t"
		cadena = cadena + partido['matchhomename'] + " " + partido['homegoals']
		cadena = cadena + " - "
		cadena = cadena + partido['awaygoals'] + " " +partido['matchawayname'] +"\n"
		if partido['carita'].endswith(')'):
			res['g'] = res['g'] + 1
		elif partido['carita'].endswith('('):
			res['p'] = res['p'] + 1
		else:
			res['e'] = res['e'] + 1
	cadena = cadena + '\n%d jugados: %d ganados, %d empatados, %d perdidos\n' % (len(matches), res['g'], res['e'], res['p'])
	print cadena
	afichero(cadena, path)

def asciizacion(cadena):
	tildes = {u'á':'a', u'é':'e', u'í':'i', u'ó':'o', u'ú':'u'}
	keys = tildes.keys()
	try:
		for i in tildes:
			abuscar = keys.pop()
			while cadena.find(abuscar) > -1:
				cadena = cadena.replace(abuscar, tildes[abuscar])
	except IndexError:
		pass
	return cadena
	
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