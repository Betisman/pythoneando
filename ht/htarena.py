# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
httplib2.debuglevel = 1
http = httplib2.Http()

headers = {'Content-type': 'application/x-www-form-urlencoded'}
def login(http, username, password):
	try:
		cookie = ''
		url = 'http://www.ht-arena.com/?page=identification'
		print url
		#ident=1&login=betisman&password=logaritmo
		body = {'login':username,'password':password,'ident':'1'}
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		#if content.find('http://www.ht-arena.com/realbetismanbalompie/') > 0:
		if content.find('betisman') > 0:
			print 'Se encontro el link, login ok'
		else:
			print 'PUES NO!! NO SE ENCUENTRA EL LINK'
			print content
		try:
			cookie = response['set-cookie']
			headers['Cookie'] = cookie
		except KeyError:
			print 'Saltó excepción KeyError'
			return None
		return http
	except Exception, msg:
		print 'Saltó una excepción en login()', msg
		return None

login(http, 'betisman', 'logaritmo')