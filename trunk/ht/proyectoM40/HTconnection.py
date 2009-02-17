#!/usr/bin/env python
# coding=UTF-8
import xml.dom.minidom as minidom
import urllib, httplib2, sys

class HtConnManager:	
	def __init__(self):
		#creamos una conexión HTTP
		self.http = httplib2.Http()
		self.recServer = None
		try:
			self.recServer = self.getRecommendedServer()
		except Exception, msg:
			print "Excepción al conectar:", msg
		self.cookie = None
		self.headers = None
	
	def getRecommendedServer(self):
		"""
		Método que obtiene el servidor recomendado por Ht para realizar las conexiones.
		"""
		try:
			#urle que Hattrick dice que es la que nos dice qué servidor usar
			url = 'http://www.hattrick.org/common/chppxml.axd?file=servers'
			#realizamos la petición http a la url anterior
			response, content = self.http.request(url, 'GET')
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
	
	def login(self, username, password):
		"""
		Realiza el login a ht.
		El problema es que lo hacemos con el password, cuando deberíamos hacerlo con el securitycode.
		"""
		
		#obtenemos el servidor recomendado al cual conectarnos.
		#recServer = getRecommendedServer()
		try:
			#aquí se indica el nombre y versión de la app #esto se debe actualizar cuando se consiga el CHPP
			#userAgent = "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4"
			#inicializamos la variable que guardará la cookie para mantener la sesión
			self.cookie = ''
			
			#inicializamos la cabecera de la petición http
			#self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
			self.headers = {}
			
			#url a la que conectarse para realizar el login
			url = self.recServer + '/common/chppxml.axd?file=login&readonlypassword=elpiso&loginname=alecasona&actionType=login&chppID=3501&chppKey=BE421657-81E6-4AEE-8BF5-CB2E36BB3D6A'
			
			#construimos el boy de la petición http (para saber qué valores enviar, hemos usado el LiveHttpHeaders de Firefox)
			body = {'actionType':'login','loginname':username, 'readonlypassword':'elpiso', 'chppID':'3501', 'chppKey':'BE421657-81E6-4AEE-8BF5-CB2E36BB3D6A'}
			
			#realizamos la conexión y recibimos el contenido de la respuesta y el response
			#response, content = self.http.request(url, 'GET', headers=self.headers, body = urllib.urlencode(body))
			response, content = self.http.request(url, 'GET', headers=self.headers)
			try:
				#capturamos la cookie devuelta para mantener la sesión
				self.cookie = response['set-cookie']
				self.headers['Cookie'] = self.cookie
			except KeyError:
				print 'Saltó excepción KeyError', sys.exc_info()
				#return None
			doc = minidom.parseString(content)
			isAuth = doc.getElementsByTagName('IsAuthenticated')[0].firstChild.nodeValue
			loginResult = doc.getElementsByTagName('LoginResult')[0].firstChild.nodeValue
			userID = doc.getElementsByTagName('UserID')[0].firstChild.nodeValue

			response, content = self.http.request(url, 'GET', headers=self.headers)
			try:
				print 'ppio try'
				#capturamos la cookie devuelta para mantener la sesión
				self.cookie = response['set-cookie']
				self.headers['Cookie'] = self.cookie
			except KeyError:
				print 'Saltó excepción KeyError', sys.exc_info()
				#return None
			print 'se fue el try'
			
			doc = minidom.parseString(content)
			isAuth = doc.getElementsByTagName('IsAuthenticated')[0].firstChild.nodeValue
			loginResult = doc.getElementsByTagName('LoginResult')[0].firstChild.nodeValue
			userID = doc.getElementsByTagName('UserID')[0].firstChild.nodeValue

			return self.http, self.headers
		except Exception, msg:
			# print 'Saltó una excepción en login().'
			# print 'Info:', sys.exc_info()
			print msg
			raise HtConnectionException(Exception, 'Excepción en login')
	
	def getFicheroXmlHt(self, ruta, body):
		response, content = self.http.request(ruta, headers=self.headers, body)
		print 'ruta', ruta, '\nheaders', '\nbody', body
		return content

class HtConnectionException(Exception):
	def __init__(self, exception, message):
		#HtConnectionException = Exception(exception)
		pass