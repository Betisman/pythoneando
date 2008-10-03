# coding=ISO-8859-1
import urllib, httplib2, getpass
import sys
import time, datetime
#httplib2.debuglevel = 1
http = httplib2.Http()

#variables globales
recServer = ''
headers = {'Content-type': 'application/x-www-form-urlencoded'}
#hasta aquí, variables globales

def login(username, password):
	try:
		cookie = ''
		url = 'http://www.cupmanager.org/files/index.php'
		body = {'szLoginName':username,'szPassword':password,'login.x':'37','login.y':'8','login':'Login'}
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		if content.find('<span class="error">Error</span>') > 0:
			return 'Error en el Login, seguramente Usuario/password incorrecto(s)', None
		else:
			try:
				cookie = response['set-cookie']
				headers['Cookie'] = cookie
			except KeyError:
				print 'Saltó excepción KeyError'
				return None, None
			return 'Login OK', getUserId(content)
	except Exception:
		print 'Saltó una excepción en login().'
		print 'Info: '
		print sys.exc_info()
		return None, None

def getUserId(html):
	inipos = html.find('nUserId') + len('nUserId=')
	finpos = html.find('"', inipos)
	return html[inipos:finpos]
	
def actualizarCupManager(userid):
	try:
		url = 'http://www.cupmanager.org/files/index.php?mainpage=teamdetails&szMenu=main&nUserId='+userid+'&szAction=update'
		body = {'szLoginName':username,'szPassword':password,'login.x':'37','login.y':'8','login':'Login'}
		response, content = http.request(url, 'GET', headers=headers)
		if content.find('Tus detalles fueron actualizados') > 0:
			return 'Tus detalles fueron actualizados'
		else:
			return 'ERROR'
	except Exception:
		print 'Saltó una excepción en actualizarCupManager.'
		print 'Info: ', sys.exc_info()
		return None

username = raw_input('Usuario de CupManager: ')
password = getpass.getpass('Password de CupManager: ')
msgLogin, userid = login(username, password)
print msgLogin
if userid != None:
	print actualizarCupManager(userid) #idCopa
salir = raw_input('Pulse una tecla para finalizar.')