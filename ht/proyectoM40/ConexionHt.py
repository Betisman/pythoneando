import xml.dom.minidom as minidom
import urllib, httplib2

class HtConnManager:
	http = None
	recServer = None
	cookie = None
	headers = None
	
	def __init__(self):
		#creamos una conexión HTTP
		http = httplib2.Http()
	
	def getRecommendedServer(self):
		"""
		Método que obtiene el servidor recomendado por Ht para realizar las conexiones.
		"""
		try:
			#urle que Hattrick dice que es la que nos dice qué servidor usar
			url = 'http://www.hattrick.org/Common/menu.asp?outputType=XML'
			#realizamos la petición http a la url anterior
			response, content = http.request(url, 'GET')
			#el content que nos devuelve la respuesta es un xml. Lo parseamos y buscamos la información que indica qué servidor es el que nos recomienda ht usar.
			dom = minidom.parseString(content)
			itemlist = dom.getElementsByTagName('RecommendedURL')
			recommendedServer = itemlist[0].firstChild.nodeValue
			
			print 'Servidor recomendado:', recommendedServer
			return recommendedServer
		except Exception:
			print 'Salto una excepcion en getRecommendedServer()', sys_exc_info()
			return None
	
	def login(self, username, password):
		"""
		Realiza el login a ht.
		El problema es que lo hacemos con el password, cuando deberíamos hacerlo con el securitycode.
		"""
		
		#obtenemos el servidor recomendado al cual conectarnos.
		recServer = getRecommendedServer()
		try:
			#aquí se indica el nombre y versión de la app #esto se debe actualizar cuando se consiga el CHPP
			userAgent = 'MyApp/v1.0'
			#inicializamos la variable que guardará la cookie para mantener la sesión
			cookie = ''
			#inicializamos la cabecera de la petición http
			headers = {'Content-type': 'application/x-www-form-urlencoded'}
			#url a la que conectarse para realizar el login
			url = recServer + '/common/default.asp'
			#print url
			#construimos el boy de la petición http (para saber qué valores enviar, hemos usado el LiveHttpHeaders de Firefox)
			body = {'loginname':username,'password':password,'actionType':'login','flashVersion':'0','submit.x':'0','submit.y':'0','submit':'Entrar'}
			#realizamos la conexión y recibimos el contenido de la respuesta y el response
			response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
			try:
				#capturamos la cookie devuelta para mantener la sesión
				cookie = response['set-cookie']
				headers['Cookie'] = cookie
			except KeyError:
				print 'Saltó excepción KeyError', sys.exc_info()
				return None
			print 'Login OK'
			#devolvemos tanto la conexión http como la cabecera de la petición.
			return http, headers
		except Exception:
			# print 'Saltó una excepción en login().'
			# print 'Info:', sys.exc_info()
			raise HtConnectionException(Exception, 'Excepción en login')
			

class HtConnectionException(Exception):
	def __init__(self, exception, message):
		#HtConnectionException = Exception(exception)