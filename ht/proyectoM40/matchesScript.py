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

def gestionarMatchId(partido, matches):
	try:
		matches.index(partido)
	except ValueError:
		matches.append(partido)
	return matches

def crearXml(path, matches):
	doc = minidom.Document()
	matchids = doc.createElement("matchids")
	for partido in matches:
		print "matches", partido['matchid'], partido['matchhomename'], "-",partido['matchawayname']
		elem = doc.createElement("matchid")
		elem.appendChild(doc.createTextNode(str(partido['matchid'])))
		elem.appendChild(doc.createComment(partido['matchhomename'] + " - " + partido['matchawayname']))
		matchids.appendChild(elem)
	doc.appendChild(matchids)
	#doc.writexml(open(path, "w"), encoding="utf-8")
	#doc.writexml(open(path, "w"), encoding="ISO-8859-1")
	afichero(doc.toprettyxml(encoding='utf-8'), path)
	print doc.toprettyxml(encoding='utf-8')

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
pathMatchids = config.get('file.matches')
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
	teams.append(team)

for team in teams:
	url = recServer + '/Common/chppxml.axd?file=matches&teamid='+team['id']
	print '\n', team['name'], '('+team['id']+')'
	try:
		response, content = http.request(url, 'GET', headers=headers)
		#open('misc\\live'+matchid+'.xml', "w").write(content)
		#afichero(content, "misc\\matches"+teamid+".xml")
		
		doc = minidom.parseString(content)
		#para cada partido, recuperamos el MatchID de aquel que cumpla:
		#	MatchType = 4
		#	y Status = UPCOMING
		partidos = doc.getElementsByTagName('Match')
		for match in partidos:
			partido = {}
			matchtype = match.getElementsByTagName('MatchType')[0].firstChild.nodeValue
			#if matchtype == "4": ##solo liguilla
			if matchtype == "4" or matchtype == "5" or matchtype=='9': #4: reglas normales; 5: reglas de copa; 5: internacional
				status = match.getElementsByTagName('Status')[0].firstChild.nodeValue
				if status == "UPCOMING":
					partido['matchid'] = match.getElementsByTagName('MatchID')[0].firstChild.nodeValue
					partido['matchhomename'] = asciizacion(match.getElementsByTagName('HomeTeamName')[0].firstChild.nodeValue)
					partido['matchawayname'] = asciizacion(match.getElementsByTagName('AwayTeamName')[0].firstChild.nodeValue)
					print "\tmatchid", partido['matchid'], str(len(matches)), partido['matchhomename'], "vs.", partido['matchawayname']
					matches = gestionarMatchId(partido, matches)
					nopartido = False
					break;
			else:
				nopartido = True
		if nopartido:
			print "\tNo tiene partido!!"
	except Exception, msg:
		print "oh, oh", msg
		traceback.print_exc()
crearXml(pathMatchids, matches)