# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
httplib2.debuglevel = 1
http = httplib2.Http()

#variables globales
htArenaUrl = 'http://www.ht-arena.com/'
headers = {'Content-type': 'application/x-www-form-urlencoded'}

username = 'betisman'
password = 'logaritmo'
security = 'odonkor'
nombreWeb = 'realbetismanbalompie'

numJugadoresTransfer = '25'
temporada = '21'
idliga = '96596'
#hasta aquí, variables globales

def afichero(content):
	print 'fichereando...'
	f = open('temp.txt', 'w')
	f.write(content)
	f.close()
	return 'fichereado'

def login():
	try:
		userAgent = 'MyApp/v1.0'
		cookie = ''
		#url = htArenaUrl + '?page=identification'
		url = 'http://www.ht-arena.com/?page=identification'
		response, content = http.request(url, 'POST', headers=headers)
		afichero(content)
		if (content.find('<input name="login" type="text" id="login">') > 0):
			print 'ES LA PÁGINA CORRECTA'
			headers['Referer'] = 'http://www.ht-arena.com/?page=identification'
			try:
				cookie = response['set-cookie']
				headers['Cookie'] = cookie
			except KeyError:
				print 'Saltó excepción KeyError'
				return None
		else:
			print 'NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
		url = htArenaUrl
		#body = {'ident':'1','login':username,'password':password}
		#body = {'page':'identification','ident':'1','login':username,'password':password}
		#response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		url = htArenaUrl + '?page=identification&login='+username+'&password='+password+'&ident=1'
		body = {'page':'identification','login':username,'password':password,'ident':'1'}
		url = htArenaUrl
		response, content = http.request(url, "POST", headers=headers, body=urllib.urlencode(body))
		#response, content = http.request(url, 'POST', headers=headers)
		#print afichero(content)
		if (content.find('Tu sitio esta disponible en la siguiente dirección :') > 0):	
			try:
				cookie = response['set-cookie']
				headers['Cookie'] = cookie
			except KeyError:
				print 'Saltó excepción KeyError'
				return None
			return 'Login OK'
		else:
			return 'Login incorrecto'
	except Exception:
		print 'Saltó una excepción en login()'
		return None

def conexHattrick():
	try:
		url = htArenaUrl + '?page=team'
		body = {'loginname':username,'password':security,'action':'login','security_code':'readonlypassword'}
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		return 'Conexión a Hattrick Correcta'
	except Exception:
		print 'Saltó una excepción en login()'
		return None

def actualizar(pagina):
	try:
		url = htArenaUrl
		if (pagina == 'transfers'):
			body = {'page':pagina,'action':'update','nb_players_to_show':'25'}
		elif (pagina == 'old_season'):
			body = {'page':pagina,'action':'update','season':temporada,'league':idliga}
		else:
			body = {'page':pagina,'action':'update'}
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		if (content.find('Data downloaded') > 0):
			return 'Actualización correcta de ' + pagina
		else:
			return 'ERROR en la actualización de ' + pagina
	except Exception:
		print 'Saltó una excepción en login()'
		return None

def Main():		
	print login()
	# print conexHattrick()
	# print actualizar('team')
	# print actualizar('player')
	# print actualizar('arena')
	# print actualizar('standings')
	# print actualizar('last_match')
	# print actualizar('scorers')
	# print actualizar('transfers')
	# print actualizar('old_season')

Main()
print 'prueba'
#ident=1&login=betisman&password=logaritmo
url = htArenaUrl + '?page=identification&login=betisman&password=logaritmo&ident=1'
print 'url: ' + url
response, content = http.request(url, 'POST', headers=headers)
afichero(content) 