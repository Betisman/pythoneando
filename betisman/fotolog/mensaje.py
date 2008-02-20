# coding=utf-8
import httplib2, urllib, getpass
#httplib2.debuglevel = 1

strFotologDown = 'Fotolog se encuentra bajo mantenimiento programado'
headers = {'Content-type': 'application/x-www-form-urlencoded'}
http = httplib2.Http()


def isFotologRunning():
	content = urllib.urlopen('http://www.fotolog.com').read()
	if content.find(strFotologDown) != -1:	#si lo encuentra
		return 0 #fotolog caido
	else:
		return 1 #fotolog funcionando

def login(username, password):
	url = 'http://account.fotolog.com/login'
	body = {'u_name':username,'p_word':password}
	response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
	try:
		cookie = response['set-cookie']
		headers['Cookie'] = cookie
	except KeyError:
		return 0
	else:
		return 1

def dejarMensaje(amigo, mensaje):
	url = "http://www.fotolog.com/"+amigo
	response, content = http.request(url, 'GET', headers=headers)
	tvalue = t(content)
	body = {'message':mensaje,'t':tvalue,'ajax':'true'}
	url = "http://www.fotolog.com/gb.post"
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
	if content.find("HTTP Status 500") == -1:
		ok = 1
	else:
		ok = -1
	return ok

def t(content):
	t = content.find('<input type="hidden" name="t" value=')
	value = content.find("value", t)
	com = content.find('"', value)
	com2 = content.find('"', com+1)
	return content[com+1:com2]

#main
if isFotologRunning():
	l = 0
	while l == 0:
		username = raw_input('user: ')
		password = getpass.getpass('password: ')
		l = login(username, password)
		if l == 0:
			print 'Login incorrecto, vuelve a introducir tu username y password de tu cuenta fotolog.'
	amigo = raw_input('amigo: ')
	mensaje = raw_input('mensaje:\n\t')
	ok = dejarMensaje(amigo, mensaje)
	if ok == -1:
		print "ERROR: El mensaje no ha sido enviado."
	else:
		print "El mensaje ha sido enviado correctamente"
else:
	print strFotologDown