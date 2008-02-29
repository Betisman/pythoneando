#!/usr/bin/env python
# coding=UTF-8
import xml.dom.minidom as minidom
import urllib, httplib2

class HtConnManager:	
	def __init__(self):
		#creamos una conexi�n HTTP
		self.http = httplib2.Http()
		self.recServer = None
		try:
			self.recServer = self.getRecommendedServer()
		except Exception, msg:
			print "Excepci�n al conectar:", msg
		self.cookie = None
		self.headers = None
	
	def getRecommendedServer(self):
		"""
		M�todo que obtiene el servidor recomendado por Ht para realizar las conexiones.
		"""
		try:
			#urle que Hattrick dice que es la que nos dice qu� servidor usar
			url = 'http://www.hattrick.org/Common/menu.asp?outputType=XML'
			#realizamos la petici�n http a la url anterior
			response, content = self.http.request(url, 'GET')
			#el content que nos devuelve la respuesta es un xml. Lo parseamos y buscamos la informaci�n que indica qu� servidor es el que nos recomienda ht usar.
			dom = minidom.parseString(content)
			itemlist = dom.getElementsByTagName('RecommendedURL')
			recommendedServer = itemlist[0].firstChild.nodeValue
			
			print 'Servidor recomendado:', recommendedServer
			return recommendedServer
		except Exception, msg:
			#print 'Salto una excepcion en getRecommendedServer()', sys_exc_info()
			print 'Salto una excepcion en getRecommendedServer():', msg
			return None
	
	def login(self, username, password):
		"""
		Realiza el login a ht.
		El problema es que lo hacemos con el password, cuando deber�amos hacerlo con el securitycode.
		"""
		
		#obtenemos el servidor recomendado al cual conectarnos.
		#recServer = getRecommendedServer()
		try:
			#aqu� se indica el nombre y versi�n de la app #esto se debe actualizar cuando se consiga el CHPP
			userAgent = 'MyApp/v1.0'
			#inicializamos la variable que guardar� la cookie para mantener la sesi�n
			self.cookie = ''
			#inicializamos la cabecera de la petici�n http
			self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
			#url a la que conectarse para realizar el login
			#	url = recServer + '/common/default.asp'
			print 'url', self.recServer
			url = self.recServer + '/common/default.asp'
			#print url
			#construimos el boy de la petici�n http (para saber qu� valores enviar, hemos usado el LiveHttpHeaders de Firefox)
			body = {'loginname':username,'password':password,'actionType':'login','flashVersion':'0','submit.x':'0','submit.y':'0','submit':'Entrar'}
			#realizamos la conexi�n y recibimos el contenido de la respuesta y el response
			response, content = self.http.request(url, 'POST', headers=self.headers, body = urllib.urlencode(body))
			try:
				#capturamos la cookie devuelta para mantener la sesi�n
				self.cookie = response['set-cookie']
				self.headers['Cookie'] = self.cookie
			except KeyError:
				print 'Salt� excepci�n KeyError', sys.exc_info()
				return None
			print 'Login OK'
			#devolvemos tanto la conexi�n http como la cabecera de la petici�n.
			return self.http, self.headers
		except Exception, msg:
			# print 'Salt� una excepci�n en login().'
			# print 'Info:', sys.exc_info()
			print msg
			raise HtConnectionException(Exception, 'Excepci�n en login')

class HtConnectionException(Exception):
	def __init__(self, exception, message):
		#HtConnectionException = Exception(exception)
		pass