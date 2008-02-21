import xml.dom.minidom as minidom
import urllib, httplib2

class HtConnManager:
	http = None
	recServer = None
	cookie = None
	headers = None
	
	def __init__(self):
		#creamos una conexi�n HTTP
		http = httplib2.Http()
	
	def getRecommendedServer(self):
		"""
		M�todo que obtiene el servidor recomendado por Ht para realizar las conexiones.
		"""
		try:
			#urle que Hattrick dice que es la que nos dice qu� servidor usar
			url = 'http://www.hattrick.org/Common/menu.asp?outputType=XML'
			#realizamos la petici�n http a la url anterior
			response, content = http.request(url, 'GET')
			#el content que nos devuelve la respuesta es un xml. Lo parseamos y buscamos la informaci�n que indica qu� servidor es el que nos recomienda ht usar.
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
		El problema es que lo hacemos con el password, cuando deber�amos hacerlo con el securitycode.
		"""
		
		#obtenemos el servidor recomendado al cual conectarnos.
		recServer = getRecommendedServer()
		try:
			#aqu� se indica el nombre y versi�n de la app #esto se debe actualizar cuando se consiga el CHPP
			userAgent = 'MyApp/v1.0'
			#inicializamos la variable que guardar� la cookie para mantener la sesi�n
			cookie = ''
			#inicializamos la cabecera de la petici�n http
			headers = {'Content-type': 'application/x-www-form-urlencoded'}
			#url a la que conectarse para realizar el login
			url = recServer + '/common/default.asp'
			#print url
			#construimos el boy de la petici�n http (para saber qu� valores enviar, hemos usado el LiveHttpHeaders de Firefox)
			body = {'loginname':username,'password':password,'actionType':'login','flashVersion':'0','submit.x':'0','submit.y':'0','submit':'Entrar'}
			#realizamos la conexi�n y recibimos el contenido de la respuesta y el response
			response, content = http.request(url, 'POST', headers=headers, body = urllib.urlencode(body))
			try:
				#capturamos la cookie devuelta para mantener la sesi�n
				cookie = response['set-cookie']
				headers['Cookie'] = cookie
			except KeyError:
				print 'Salt� excepci�n KeyError', sys.exc_info()
				return None
			print 'Login OK'
			#devolvemos tanto la conexi�n http como la cabecera de la petici�n.
			return http, headers
		except Exception:
			# print 'Salt� una excepci�n en login().'
			# print 'Info:', sys.exc_info()
			raise HtConnectionException(Exception, 'Excepci�n en login')
			

class HtConnectionException(Exception):
	def __init__(self, exception, message):
		#HtConnectionException = Exception(exception)