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
	
	def login2(self, username, password):
		from mechanize import Browser
		import mechanize as mech
		import logging, sys
		logger = logging.getLogger("mechanize")
		logger.addHandler(logging.StreamHandler(sys.stdout))
		logger.setLevel(logging.INFO)

		br = Browser()
		#response = br.submit()
		br.open(self.recServer)
		br.open(self.recServer)
		br.select_form(name="aspnetForm")
		print br.form
		#import pdb;pdb.set_trace()
		# br.form.controls[0].readonly = False
		# br["ctl00_sm_HiddenField"] = "%3B%3BSystem.Web.Extensions%2C+Version%3D3.5.0.0%2C+Culture%3Dneutral%2C+PublicKeyToken%3D31bf3856ad364e35%3Aes-ES%3A3bbfe379-348b-450d-86a7-bb22e53c1978%3A52817a7d%3A67c678a8"
		print br["ctl00_sm_HiddenField"]
		br["ctl00$ucSubMenu$txtUserName"] = username
		br["ctl00$ucSubMenu$txtPassword"] = password
		br["ctl00$CPSidebar$AllLanguages$ddlLanguages"] = ["6"]
		print br.form
		#ctl00_ucSubMenu_butLogin
		response = br.submit()
		print response.read()
		print response.info()
		
		response2 = mech.urlopen(response.info()['location'])
		print response2.read()
		print response2.info()
	
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
			#	url = recServer + '/common/default.asp'
			print 'url', self.recServer
			url = self.recServer + '/common/chppxml.axd?file=login&readonlypassword=elpiso&loginname=alecasona&actionType=login&chppID=3501&chppKey=BE421657-81E6-4AEE-8BF5-CB2E36BB3D6A'
			#print url
			#construimos el boy de la petición http (para saber qué valores enviar, hemos usado el LiveHttpHeaders de Firefox)
			body = {'actionType':'login','loginname':username, 'readonlypassword':'elpiso', 'chppID':'3501', 'chppKey':'BE421657-81E6-4AEE-8BF5-CB2E36BB3D6A'}
			#realizamos la conexión y recibimos el contenido de la respuesta y el response
			#response, content = self.http.request(url, 'GET', headers=self.headers, body = urllib.urlencode(body))
			response, content = self.http.request(url, 'GET', headers=self.headers)
			#print "requesting url:", url, urllib.urlencode(body)
			print "requesting url:", url
			#-----------------------------------temporal para pruebas nuevo login
			f = open('temp.txt', 'w')
			f.write('%s %s&%s\n' %("requesting url:", url, urllib.urlencode(body)))
			#f = codecs.open(fichero, encoding='utf-8', mode='w')
			f.write(content +'\n' + '*******************\n' + str(response) + '\n========================='*2)
			f.close()
			#------------------------------------------------------------------------
			print 'llega el try'
			try:
				print 'ppio try'
				#capturamos la cookie devuelta para mantener la sesión
				self.cookie = response['set-cookie']
				print self.cookie
				print 'dentro try'
				self.headers['Cookie'] = self.cookie
				print 'final try'
			except KeyError:
				print 'Saltó excepción KeyError', sys.exc_info()
				#return None
			print 'se fue el try'
			
			doc = minidom.parseString(content)
			isAuth = doc.getElementsByTagName('IsAuthenticated')[0].firstChild.nodeValue
			loginResult = doc.getElementsByTagName('LoginResult')[0].firstChild.nodeValue
			userID = doc.getElementsByTagName('UserID')[0].firstChild.nodeValue
			print '%s->%s->%s' %(isAuth, loginResult, userID)
			
			response, content = self.http.request(url, 'GET', headers=self.headers)
			#print "requesting url:", url, urllib.urlencode(body)
			print "requesting url:", url
			#-----------------------------------temporal para pruebas nuevo login
			f = open('temp.txt', 'w')
			f.write('%s %s&%s\n' %("requesting url:", url, urllib.urlencode(body)))
			#f = codecs.open(fichero, encoding='utf-8', mode='w')
			f.write(content +'\n' + '*******************\n' + str(response) + '\n========================='*2)
			f.close()
			#------------------------------------------------------------------------
			print 'llega el try'
			try:
				print 'ppio try'
				#capturamos la cookie devuelta para mantener la sesión
				self.cookie = response['set-cookie']
				print self.cookie
				print 'dentro try'
				self.headers['Cookie'] = self.cookie
				print 'final try'
			except KeyError:
				print 'Saltó excepción KeyError', sys.exc_info()
				#return None
			print 'se fue el try'
			
			doc = minidom.parseString(content)
			isAuth = doc.getElementsByTagName('IsAuthenticated')[0].firstChild.nodeValue
			loginResult = doc.getElementsByTagName('LoginResult')[0].firstChild.nodeValue
			userID = doc.getElementsByTagName('UserID')[0].firstChild.nodeValue
			print '%s->%s->%s' %(isAuth, loginResult, userID)
			
			return self.http, self.headers
		except Exception, msg:
			# print 'Saltó una excepción en login().'
			# print 'Info:', sys.exc_info()
			print msg
			raise HtConnectionException(Exception, 'Excepción en login')

	
	def login3(self, username, password):
		"""
		Realiza el login a ht.
		El problema es que lo hacemos con el password, cuando deberíamos hacerlo con el securitycode.
		"""
		
		#obtenemos el servidor recomendado al cual conectarnos.
		#recServer = getRecommendedServer()
		try:
			#aquí se indica el nombre y versión de la app #esto se debe actualizar cuando se consiga el CHPP
			userAgent = "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4"
			#inicializamos la variable que guardará la cookie para mantener la sesión
			self.cookie = ''
			#inicializamos la cabecera de la petición http
			self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
			#url a la que conectarse para realizar el login
			#	url = recServer + '/common/default.asp'
			print 'url', self.recServer
			url = self.recServer + '/default.aspx'
			#print url
			#construimos el boy de la petición http (para saber qué valores enviar, hemos usado el LiveHttpHeaders de Firefox)
			body = {'ctl00_ucSubMenu_txtUserName':username,'ctl00_ucSubMenu_txtPassword':password, 'ctl00_ucSubMenu_butLogin':'Entrar', 'ctl00_CPSidebar_AllLanguages%24ddlLanguages':'6'}
			#realizamos la conexión y recibimos el contenido de la respuesta y el response
			response, content = self.http.request(url, 'POST', headers=self.headers, body = urllib.urlencode(body))
			print "requesting url:", url
			#con el nuevo diseño, para entrar vamos a coger unas variables ocultas en la interfaz que hemos de agregar al body
			#parametro ctl00_sm_HiddenField
			paramSmHF = '%3B%3BSystem.Web.Extensions%2C+Version%3D3.5.0.0%2C+Culture%3Dneutral%2C+PublicKeyToken%3D31bf3856ad364e35%3Aes-ES%3A3bbfe379-348b-450d-86a7-bb22e53c1978%3A52817a7d%3A67c678a8'
			#parametro __LASTFOCUS
			paramLastFocus = ''
			#parametro __EVENTTARGET
			paramEventTarget = ''
			#parametro __EVENTARGUMENT
			paramEventArgument = ''
			#parametro __VIEWSTATE
			ini = content.find('id="__VIEWSTATE"')
			ini = content.find('value="', ini) + len('value="')
			fin = content.find('"', ini)
			paramViewstate = content[ini:fin]
			#parametro __EVENTVALIDATION
			ini = content.find('id="__EVENTVALIDATION"')
			ini = content.find('value="', ini) + len('value="')
			fin = content.find('"', ini)
			paramEventvalidation = content[ini:fin]
			#-----------------------------------temporal para pruebas nuevo login
			f = open('temp.txt', 'w')
			#f = codecs.open(fichero, encoding='utf-8', mode='w')
			f.write(content +'\n' + '*******************' + str(response))
			f.close()
			#------------------------------------------------------------------------
			
			#repetimos el login incluyendo los parametros sacados de la pagina de Hattrick
			#construimos el boy de la petición http (para saber qué valores enviar, hemos usado el LiveHttpHeaders de Firefox)
			body = {'ctl00_sm_HiddenField':paramSmHF, '__EVENTVALIDATION':paramEventvalidation, '__VIEWSTATE':paramViewstate, '__LASTFOCUS':paramLastFocus, '__EVENTTARGET':paramEventTarget, '__EVENTARGUMENT':paramEventTarget, 'ctl00$ucSubMenu$txtUserName':username,'ctl00$ucSubMenu$txtPassword':password, 'ctl00$ucSubMenu$butLogin':'Login', 'ctl00$CPSidebar$AllLanguages_ddlLanguages':'6'}
			#realizamos la conexión y recibimos el contenido de la respuesta y el response
			response, content = self.http.request(url, 'POST', headers=self.headers, body = urllib.urlencode(body))
			print "requesting url:", url
			#-----------------------------------temporal para pruebas nuevo login
			f = open('temp.txt', 'a')
			#f = codecs.open(fichero, encoding='utf-8', mode='w')
			f.write(content +'\n' + '*******************' + str(response))
			f.close()
			#------------------------------------------------------------------------
			try:
				#capturamos la cookie devuelta para mantener la sesión
				self.cookie = response['set-cookie']
				self.headers['Cookie'] = self.cookie
			except KeyError:
				print 'Saltó excepción KeyError', sys.exc_info()
				return None
			#realizamos la conexión y recibimos el contenido de la respuesta y el response
			loc = response["location"]
			#response, content = self.http.request(loc, 'POST', headers=self.headers, body = urllib.urlencode(body))
			response, content = self.http.request(loc, 'GET', headers=self.headers)
			print "requesting url:", loc
			try:
				#capturamos la cookie devuelta para mantener la sesión
				self.cookie = response['set-cookie']
				self.headers['Cookie'] = self.cookie
			except KeyError:
				print 'Saltó excepción KeyError', sys.exc_info()
				return None	
			print 'Login OK'
			#devolvemos tanto la conexión http como la cabecera de la petición.
			#-----------------------------------temporal para pruebas nuevo login
			f = open('temp.txt', 'a')
			#f = codecs.open(fichero, encoding='utf-8', mode='w')
			f.write(content +'\n' + '*******************' + str(response))
			f.close()
			#------------------------------------------------------------------------
			return self.http, self.headers
		except Exception, msg:
			# print 'Saltó una excepción en login().'
			# print 'Info:', sys.exc_info()
			print msg
			raise HtConnectionException(Exception, 'Excepción en login')

class HtConnectionException(Exception):
	def __init__(self, exception, message):
		#HtConnectionException = Exception(exception)
		pass