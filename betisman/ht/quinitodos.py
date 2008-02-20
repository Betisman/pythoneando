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
		#recServer = recommendedServer
		#return 1
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
		print 'Saltó una excepción en login().'
		print 'Info: '
		print sys.exc_info()
		return None
	
def getHtFileString(file, body):
	body = {'outputType':'XML','actionType':'view'}
	url = recServer + '/common/' + file
	try:
		response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
		return content
	except Exception, message:
		print 'Saltó execpción en getHtFileString(' + file + ') : ' #+ sys.exc_info()[]
		return None

def setRecServer():
	recServer = getRecommendedServer()

m40file = "m40.xml"
diccEquipos = {} #diccionario donde asignamos id y nombre de equipo
doc = minidom.parse(m40file)
equipos = doc.getElementsByTagName('equipo')
for equipo in equipos:
	nombre = equipo.getElementsByTagName('nombre')[0].firstChild.nodeValue
	id = equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
	diccEquipos[id] = nombre

print diccEquipos

#para cada equipo obtener siguiente partido
	
recServer = getRecommendedServer()
##setRecServer()
login()
# body = {'outputType':'XML','actionType':'view','TeamID':'487829'}
# print getHtFileString('TeamDetails.asp', body = body)

# teamId = '491940';
# body = {'outputType':'XML','actionType':'view','teamid':teamId,'file':'matches'}
##matchType
##4:
##5:
##8:
##9:
# url = recServer + '/Common/' + 'chppxml.axd'
# try:
	# response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
	# print content
# except Exception, message:
	# print 'Saltó execpción en getHtFileString(' + file + ') : ' #+ sys.exc_info()[]

url = recServer + '/Common/chppxml.axd?file=matches&teamid=491940'
try:
	response, content = http.request(url, 'GET', headers=headers)
	print content
except Exception, message:
	print 'Saltó execpción en getHtFileString(' + file + ') : ' #+ sys.exc_info()[]


# url = recServer + '/Common/chppxml.axd?file=matchDetails&matchid=157340018'
# try:
	# response, content = http.request(url, 'GET', headers=headers)
	# print content
# except Exception, message:
	##print 'Saltó execpción en getHtFileString(' + file + ') : ' #+ sys.exc_info()[]
	# print 'joer'



