# coding=ISO-8859-1
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
httplib2.debuglevel = 1
http = httplib2.Http()

#variables globales
recServer = ''
headers = {'Content-type': 'application/x-www-form-urlencoded'}
username = 'betisman'
password = 'logaritmo'
#hasta aquí, variables globales

def getRecommendedServer():
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
	except Exception:
		print 'Salto una excepcion'
		return None

def login():
	try:
		userAgent = 'MyApp/v1.0'
		cookie = ''
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
		return 'Login OK'
	except Exception:
		print 'Saltó una excepción en login()'
		return None

def getHtFileString(file):
	body = {'outputType':'XML','actionType':'view'}
	url = recServer + '/common/' + file
	try:
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		return content
	except Exception, message:
		print 'Saltó execpción en getHtFileString(' + file + ') : ' #+ sys.exc_info()[]
		return None

		#trick.org/Common/MatchDetails.aspx?matchID=157935134
def Main():		
	recServer = getRecommendedServer()
	login()
	print getHtFileString('Live.aspx')

Main()

##################
body = {'outputType':'XML','actionType':'view','TeamID':'487829'}
body = {'outputType':'XML','actionType':'view'}
body = {'outputType':'XML','actionType':'view','matchID':'157935134'}


recServer = getRecommendedServer()
print login()
url = recServer + '/Common/MatchDetails.aspx'
body = {'outputType':'XML','matchid':'157935134','actionType':'view'}
#print url + '?' + urllib.urlencode(body)
response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
print content

url = recServer + '/Common/TeamDetails.asp'
body = {'outputType':'XML','actionType':'view','TeamID':'487829'}
#print url + '?' + urllib.urlencode(body)
response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
print content

url = recServer + '/Common/Live.aspx'
body = {'outputType':'XML','actionType':'view'}
#print url + '?' + urllib.urlencode(body)
response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
print content