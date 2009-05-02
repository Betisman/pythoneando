# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
import time, datetime
#httplib2.debuglevel = 1

def getRecommendedServer(http):
	"""
	Método que obtiene el servidor recomendado por Ht para realizar las conexiones.
	"""
	try:
		#urle que Hattrick dice que es la que nos dice qué servidor usar
		url = 'http://www.hattrick.org/common/chppxml.axd?file=servers'
		#realizamos la petición http a la url anterior
		response, content = http.request(url, 'GET')
		#el content que nos devuelve la respuesta es un xml. Lo parseamos y buscamos la información que indica qué servidor es el que nos recomienda ht usar.
		dom = minidom.parseString(content)
		itemlist = dom.getElementsByTagName('RecommendedURL')
		recommendedServer = itemlist[0].firstChild.nodeValue
		
		print 'Servidor recomendado:', recommendedServer
		return recommendedServer
	except Exception, msg:
		#print 'Salto una excepcion en getRecommendedServer()', sys_exc_info()
		print 'Salto una excepcion en getRecommendedServer():', msg
		return None

def login(username, password, recServer, http):
	"""
	Realiza el login a ht.
	El problema es que lo hacemos con el password, cuando deberíamos hacerlo con el securitycode.
	"""
	try:
		cookie = ''
		#inicializamos la cabecera de la petición http
		#self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
		headers = {}
		print 'url', recServer
		url = recServer + '/common/chppxml.axd?file=login&readonlypassword=elpiso&loginname=alecasona&actionType=login&chppID=3501&chppKey=BE421657-81E6-4AEE-8BF5-CB2E36BB3D6A'
		#print url
		#construimos el boy de la petición http (para saber qué valores enviar, hemos usado el LiveHttpHeaders de Firefox)
		body = {'actionType':'login','loginname':username, 'readonlypassword':'elpiso', 'chppID':'3501', 'chppKey':'BE421657-81E6-4AEE-8BF5-CB2E36BB3D6A'}
		#realizamos la conexión y recibimos el contenido de la respuesta y el response
		#response, content = self.http.request(url, 'GET', headers=self.headers, body = urllib.urlencode(body))
		response, content = http.request(url, 'GET', headers=headers)
		#print "requesting url:", url, urllib.urlencode(body)
		try:
			#capturamos la cookie devuelta para mantener la sesión
			cookie = response['set-cookie']
			headers['Cookie'] = cookie
		except KeyError:
			print 'Saltó excepción KeyError', sys.exc_info()
			#return None
		print 'se fue el try'
		
		doc = minidom.parseString(content)
		isAuth = doc.getElementsByTagName('IsAuthenticated')[0].firstChild.nodeValue
		loginResult = doc.getElementsByTagName('LoginResult')[0].firstChild.nodeValue
		userID = doc.getElementsByTagName('UserID')[0].firstChild.nodeValue
		
		response, content = http.request(url, 'GET', headers=headers)
		#print "requesting url:", url, urllib.urlencode(body)
		try:
			#capturamos la cookie devuelta para mantener la sesión
			cookie = response['set-cookie']
			headers['Cookie'] = cookie
		except KeyError:
			print 'Saltó excepción KeyError', sys.exc_info()
			#return None
		
		doc = minidom.parseString(content)
		isAuth = doc.getElementsByTagName('IsAuthenticated')[0].firstChild.nodeValue
		loginResult = doc.getElementsByTagName('LoginResult')[0].firstChild.nodeValue
		userID = doc.getElementsByTagName('UserID')[0].firstChild.nodeValue
		
		return http, headers
	except Exception, msg:
		# print 'Saltó una excepción en login().'
		# print 'Info:', sys.exc_info()
		print msg
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

def carruselear():
	http = httplib2.Http()
	#variables globales
	recServer = ''
	#headers = {'Content-type': 'application/x-www-form-urlencoded'}
	username = 'alecasona'
	password = 'casona'
	seccode = 'odonkor'
	#hasta aquí, variables globales
	pathXmls = "./xmls/"
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
			# parche cutre para el 26.07.2008 ###################
			awayteam = awayteam.replace('ThePiso', 'ThP')
			if hometeam.find('Betisman') > -1:
				hometeam = 'RBB'
			if hometeam.find('Plaza') > -1:
				homeyteam = 'Pza'
			if awayteam.find('Shadiers') > -1:
				awayteam = 'Sha'
			if hometeam.find('Servele') > -1:
				hometeam = 'RSC'
			if awayteam.find('jCallado') > -1:
				awayteam = 'jCa'
			# fin parche ##############################
			
			
			#calculo del minuto actual
			inicio = doc.getElementsByTagName('MatchDate')[0].firstChild.nodeValue
			inicio = time.mktime(time.strptime(inicio, "%Y-%m-%d %H:%M:%S"))
			inicio = datetime.datetime.fromtimestamp(inicio)
			ahora = datetime.datetime.now()
			# #########PARCHE CUTRE PARA LOS TIEMPOS CON LA DIFERENCIA DE 8 HORAS DE BLUEHOST
			ahora = datetime.datetime.now() + datetime.timedelta(hours=8)
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
			
			strResultados = strResultados + hometeam + " " + homegoals + " - " + awaygoals + " " + awayteam + " (" + minuto + "'); "
			url = recServer + '/Common/chppxml.axd?file=live&actionType=deleteMatch&matchid=' + matchid
			response, content = http.request(url, 'GET', headers=headers)
		except Exception, message:
			print 'No se ha podido tratar el partido', matchid, '\n', sys.exc_info()
			print message

	print asciizacion(strResultados)
	#strResultados = strResultados + '\n\n\nCarrusel automatico v1.1 implementado en carr.py'
	afichero(unicode(strResultados), pathXmls+'carr.txt')