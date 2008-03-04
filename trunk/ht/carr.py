# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
import time, datetime
#httplib2.debuglevel = 1

def getRecommendedServer(http):
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
		print 'Salto una excepcion en getRecommendedServer()'
		return None

def login(username, password, recServer, http):
	try:
		userAgent = 'MyApp/v1.0'
		cookie = ''
		headers = {'Content-type': 'application/x-www-form-urlencoded'}
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
		print 'Login OK'
		return http, headers
	except Exception:
		print 'Saltó una excepción en login().'
		print 'Info: '
		print sys.exc_info()
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
	f.write(content.encode("utf-8"))
	f.close()
	return 'Generado fichero ' + fichero

def getMatches(path):
	doc = minidom.parse(path)
	matchids = doc.getElementsByTagName('matchid')
	ret = []
	for matchid in matchids:
		ret.append(matchid.firstChild.nodeValue)
	return ret

def carruselear():
	http = httplib2.Http()
	#variables globales
	recServer = ''
	#headers = {'Content-type': 'application/x-www-form-urlencoded'}
	username = 'betisman'
	password = 'logaritmo'
	#hasta aquí, variables globales
	pathXmls = ".\\xmls\\"
	pathMatchids = pathXmls + "matchids.xml"
	now = datetime.datetime.now()
	strResultados = ""
	#strResultados = "RESULTADOS"+ " (" + str(now.hour) + ":" + str(now.minute) + ")\n\n"

	recServer = getRecommendedServer(http)
	http, headers = login(username, password, recServer, http)
	matchids = getMatches(pathMatchids);
	print str(len(matchids)) + ' partidos'
	for matchid in matchids:
		url = recServer + '/Common/chppxml.axd?file=live&actionType=addMatch&matchid=' + matchid
		#print url
		try:
			response, content = http.request(url, 'GET', headers=headers)
			#afichero(content, pathXmls + 'live'+matchid+'.xml')
			
			
			doc = minidom.parseString(content)
			hometeam = doc.getElementsByTagName('HomeTeamName')[0].firstChild.nodeValue
			awayteam = doc.getElementsByTagName('AwayTeamName')[0].firstChild.nodeValue
			homegoals = doc.getElementsByTagName('HomeGoals')[0].firstChild.nodeValue
			awaygoals = doc.getElementsByTagName('AwayGoals')[0].firstChild.nodeValue
			
			
			#calculo del minuto actual
			inicio = doc.getElementsByTagName('MatchDate')[0].firstChild.nodeValue
			inicio = time.mktime(time.strptime(inicio, "%Y-%m-%d %H:%M:%S"))
			inicio = datetime.datetime.fromtimestamp(inicio)
			ahora = datetime.datetime.now()
			if ahora < inicio:
				diferencia = 0
			else:
				diferencia = ahora-inicio
				diferencia, segundos = divmod(diferencia.seconds, 60)
				if (diferencia > 45):
					if (diferencia > 60):
						diferencia = diferencia - 15
						if (diferencia > 90):
							diferencia = 90	
					else:
						diferencia = 45
			minuto = str(diferencia)
			
			strResultados = strResultados + hometeam + " " + homegoals + " - " + awaygoals + " " + awayteam + " (minuto " + minuto + ")\n"
		except Exception, message:
			print 'No se ha podido tratar el partido', matchid, '\n', sys.exc_info()
			print message

	#strResultados = strResultados + '\n\n\nCarrusel automatico v1.1 implementado en carr.py'
	afichero(unicode(strResultados), pathXmls+'carr.txt')