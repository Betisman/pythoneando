# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
httplib2.debuglevel = 1
http = httplib2.Http()

#variables globales
headers = {'Content-type': 'application/x-www-form-urlencoded'}
loginurl = 'http://193.146.228.10/webmail/src/redirect.php'
username = 'jc.jimenez'
password = '360846'
cookie = ''


def login():
	try:
	
	#pre
		url = 'http://193.146.228.10/alumnos.php'
		response, content = http.request(url, 'POST', headers=headers)
		try:
			cookie = response['set-cookie']
			headers['Cookie'] = cookie
		except KeyError:
			print 'Saltó excepción KeyError'
	#pre
		url = loginurl
		#body = {'page':'identification','ident':'1','login':username,'password':password}
		#body = {'js_autodetect_results':'1','just_logged_in':'1','domceu1':'usp.ceu.es','login_username':username,'secretkey':password}
		#body = {'login_username':username,'secretkey':password}
		#js_autodetect_results=1&just_logged_in=1&domceu1=%40usp.ceu.es&login_username=jc.jimenez&secretkey=360846
		url = loginurl + '?' + 'js_autodetect_results=1&just_logged_in=1&domceu1=%40usp.ceu.es&login_username='+username+'&secretkey='+password
		#response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		response, content = http.request(url, 'POST', headers=headers)
		try:
			cookie = response['set-cookie']
			headers['Cookie'] = cookie
		except KeyError:
			print 'Saltó excepción KeyError'
			return None
		afichero(content)
		return 'Login OK'
	except Exception:
		print 'ERROR'

def comprobarCorreo():
	try:
		url = 'http://193.146.228.10/webmail/src/left_main.php'
		response, content = http.request(url, 'POST', headers=headers)
		try:
			cookie = response['set-cookie']
			headers['Cookie'] = cookie
		except KeyError:
			print 'Saltó excepción KeyError'
			return None
		afichero(content)
		return 'Login OK'
	except Exception:
		print 'ERROR'

def afichero(content):
	print 'fichereando...'
	f = open('temp.txt', 'w')
	f.write(content)
	f.close()
	return 'fichereado'

print login()
#print comprobarCorreo()