# coding=ISO-8859-1
import sendgmail
import HTconnection
import handlers
import model
import Config
import datetime
import xml.dom.minidom as minidom
import sys
import traceback

class CarruselHandler:
	def __init__(self):
		self.config = Config.Config()
		#conectamos con Hattrick y nos logueamos
		self.htconn = HTconnection.HtConnManager()
		self.http, self.headers = self.htconn.login(self.config.get('hattrick.username'), self.config.get('hattrick.password'))
		self.recServer = self.htconn.recServer
	
	def valorElementoSimple(self, elem, tag):
		return elem.getElementsByTagName(tag)[0].firstChild.nodeValue
		# equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
	
	def setValorElementoSimple(self, elem, tag, valor):
		elem.getElementsByTagName(tag)[0].firstChild.nodeValue = valor
	
	def afichero(self, content, fichero):
		f = open(fichero, 'w')
		f.write(content.encode("utf-8"))
		f.close()
		return 'Generado fichero ' + fichero

	def getMatches(self, path):
		doc = minidom.parse(path)
		matchids = doc.getElementsByTagName('matchid')
		ret = []
		for matchid in matchids:
			ret.append(matchid.firstChild.nodeValue)
		return ret

	def generarFicheroCarrusel(self, fich):
		#headers = {'Content-type': 'application/x-www-form-urlencoded'}
		username = self.config.get('hattrick.username')
		password = self.config.get('hattrick.password')
		securitycode = self.config.get('hattrick.securitycode')
		pathMatchids = self.config.get('file.matches')
		#hasta aquí, variables globales
		
		recServer = self.recServer
		now = datetime.datetime.now()
		strResultados = "RESULTADOS"+ " (" + str(now.hour) + ":" + str(now.minute) + ")\n\n"
		
		strClasif = "CLASIFICACION ACTUAL\n"

		matchids = self.getMatches(pathMatchids);
		print str(len(matchids)) + ' partidos'
		for matchid in matchids:
			url = recServer + '/Common/chppxml.axd?file=live&actionType=addMatch&matchid=' + matchid
			#print url
			try:
				response, content = self.http.request(url, 'GET', headers=self.headers)
				#afichero(content, pathXmls + 'live'+matchid+'.xml')
				
				doc = minidom.parseString(content)
				hometeam = doc.getElementsByTagName('HomeTeamName')[0].firstChild.nodeValue
				awayteam = doc.getElementsByTagName('AwayTeamName')[0].firstChild.nodeValue
				homegoals = doc.getElementsByTagName('HomeGoals')[0].firstChild.nodeValue
				awaygoals = doc.getElementsByTagName('AwayGoals')[0].firstChild.nodeValue
				
				#obtenemos objetos Equipo para el local y el visitante
				dbh = handlers.DBHandler()
				hometeam = dbh.getEquipoIni(hometeam)
				awayteam = dbh.getEquipoIni(awayteam)
				
				#calculo del minuto actual
				inicio = doc.getElementsByTagName('MatchDate')[0].firstChild.nodeValue
				inicio = time.mktime(time.strptime(inicio, "%Y-%m-%d %H:%M:%S"))
				inicio = datetime.datetime.fromtimestamp(inicio)
				ahora = datetime.datetime.now()
				if ahora < inicio:
					diferencia = 0
				else:
					diferencia = ahora-inicio
					diferencia, segundos = divmod(diferencia.seconds, 60)
					if (diferencia > 45):
						if (diferencia > 60):
							diferencia = diferencia - 15
							if (diferencia > 90):
								diferencia = 90	
						else:
							diferencia = 45
				minuto = str(diferencia)
				
				partido = model.Partido(hometeam, homegoals, awaygoals, awayteam, minuto)
				
				strResultados = strResultados + partido.local.nombre + " " + partido.goleslocal + " - " + partido.golesvisitante + " " + partido.visitante.nombre + " (minuto " + partido.minuto + ")\n"
				
				#actualizamos la clasificacion
				ch = handlers.ClasifHandler()
				ch.actualizarClasifPartido(partido)
			except Exception, message:
				traceback.print_exc()
				print 'No se ha podido tratar el partido', matchid, '\n', sys.exc_info()
				print message
		
		ch = handlers.ClasifHandler()
		strClasif = strClasif + "\nGrupo A\n\n"
		strClasif = strClasif + ch.getStrClasifTemp('A')
		strClasif = strClasif + "\n\n"
		strClasif = strClasif + "\nGrupo B\n\n"
		strClasif = strClasif + ch.getStrClasifTemp('B')
		
		strPie = '\n\n\nCarrusel automatico v1.1 implementado en carr.py'
		
		strCarr = strResultados + strClasif + strPie
		
		afichero(unicode(strResultados), fich)