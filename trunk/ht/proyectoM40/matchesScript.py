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

def gestionarMatchId(matchid, matches):
	try:
		matches.index(matchid)
	except ValueError:
		matches.append(matchid)
	return matches

def crearXml(path, matches):
	doc = minidom.Document()
	matchids = doc.createElement("matchids")
	for matchid in matches:
		print "matches", matchid
		elem = doc.createElement("matchid")
		elem.appendChild(doc.createTextNode(str(matchid)))
		matchids.appendChild(elem)
	doc.appendChild(matchids)
	doc.writexml(open(path, "w"), encoding="utf-8")
	print doc.toprettyxml()
	
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
	teams.append(equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue)

for teamid in teams:
	url = recServer + '/Common/chppxml.axd?file=matches&teamid='+teamid
	print teamid
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
			matchtype = match.getElementsByTagName('MatchType')[0].firstChild.nodeValue
			#if matchtype == "4": ##solo liguilla
			if matchtype == "4" or matchtype == "5": #4: reglas normales; 5: reglas de copa
				status = match.getElementsByTagName('Status')[0].firstChild.nodeValue
				if status == "UPCOMING":
					matchid = match.getElementsByTagName('MatchID')[0].firstChild.nodeValue
					print "\tmatchid", matchid, str(len(matches))
					matches = gestionarMatchId(matchid, matches)
					break;
	except Exception, msg:
		print "oh, oh", msg
		traceback.print_exc()
crearXml(pathMatchids, matches)