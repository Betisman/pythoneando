# coding=ISO-8859-1
import sendgmail
import HTconnection
#import handlers
import model
import Config
import datetime
import time
import xml.dom.minidom as minidom
import sys
import traceback
import codecs

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
	
	# def afichero(self, content, fichero):
		# f = open(fichero, 'w')
		# f.write(content.encode("utf-8"))
		# f.close()
		# return 'Generado fichero ' + fichero

	def getMatches(self, path):
		doc = minidom.parse(path)
		matchids = doc.getElementsByTagName('matchid')
		ret = []
		for matchid in matchids:
			ret.append(matchid.firstChild.nodeValue)
		return ret

	def afichero(self, content, fichero):
		#f = open(fichero, 'w')
		f = codecs.open(fichero, encoding='utf-8', mode='w')
		f.write(content)
		f.close()
		return 'Generado fichero ' + fichero
	
	def generarFicheroCarrusel(self, fich):
		#headers = {'Content-type': 'application/x-www-form-urlencoded'}
		username = self.config.get('hattrick.username')
		password = self.config.get('hattrick.password')
		securitycode = self.config.get('hattrick.securitycode')
		pathMatchids = self.config.get('file.matches')
		fichCarrusel = self.config.get('file.carrusel')
		liguilla = self.config.get('cup.liguilla')
		fichMarcadorXml = self.config.get('file.marcadorXml')
		#hasta aquí, variables globales
		
		recServer = self.recServer
		 # #########PARCHE CUTRE PARA LOS TIEMPOS CON LA DIFERENCIA DE 8 HORAS DE BLUEHOST
                #now = datetime.datetime.now() + datetime.timedelta(hours=8)
                # EN INVIERNO (O POR LO MENOS HOY, 28.10.2009) SON 7 HORAS DE DIFERENCIA!!!
                now = datetime.datetime.now() + datetime.timedelta(hours=8)
		# #########
		strResultados = "RESULTADOS"+ " (%02d:%02d)\n\n" %(now.hour, now.minute)
		
		strClasif = ""

		matchids = self.getMatches(pathMatchids)
		print str(len(matchids)) + ' partidos'
		#MOLINORR
		# marcador  = minidom.Document()
		# partidos = marcador.createElement("partidos")
		# ######
		
		#url = recServer + '/Common/chppxml.axd?file=live&actionType=addMatch&matchid=' + matchid
		#url = recServer + '/Common/chppxml.axd?file=live&actionType=viewNew&matchid=' + matchid
		#recuperamos el archivo actual de live
		url = recServer + '/Common/chppxml.axd?file=live'
		print url
		try:
			response, content = self.http.request(url, 'GET', headers=self.headers)
			#open('misc\\live'+matchid+'.xml', "w").write(content)
			open('misc/live.xml', "w").write(content)
			#import pdb;pdb.set_trace()
			
			doc = minidom.parseString(content)
			
			#recuperamos el fichero y sacamos los ids de todos los partidos que se encuentran en el
			matches = doc.getElementsByTagName('Match')
			matchidsborrar = []
			for m in matches:
				id_borrar = m.getElementsByTagName('MatchID')[0].firstChild.nodeValue
				matchidsborrar.append(id_borrar)
				url = recServer + '/Common/chppxml.axd?file=live&actionType=deleteMatch&matchid=' + id_borrar
				response, content = self.http.request(url, 'GET', headers=self.headers)
			
			url = recServer + '/Common/chppxml.axd?file=live'
			response, content = self.http.request(url, 'GET', headers=self.headers)
			open('misc/live.xml', "w").write(content)
			doc = minidom.parseString(content)
			matches = doc.getElementsByTagName('Match')
			print "el fichero live.xml tiene", len(matches), "partidos"
			
			print "Vamos a añadir", len(matchids), "partidos"
			for matchid in matchids:
				print "añadiendo partido", matchid
				url = recServer + '/Common/chppxml.axd?file=live&actionType=addMatch&matchid=' + matchid
				response, content = self.http.request(url, 'GET', headers=self.headers)
				print "añadido partido", matchid
			
			url = recServer + '/Common/chppxml.axd?file=live'
			response, content = self.http.request(url, 'GET', headers=self.headers)
			open('misc/live.xml', "w").write(content)
			
			doc = minidom.parseString(content)
			matches = doc.getElementsByTagName('Match')
			print len(matches), "partidos recuperados de live.xml"
			for m in matches:
				xmlMatchID = m.getElementsByTagName('MatchID')[0].firstChild.nodeValue
				print "procesamos el partido", xmlMatchID
				if xmlMatchID in matchids:
					hometeam = m.getElementsByTagName('HomeTeamName')[0].firstChild.nodeValue
					awayteam = m.getElementsByTagName('AwayTeamName')[0].firstChild.nodeValue
					homegoals = m.getElementsByTagName('HomeGoals')[0].firstChild.nodeValue
					awaygoals = m.getElementsByTagName('AwayGoals')[0].firstChild.nodeValue
					hometeamid = m.getElementsByTagName('HomeTeamID')[0].firstChild.nodeValue
					awayteamid = m.getElementsByTagName('AwayTeamID')[0].firstChild.nodeValue
					
					#MOLINORR
					# cadapartido = marcador.createElement("partido")
					# local = marcador.createElement("equipolocal")
					# local.appendChild(marcador.createTextNode(hometeam))
					# visitante = marcador.createElement("equipovisitante")
					# visitante.appendChild(marcador.createTextNode(awayteam))
					# goleslocal = marcador.createElement("goleslocal")
					# goleslocal.appendChild(marcador.createTextNode(homegoals))
					# golesvisitante = marcador.createElement("golesvisitante")
					# golesvisitante.appendChild(marcador.createTextNode(awaygoals))
					
					# cadapartido.appendChild(local)
					# cadapartido.appendChild(goleslocal)
					# cadapartido.appendChild(visitante)
					# cadapartido.appendChild(golesvisitante)
					
					# partidos.appendChild(cadapartido)
					# ######
					
					
					#obtenemos objetos Equipo para el local y el visitante
					# dbh = handlers.DBHandler()
					partidoliga = True
					# try:
						# hometeam = dbh.getEquipoIni(hometeamid)
					# except Exception:
						# hometeam = model.Equipo(id=hometeamid, nombre=hometeam)
						# partidoliga = False #indica que el partido no se corresponde con la liga (por ejemplo, cuando un equipo juega un amistoso que no le corresponde con el calendario de la liga)
					# try:
						# awayteam = dbh.getEquipoIni(awayteamid)
					# except Exception:
						# awayteam = model.Equipo(id=awayteamid, nombre=awayteam)
						# partidoliga = False
					
					#calculo del minuto actual
					inicio = m.getElementsByTagName('MatchDate')[0].firstChild.nodeValue
					inicio = time.mktime(time.strptime(inicio, "%Y-%m-%d %H:%M:%S"))
					inicio = datetime.datetime.fromtimestamp(inicio)
					#ahora = datetime.datetime.now()
					# #########PARCHE CUTRE PARA LOS TIEMPOS CON LA DIFERENCIA DE 8 HORAS DE BLUEHOST
                                        #ahora = datetime.datetime.now() + datetime.timedelta(hours=8)
                                        # EN INVIERNO (O POR LO MENOS HOY, 28.10.2009) SON 7 HORAS DE DIFERENCIA!!!
                                        ahora = datetime.datetime.now() + datetime.timedelta(hours=8)
					# ##############################################
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
					
					partido = model.Partido(hometeam, homegoals, awaygoals, awayteam, minuto, partidoliga)

					#strResultados = strResultados + partido.local.nombre + " " + partido.goleslocal + " - " + partido.golesvisitante + " " + partido.visitante.nombre + " (minuto " + partido.minuto + ")\n"
					strResultados = strResultados + partido.local + " " + partido.goleslocal + " - " + partido.golesvisitante + " " + partido.visitante + " (minuto " + partido.minuto + ")\n"
					
					# if liguilla.lower().startswith('true'):
						#ctualizamos la clasificacion
						# ch = handlers.ClasifHandler()
						# ch.actualizarClasifPartido(partido)
						
					#quitamos el partido del htlive
					url = recServer + '/Common/chppxml.axd?file=live&actionType=deleteMatch&matchid=' + xmlMatchID
					response, content = self.http.request(url, 'GET', headers=self.headers)
					doc = minidom.parseString(content)
					matches = doc.getElementsByTagName('Match')
					print "procesado y borrado el partido", xmlMatchID
					print "Quedan", len(matches), "en live.xml"
			#url = recServer + '/Common/chppxml.axd?file=live&actionType=clearAll&version=1.4'
			#response, content = http.request(url, 'GET', headers=headers)
			#doc = minidom.parseString(content)
			#matches = doc.getElementsByTagName('Match')
		except Exception, message:
			traceback.print_exc()
			#print 'No se ha podido tratar el partido', matchid, '\n', sys.exc_info()
			print 'No se ha podido tratar el partido', matchid, '\n'
			print message		
		
		#MOLINORR
		# marcador.appendChild(partidos)
		# print marcador.toprettyxml(encoding="utf-8")
		# print "-----"+str(marcador.toprettyxml(encoding="utf-8"))[90:102]
		# self.afichero(unicode(marcador.toprettyxml(encoding="utf-8")), fichMarcadorXml)
		# ######
		
		
		
		# if liguilla.lower().startswith('true'):
			# ch = handlers.ClasifHandler()
			# strClasif = strClasif + "\nCLASIFICACION ACTUAL\n"
			# strClasif = strClasif + "\nGrupo A\n\n"
			# strClasif = strClasif + ch.getStrClasifTemp('A')
			# strClasif = strClasif + "\n\n"
			# strClasif = strClasif + "\nGrupo B\n\n"
			# strClasif = strClasif + ch.getStrClasifTemp('B')
			# if (partido.minuto == "90"):
				# ch.setearTempComoPerm()
		
		#print strClasif
		strPie = '\n\n\nCarrusel automatico (rev 200)'
		# if liguilla.lower().startswith('true'):
			# strOctavos = self.addOctavosString()
		# else:
			# strOctavos = ""
		strOctavos = ""
			
		strCarr = strResultados + strClasif + strOctavos + strPie
		self.afichero(unicode(strCarr), fichCarrusel)

	def addOctavosString(self):
		ch = handlers.ClasifHandler()
		grupoa = ch.getClasifTempNombresDict('A')
		grupob = ch.getClasifTempNombresDict('B')
		
		str = "\n\nSi la liga termina asi, los octavos de final serian asi:\n\n"
		if self.config.get('cup.pasanporgrupo') == '8':
			#1A - 8B
			str = str + "(1) 1A - 8B: " + grupoa[1] + " - " + grupob[8] + "\n"
			#4B - 5A
			str = str + "(2) 4B - 5A: " + grupob[4] + " - " + grupoa[5] + "\n"
			#7A - 2B
			str = str + "(3) 7A - 2B: " + grupoa[7] + " - " + grupob[2] + "\n"
			#6B - 3A
			str = str + "(4) 6B - 3A: " + grupob[6] + " - " + grupoa[3] + "\n"
			#2A - 7B
			str = str + "(5) 2A - 7B: " + grupoa[2] + " - " + grupob[7] + "\n"
			#3B - 6A
			str = str + "(6) 3B - 6A: " + grupob[3] + " - " + grupoa[6] + "\n"
			#8A - 1B
			str = str + "(7) 8A - 1B: " + grupoa[8] + " - " + grupob[1] + "\n"
			#5B - 4A
			str = str + "(8) 5B - 4A: " + grupob[5] + " - " + grupoa[4] + "\n"
		elif self.config.get('cup.pasanporgrupo') == '4':
			#1A - 4B
			str = str + "(1) 1A - 4B: " + grupoa[1] + " - " + grupob[4] + "\n"
			#2B - 3A
			str = str + "(2) 2B - 3A: " + grupob[2] + " - " + grupoa[3] + "\n"
			#2A - 3B
			str = str + "(3) 2A - 3B: " + grupoa[2] + " - " + grupob[3] + "\n"
			#1B - 4A
			str = str + "(4) 1B - 4A: " + grupob[1] + " - " + grupoa[4] + "\n"
		
		str = str + "\n\n(ojo, puede ocurrir que, en caso de empate, cupmanager.org resuelva el desempate de forma diferente a este script, por lo que cambiaria la clasificacion y, por ende, los cruces de octavos de final)\nLos cruces de cuartos serian:\n(1) vs (2), (3) vs (4)...\n\n"
		
		return str